"""Exhaustive finite checks on permutations and comparison histories.

The paper's general proofs are not replaced by finite enumeration.  These
checks exercise every permutation through moderate n, where exhaustive search
is still fast enough to catch indexing, inverse-permutation, sign, and strict
inequality mistakes.
"""

from __future__ import annotations

import math
from itertools import permutations

import sympy as sp

from verification_utils import run_group


def potential(rank_word: tuple[int, ...]) -> int:
    """Return V(r)=1/2*||r-(1,...,n)||^2 as an exact integer."""

    squared_distance = sum(
        (rank - sorted_rank) ** 2
        for sorted_rank, rank in enumerate(rank_word, start=1)
    )
    # For permutations the squared distance is always even, so V is integral.
    assert squared_distance % 2 == 0
    return squared_distance // 2


def inversion_count(rank_word: tuple[int, ...]) -> int:
    """Count pairs that occur in the opposite order from the sorted word."""

    return sum(
        rank_word[left] > rank_word[right]
        for left in range(len(rank_word))
        for right in range(left + 1, len(rank_word))
    )


def vertices_and_affine_dimension() -> bool:
    """Proposition 3.2: n! vertices lie in an (n-1)-dimensional hyperplane."""

    for n in range(2, 8):
        vertices = list(permutations(range(1, n + 1)))
        if len(vertices) != math.factorial(n):
            return False
        if any(sum(vertex) != n * (n + 1) // 2 for vertex in vertices):
            return False

        # Swapping each adjacent pair of the identity produces the difference
        # vectors e_i-e_{i+1}.  Their exact rank supplies the n-1 lower bound;
        # the constant-sum equation supplies the matching upper bound.
        identity = sp.Matrix(range(1, n + 1))
        adjacent_differences = []
        for index in range(n - 1):
            neighbor = list(range(1, n + 1))
            neighbor[index], neighbor[index + 1] = neighbor[index + 1], neighbor[index]
            adjacent_differences.append(sp.Matrix(neighbor) - identity)
        if sp.Matrix.hstack(*adjacent_differences).rank() != n - 1:
            return False
    return True


def adjacent_swap_and_lyapunov_bounds() -> bool:
    """Proposition 4.1: verify the exact drop and both bounds for every word."""

    for n in range(2, 8):
        for rank_word in permutations(range(1, n + 1)):
            inversions = inversion_count(rank_word)
            value = potential(rank_word)
            if not inversions <= value <= (n - 1) * inversions:
                return False

            for index in range(n - 1):
                left, right = rank_word[index : index + 2]
                if left <= right:
                    continue
                swapped = list(rank_word)
                swapped[index], swapped[index + 1] = right, left
                swapped_word = tuple(swapped)
                if potential(rank_word) - potential(swapped_word) != left - right:
                    return False
                if inversion_count(rank_word) - inversion_count(swapped_word) != 1:
                    return False
    return True


Constraint = tuple[int, str, int]


def candidate_satisfies(candidate: tuple[int, ...], constraint: Constraint) -> bool:
    """Evaluate a comparison in fixed original-item coordinates."""

    left_item, relation, right_item = constraint
    if relation == "<":
        return candidate[left_item] < candidate[right_item]
    return candidate[left_item] > candidate[right_item]


def bubble_sort_history(original_rank_map: tuple[int, ...]) -> tuple[list[Constraint], tuple[int, ...]]:
    """Run BubbleSort while recording comparisons between original items.

    ``positions`` maps current array positions to original item identities.
    Recording those identities before a possible swap is the bookkeeping point
    emphasized in Section 3.2 of the paper.
    """

    n = len(original_rank_map)
    positions = list(range(n))
    history: list[Constraint] = []

    for unsorted_end in range(n - 1, 0, -1):
        for position in range(unsorted_end):
            left_item = positions[position]
            right_item = positions[position + 1]
            left_rank = original_rank_map[left_item]
            right_rank = original_rank_map[right_item]
            relation = "<" if left_rank < right_rank else ">"
            history.append((left_item, relation, right_item))
            if relation == ">":
                positions[position], positions[position + 1] = right_item, left_item

    return history, tuple(positions)


def complete_histories_identify_rank_maps() -> bool:
    """Proposition 3.3: every complete BubbleSort leaf has one candidate map."""

    # n=6 covers 720 possible true rank maps and 720 candidate maps per leaf,
    # while keeping this exhaustive check quick enough for routine use.
    for n in range(2, 7):
        candidates = list(permutations(range(1, n + 1)))
        for true_rank_map in candidates:
            history, sorted_item_order = bubble_sort_history(true_rank_map)
            feasible = [
                candidate
                for candidate in candidates
                if all(candidate_satisfies(candidate, constraint) for constraint in history)
            ]
            if feasible != [true_rank_map]:
                return False

            # Applying the output permutation to the identified original rank
            # map must produce the sorted rank word, as in equation (20).
            output_ranks = tuple(true_rank_map[item] for item in sorted_item_order)
            if output_ranks != tuple(range(1, n + 1)):
                return False
    return True


def running_example_candidate_counts() -> bool:
    """Table 1: the [5,4,2] example shrinks 6 -> 3 -> 2 -> 1."""

    candidates = list(permutations((1, 2, 3)))
    # Original items 0,1,2 have ranks 3,2,1.  The three comparisons in the
    # paper are rho_1>rho_2, rho_1>rho_3, rho_2>rho_3 (converted to 0-based
    # Python item labels here).
    constraints: list[Constraint] = [
        (0, ">", 1),
        (0, ">", 2),
        (1, ">", 2),
    ]
    counts = [len(candidates)]
    for constraint in constraints:
        candidates = [
            candidate
            for candidate in candidates
            if candidate_satisfies(candidate, constraint)
        ]
        counts.append(len(candidates))
    return counts == [6, 3, 2, 1] and candidates == [(3, 2, 1)]


def canonical_p3_halfspaces() -> bool:
    """Figure 3: x1<x2 and x2<x3 isolate the increasing rank word."""

    feasible = [
        word
        for word in permutations((1, 2, 3))
        if word[0] < word[1] and word[1] < word[2]
    ]
    return feasible == [(1, 2, 3)]


def reverse_word_is_farthest() -> bool:
    """Proposition 4.3 and Eq. (56): reverse order realizes the diameter."""

    for n in range(2, 9):
        target = tuple(range(1, n + 1))
        reverse = tuple(reversed(target))
        squared_distances = [
            sum((left - right) ** 2 for left, right in zip(word, target, strict=True))
            for word in permutations(target)
        ]
        expected = n * (n**2 - 1) // 3
        if max(squared_distances) != expected:
            return False
        if sum((left - right) ** 2 for left, right in zip(reverse, target, strict=True)) != expected:
            return False
    return True


def decision_tree_leaf_count() -> bool:
    """Lemma 2.1: fewer than ceil(log2(n!)) binary levels cannot hold n! leaves."""

    for n in range(2, 13):
        required_leaves = math.factorial(n)
        minimum_height = math.ceil(math.log2(required_leaves))
        if 2 ** (minimum_height - 1) >= required_leaves:
            return False
        if 2**minimum_height < required_leaves:
            return False
    return True


def main() -> int:
    checks = [
        ("Lemma 2.1: exact finite binary-tree leaf counts", decision_tree_leaf_count),
        ("Proposition 3.2: vertex count, affine containment, and dimension", vertices_and_affine_dimension),
        ("Proposition 3.3: complete fixed-coordinate histories isolate one map", complete_histories_identify_rank_maps),
        ("Table 1: candidate counts 6 -> 3 -> 2 -> 1", running_example_candidate_counts),
        ("Figure 3: canonical P3 comparison cuts isolate (1,2,3)", canonical_p3_halfspaces),
        ("Proposition 4.1: swap drop and inversion/potential inequalities", adjacent_swap_and_lyapunov_bounds),
        ("Proposition 4.3 / Eq. (56): reverse word realizes finite-case diameter", reverse_word_is_farthest),
    ]
    count = run_group("Exhaustive combinatorial verification", checks)
    print(f"\nCombinatorial verification complete: {count} checks passed.")
    return count


if __name__ == "__main__":
    main()
