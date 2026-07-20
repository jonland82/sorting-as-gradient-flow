"""Exact symbolic checks for the paper's algebraic identities.

These checks use SymPy, so equalities are simplified exactly rather than
judged with floating-point tolerances.  Equation and proposition numbers refer
to ``sorting_as_gradient_flow.pdf`` (the July 2026 repository version).
"""

from __future__ import annotations

import sympy as sp

from verification_utils import run_group


def decision_tree_equation() -> bool:
    """Equation (7): solving 2**h = n! gives h = log_2(n!)."""

    h = sp.symbols("h", real=True)
    n = sp.symbols("n", positive=True, integer=True)
    solution = sp.solve(sp.Eq(2**h, sp.factorial(n)), h)[0]
    expected = sp.log(sp.factorial(n), 2)
    return sp.simplify(solution - expected) == 0


def constant_coordinate_sum() -> bool:
    """Equations (12)-(13): every rank word has total n(n+1)/2."""

    i, n = sp.symbols("i n", positive=True, integer=True)
    total = sp.summation(i, (i, 1, n))
    return sp.simplify(total - n * (n + 1) / 2) == 0


def adjacent_swap_drop() -> bool:
    """Proposition 4.1: swapping adjacent a>b lowers V by a-b."""

    a, b, i = sp.symbols("a b i", real=True)

    # Only positions i and i+1 change.  The factor 1/2 belongs to V.
    before = ((a - i) ** 2 + (b - (i + 1)) ** 2) / 2
    after = ((b - i) ** 2 + (a - (i + 1)) ** 2) / 2
    return sp.simplify((before - after) - (a - b)) == 0


def gradient_is_target_minus_state() -> bool:
    """Equations (23) and (30): -grad V(x) = v_s-x."""

    # Four generic coordinates are enough to verify SymPy differentiates the
    # separable n-coordinate formula in the claimed way.
    coordinates = sp.symbols("x1:5", real=True)
    targets = (1, 2, 3, 4)
    potential = sp.Rational(1, 2) * sum(
        (coordinate - target) ** 2
        for coordinate, target in zip(coordinates, targets, strict=True)
    )
    negative_gradient = sp.Matrix(
        [-sp.diff(potential, coordinate) for coordinate in coordinates]
    )
    expected = sp.Matrix(
        [target - coordinate for coordinate, target in zip(coordinates, targets, strict=True)]
    )
    return negative_gradient == expected


def closed_form_solves_flow() -> bool:
    """Equation (31): the proposed solution satisfies the ODE and x(0)=x0."""

    t = sp.symbols("t", nonnegative=True)
    target, initial = sp.symbols("target initial", real=True)
    candidate = target + (initial - target) * sp.exp(-t)
    ode_residual = sp.simplify(sp.diff(candidate, t) - (target - candidate))
    initial_residual = sp.simplify(candidate.subs(t, 0) - initial)
    return ode_residual == 0 and initial_residual == 0


def squared_norm_contraction() -> bool:
    """Equation (32): squared displacement contracts by exp(-2t)."""

    t = sp.symbols("t", nonnegative=True)
    displacement = sp.symbols("d1:5", real=True)
    evolved = [component * sp.exp(-t) for component in displacement]
    evolved_norm_sq = sum(component**2 for component in evolved)
    initial_norm_sq = sum(component**2 for component in displacement)
    return sp.simplify(evolved_norm_sq - initial_norm_sq * sp.exp(-2 * t)) == 0


def energy_dissipation_identity() -> bool:
    """The flow obeys dV/dt = -||grad V||^2."""

    t = sp.symbols("t", real=True)
    displacement = sp.symbols("d1:5", real=True)
    potential = sp.Rational(1, 2) * sum(
        (component * sp.exp(-t)) ** 2 for component in displacement
    )
    gradient_norm_sq = sum(
        (component * sp.exp(-t)) ** 2 for component in displacement
    )
    return sp.simplify(sp.diff(potential, t) + gradient_norm_sq) == 0


def threshold_time() -> bool:
    """Equation (33): at the stated time, squared distance equals epsilon^2."""

    radius_sq, epsilon = sp.symbols("radius_sq epsilon", positive=True)
    threshold = sp.Rational(1, 2) * sp.log(radius_sq / epsilon**2)
    remaining_sq = radius_sq * sp.exp(-2 * threshold)
    return sp.simplify(remaining_sq - epsilon**2) == 0


def reverse_word_distance() -> bool:
    """Equations (34)-(35): the reverse word has squared radius n(n^2-1)/3."""

    i, n = sp.symbols("i n", positive=True, integer=True)
    radius_sq = sp.summation((n + 1 - 2 * i) ** 2, (i, 1, n))
    expected = n * (n**2 - 1) / 3
    return sp.simplify(radius_sq - expected) == 0


def reverse_word_potential() -> bool:
    """Equation (35): V is one half of the squared reverse-word radius."""

    n = sp.symbols("n", positive=True, integer=True)
    radius_sq = n * (n**2 - 1) / 3
    potential = sp.Rational(1, 2) * radius_sq
    return sp.simplify(potential - n * (n**2 - 1) / 6) == 0


def main() -> int:
    checks = [
        ("Lemma 2.1 / Eq. (7): binary-tree height equation", decision_tree_equation),
        ("Proposition 3.2 / Eqs. (12)-(13): constant coordinate sum", constant_coordinate_sum),
        ("Proposition 4.1 / Eqs. (25)-(28): adjacent-swap potential drop", adjacent_swap_drop),
        ("Eqs. (23), (30): negative gradient points to the sorted target", gradient_is_target_minus_state),
        ("Theorem 4.2 / Eq. (31): closed-form flow solves the IVP", closed_form_solves_flow),
        ("Theorem 4.2 / Eq. (32): exact squared-norm contraction", squared_norm_contraction),
        ("Gradient-flow energy dissipation: dV/dt = -||grad V||^2", energy_dissipation_identity),
        ("Theorem 4.2 / Eq. (33): threshold-time identity", threshold_time),
        ("Theorem 4.2 / Eq. (34): reverse-word squared distance", reverse_word_distance),
        ("Theorem 4.2 / Eq. (35): reverse-word potential", reverse_word_potential),
    ]
    count = run_group("Exact symbolic verification (SymPy)", checks)
    print(f"\nSymbolic verification complete: {count} checks passed.")
    return count


if __name__ == "__main__":
    main()
