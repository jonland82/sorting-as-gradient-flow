# Proof Verification Suite

This directory contains executable checks for the principal mathematical claims in [`sorting_as_gradient_flow.pdf`](../sorting_as_gradient_flow.pdf). The scripts combine exact SymPy manipulation, exhaustive enumeration of finite permutation spaces, and deterministic numerical experiments with convex constraints.

## Run the Suite

From the repository root:

```powershell
python -m pip install -r proof_verification_suite/requirements.txt
python proof_verification_suite/run_all.py
```

Each successful assertion prints a short `[PASS]` description. Any failed assertion stops the suite and returns a nonzero exit status.

The scripts can also be run separately:

```powershell
python proof_verification_suite/verify_symbolic.py
python proof_verification_suite/verify_combinatorial.py
python proof_verification_suite/verify_numerical_geometry.py
```

## Coverage

| Script | Manuscript claims checked | Method |
| --- | --- | --- |
| `verify_symbolic.py` | Lemma 2.1; Proposition 3.2's constant sum; Proposition 4.1's potential drop; Theorem 4.2's gradient, closed-form solution, contraction, threshold time, and reverse-word radius; the energy-dissipation identity illustrated in the discussion of Figure 4 | Exact symbolic simplification with SymPy |
| `verify_combinatorial.py` | Lemma 2.1's decision-tree leaf capacity; Proposition 3.2's vertex count and dimension; Proposition 3.3's fixed-coordinate candidate maps; Table 1 and Figure 3; Proposition 4.1's Lyapunov bounds; Proposition 4.3 and equation (56)'s reverse-word diameter | Exhaustive permutation enumeration through moderate `n` |
| `verify_numerical_geometry.py` | Theorem 4.2 trajectories; equations (65)-(67) for the straight-line flow, braid walls, and subset-sum facets; Proposition 4.6's tangent-cone projection; a target-excluding constraint; Proposition 4.3, Theorem 4.4, and Corollary 4.5 scales | NumPy sampling and SciPy optimization with a fixed random seed |

## Interpretation

The symbolic checks establish the listed algebraic identities exactly. Exhaustive checks establish their finite instances over the stated ranges. Numerical optimization is useful for detecting sign, indexing, feasibility, and projection mistakes, but it is not a formal proof for arbitrary dimension.

In particular, the suite does not claim that the gradient flow is a literal execution trace of a comparison sorter. It preserves the paper's distinction: comparison constraints reduce informational ambiguity, while the continuous flow measures metric contraction. As stated in Corollary 4.5 and the paragraph following it, the normalized comparison clock and maximal relaxation time agree only in asymptotic order; the paper does not equate one unit of flow time with one sweep of comparisons.
