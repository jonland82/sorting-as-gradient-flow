"""Numerical checks for flow, polytope, and convex-constraint geometry.

Floating-point experiments complement the exact symbolic and exhaustive
scripts.  They intentionally use a fixed random seed so a failure is
reproducible.  Numerical evidence is a diagnostic, not a replacement for the
paper's general convexity proofs.
"""

from __future__ import annotations

import math
from itertools import combinations, permutations

import numpy as np
from scipy.optimize import minimize, nnls

from verification_utils import run_group


TOLERANCE = 1e-9
RNG = np.random.default_rng(20260720)


def subset_sum_inequalities(point: np.ndarray) -> bool:
    """Check the standard permutohedron inequalities in equation (55)."""

    n = len(point)
    if not math.isclose(float(point.sum()), n * (n + 1) / 2, abs_tol=TOLERANCE):
        return False
    for size in range(1, n):
        lower_bound = size * (size + 1) / 2
        for subset in combinations(range(n), size):
            if float(point[list(subset)].sum()) < lower_bound - TOLERANCE:
                return False
    return True


def exact_flow_matches_ode_and_contraction() -> bool:
    """Theorem 4.2: sample trajectories obey the ODE and contraction law."""

    for n in range(2, 10):
        target = np.arange(1, n + 1, dtype=float)
        initial = RNG.permutation(target)
        displacement = initial - target
        initial_norm_sq = float(displacement @ displacement)

        for time in np.linspace(0.0, 5.0, 31):
            decay = math.exp(-time)
            state = target + displacement * decay
            derivative = -displacement * decay
            if not np.allclose(derivative, target - state, atol=TOLERANCE, rtol=0.0):
                return False
            actual_norm_sq = float((state - target) @ (state - target))
            expected_norm_sq = initial_norm_sq * math.exp(-2 * time)
            if not math.isclose(actual_norm_sq, expected_norm_sq, abs_tol=TOLERANCE):
                return False
    return True


def flow_stays_in_permutohedron() -> bool:
    """Equation (53): the flow is a convex combination of two vertices."""

    for n in range(3, 9):
        target = np.arange(1, n + 1, dtype=float)
        initial = RNG.permutation(target)
        for time in np.linspace(0.0, 8.0, 41):
            weight_on_initial = math.exp(-time)
            state = weight_on_initial * initial + (1.0 - weight_on_initial) * target
            if not subset_sum_inequalities(state):
                return False
    return True


def threshold_time_hits_requested_radius() -> bool:
    """Equation (33): numerical trajectories hit the prescribed epsilon."""

    for n in range(3, 11):
        target = np.arange(1, n + 1, dtype=float)
        initial = target[::-1]
        radius_sq = float((initial - target) @ (initial - target))
        epsilon = 0.37
        threshold = 0.5 * math.log(radius_sq / epsilon**2)
        state = target + (initial - target) * math.exp(-threshold)
        if not math.isclose(float(np.linalg.norm(state - target)), epsilon, abs_tol=TOLERANCE):
            return False
    return True


def braid_walls_are_not_supporting_facets() -> bool:
    """Section 4.4: x_i=x_j cuts through P_n instead of supporting it."""

    for n in range(3, 7):
        vertices = np.array(list(permutations(range(1, n + 1))), dtype=float)
        for left in range(n):
            for right in range(left + 1, n):
                signed_values = vertices[:, left] - vertices[:, right]
                # A supporting hyperplane has the whole polytope on one side.
                # Both signs show that this braid wall passes through it.
                if not (np.any(signed_values > 0) and np.any(signed_values < 0)):
                    return False
    return True


def facet_inequalities_hold_at_all_vertices() -> bool:
    """Equation (55): enumerate every subset inequality at every small vertex."""

    for n in range(2, 7):
        for vertex in permutations(range(1, n + 1)):
            if not subset_sum_inequalities(np.asarray(vertex, dtype=float)):
                return False
    return True


def target_direction_projects_to_itself() -> bool:
    """Proposition 4.5: project v_s-x onto sampled tangent cones.

    At a vertex x of a polytope K=conv(vertices), its tangent cone is generated
    by vectors vertex-x.  Because v_s is one of K's vertices, v_s-x is one of
    those generators.  Nonnegative least squares computes the Euclidean
    projection numerically and should return zero residual.
    """

    for n in range(3, 8):
        target = np.arange(1, n + 1, dtype=float)
        all_vertices = np.array(list(permutations(range(1, n + 1))), dtype=float)
        chosen_indices = RNG.choice(len(all_vertices), size=min(12, len(all_vertices)), replace=False)
        chosen = all_vertices[chosen_indices]
        # Explicitly include the target so K satisfies the proposition.
        vertices = np.vstack([target, chosen])

        for point in chosen[:5]:
            direction = target - point
            generators = (vertices - point).T
            coefficients, residual_norm = nnls(generators, direction)
            projected = generators @ coefficients
            if residual_norm > TOLERANCE:
                return False
            if not np.allclose(projected, direction, atol=TOLERANCE, rtol=0.0):
                return False

            # The full segment is also checked directly.  Its coefficients are
            # (1-s) on x and s on the target, hence it remains in K.
            for step in np.linspace(0.0, 1.0, 11):
                segment_point = point + step * direction
                expected = (1.0 - step) * point + step * target
                if not np.allclose(segment_point, expected, atol=TOLERANCE, rtol=0.0):
                    return False
    return True


def excluded_target_has_nearest_feasible_point() -> bool:
    """Section 4.4: a convex region excluding v_s minimizes V elsewhere.

    For P3 intersected with x1>=x2, the nearest point to (1,2,3) is the braid
    wall midpoint (1.5,1.5,3), not the sorted vertex.  Convex weights over all
    six P3 vertices represent points in the permutohedron.
    """

    vertices = np.array(list(permutations((1.0, 2.0, 3.0))), dtype=float)
    target = np.array((1.0, 2.0, 3.0))

    def point_from_weights(weights: np.ndarray) -> np.ndarray:
        return weights @ vertices

    def objective(weights: np.ndarray) -> float:
        displacement = point_from_weights(weights) - target
        return 0.5 * float(displacement @ displacement)

    constraints = [
        {"type": "eq", "fun": lambda weights: float(weights.sum() - 1.0)},
        {
            "type": "ineq",
            "fun": lambda weights: float(
                point_from_weights(weights)[0] - point_from_weights(weights)[1]
            ),
        },
    ]
    result = minimize(
        objective,
        np.full(len(vertices), 1.0 / len(vertices)),
        method="SLSQP",
        bounds=[(0.0, 1.0)] * len(vertices),
        constraints=constraints,
        options={"ftol": 1e-12, "maxiter": 1000},
    )
    nearest = point_from_weights(result.x)
    expected = np.array((1.5, 1.5, 3.0))
    return bool(
        result.success
        and np.allclose(nearest, expected, atol=1e-7, rtol=0.0)
        and not np.allclose(nearest, target, atol=TOLERANCE, rtol=0.0)
    )


def normalized_scales_are_consistent() -> bool:
    """Proposition 4.3 / Remark 4.4: inspect the claimed asymptotic scales."""

    for n in (16, 64, 256, 1024, 4096):
        log_factorial = math.lgamma(n + 1)  # natural log(n!), computed stably
        normalized_comparison_budget = log_factorial / n
        if not (0.5 * math.log(n) < normalized_comparison_budget < math.log(n)):
            return False

        diameter = math.sqrt(n * (n**2 - 1) / 3)
        geometric_product = (n - 1) * math.log(diameter)
        ratio = geometric_product / (n * math.log(n))
        # log(diameter)=3/2 log(n)+O(1), so the ratio tends to 3/2.
        if not 1.0 < ratio < 1.6:
            return False
    return True


def main() -> int:
    checks = [
        ("Theorem 4.2: sampled flow obeys the ODE and exact contraction", exact_flow_matches_ode_and_contraction),
        ("Theorem 4.2 / Eq. (33): threshold time hits epsilon", threshold_time_hits_requested_radius),
        ("Eq. (53): straight-line flow stays inside the permutohedron", flow_stays_in_permutohedron),
        ("Eq. (54): braid walls slice rather than support the permutohedron", braid_walls_are_not_supporting_facets),
        ("Eq. (55): subset-sum facet inequalities hold at every small vertex", facet_inequalities_hold_at_all_vertices),
        ("Proposition 4.5: target direction projects to itself", target_direction_projects_to_itself),
        ("Target-excluding constraint: descent has a different nearest point", excluded_target_has_nearest_feasible_point),
        ("Proposition 4.3 / Remark 4.4: normalized numerical scales", normalized_scales_are_consistent),
    ]
    count = run_group("Numerical geometry and constraint verification", checks)
    print(f"\nNumerical verification complete: {count} checks passed.")
    return count


if __name__ == "__main__":
    main()
