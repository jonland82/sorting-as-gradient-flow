# Sorting as Gradient Flow on the Permutohedron

Jonathan Robert Landers, 2026

This repository accompanies the updated LaTeX manuscript **Sorting as Gradient Flow on the Permutohedron**. The paper's main contribution is a continuous-time model of sorting as motion through space. A quadratic potential on the permutohedron generates an ambient gradient flow that contracts toward the fixed sorted vertex. This dynamical picture is set against adjacent-swap paths and comparison half-spaces as discrete geometric foils: comparisons remove informational ambiguity, while the flow removes metric distance.

## Project Page

Live project page: <https://jonland82.github.io/sorting-as-gradient-flow/>

Code repository: <https://github.com/jonland82/sorting-as-gradient-flow>

The GitHub Pages entry point is [`index.html`](index.html). It gives an intuitive project-page version of the paper: the decision-tree lower bound supplies the information scale, the permutohedron supplies the geometry, and the paper's ambient gradient-flow formulation supplies the continuous relaxation that makes contraction visible.

## Current Manuscripts

- [`sorting_as_gradient_flow.pdf`](sorting_as_gradient_flow.pdf)
  Current LaTeX manuscript. This is the canonical version for the repository.

- [`flattening_entropy.pdf`](flattening_entropy.pdf)
  In-progress companion manuscript. It extends the sorting geometry story toward algorithms as geodesics and preprocessing as partial curvature or entropy removal.

## Supporting Code

- [`sorting-as-gradient-flow_paper-figures.py`](sorting-as-gradient-flow_paper-figures.py)
  Figure-generation script for the updated manuscript.

- [`old_draft/sorting-as-gradient-flow.pdf`](old_draft/sorting-as-gradient-flow.pdf)
  Earlier manuscript PDF snapshot retained for reference.

- [`old_draft/sorting-as-gradient-flow_proof-verifications.ipynb`](old_draft/sorting-as-gradient-flow_proof-verifications.ipynb)
  Earlier proof-verification notebook retained for reference.

- [`old_draft/sorting-as-gradient-flow_paper-figures.ipynb`](old_draft/sorting-as-gradient-flow_paper-figures.ipynb)
  Earlier notebook version of the figure-generation workflow.

## Mathematical Story

Sorting starts with a factorial search space. For distinct inputs, there are

$$
n!
$$

possible order types. A deterministic comparison sorter can be modeled by a binary decision tree, so a correct tree must have at least the factorial number of leaves. A binary tree of height h has at most that many leaves only if

$$
2^h \ge n!,
$$

and therefore

$$
h \ge \log_2(n!) = \Theta(n \log n).
$$

The paper places this familiar lower bound inside the geometry of the permutohedron. Let

$$
v_s = (1,2,\ldots,n)
$$

be the sorted rank word. The permutohedron is

$$
\mathcal P_n = \mathrm{conv}\{\pi(v_s): \pi \in S_n\}.
$$

Its vertices are rank words. Adjacent transpositions are edges of the 1-skeleton, so adjacent-swap algorithms move locally from vertex to vertex. That local geometry resolves inversions one at a time and naturally gives the quadratic regime. The same quadratic potential used by the continuous flow decreases strictly under every inversion-removing adjacent swap.

General comparisons act differently. Comparisons occur between current positions, but their outcomes must be recorded in a common coordinate frame. If positions $a$ and $b$ contain original items $p_t(a)$ and $p_t(b)$, a less-than outcome becomes the candidate-rank inequality

$$
r_{p_t(a)} < r_{p_t(b)}.
$$

Each outcome selects a half-space in fixed original-item coordinates. A sorting algorithm therefore does not merely walk the polytope; it repeatedly cuts the feasible candidate rank maps until one vertex remains. This is the geometric version of the decision-tree story: comparison information collapses the feasible set.

## Gradient-Flow Relaxation

The continuous part of the paper introduces the potential

$$
V(x) = \frac{1}{2}\|x-v_s\|^2,
$$

whose ambient Euclidean gradient flow is

$$
\dot{x}(t) = -\nabla V(x(t)) = v_s - x(t).
$$

The solution contracts exactly:

$$
x(t) = v_s + (x(0)-v_s)e^{-t},
$$

so that

$$
\|x(t)-v_s\|^2 = \|x(0)-v_s\|^2 e^{-2t}.
$$

This is the manuscript's central modeling move. It is not claimed to be the literal path of a discrete sorting algorithm; it is a relaxation that puts local walks, global comparison constraints, and straight-line rank-displacement contraction inside one frame.

For a Euclidean threshold $0<\varepsilon<\operatorname{diam}(\mathcal P_n)$, the manuscript now determines the exact worst-case relaxation time over the permutohedron:

$$
t_{\max}(\varepsilon)
= \log\frac{\operatorname{diam}(\mathcal P_n)}{\varepsilon}
= \frac{1}{2}\log\frac{n(n^2-1)}{3\varepsilon^2}.
$$

For every fixed $\varepsilon>0$, this gives

$$
\dim(\mathcal P_n)\,t_{\max}(\varepsilon)
= \Theta(n\log n).
$$

Equivalently, $\dim(\mathcal P_n)\log\operatorname{diam}(\mathcal P_n)=\Theta(n\log n)$. This factorization is intrinsic to the polytope and its quadratic relaxation.

To compare it with classical sorting, let $C(n)$ be the optimal worst-case number of comparisons and define the normalized comparison clock

$$
\tau(n)=\frac{C(n)}{n}.
$$

The classical bounds give $\tau(n)=\Theta(\log n)$, matching the asymptotic order of $t_{\max}(\varepsilon)$. This does not identify a unit of flow time with a sweep of comparisons: the rigorous lower-bound proof remains the classical decision-tree argument, while the flow supplies an independently derived geometric scale.

The updated manuscript also clarifies the relation between constraint geometry and the ambient flow. If a closed convex metric constraint

$$
K \subseteq \mathcal P_n
$$

contains the sorted vertex $v_s$, then for every $x\in K$ the descent direction already lies in the tangent cone and projection is inactive:

$$
v_s-x\in T_K(x),
\qquad
\Pi_{T_K(x)}(v_s-x)=v_s-x.
$$

Thus the projected flow agrees with the ambient flow whenever the target remains feasible. Comparison half-spaces should be read as describing information reduction, while the Euclidean flow separately measures metric contraction. If a metric constraint excludes $v_s$, constrained descent instead approaches the point in that region nearest to $v_s$.

## Future Direction: Flattening Entropy

The companion manuscript develops the broader idea that computational models induce geometries on state space. In that language, a lower bound is a geometric obstruction to flattening the problem inside the permitted model.

Counting sort is treated as a literal flattening in histogram coordinates. Comparison sorting carries flattening entropy

$$
F_{\mathrm{cmp}}(n) = \log(n!) + O(1).
$$

Ordered bucketization removes an exact multinomial block of entropy. If the bucket occupancies are

$$
n_1,\ldots,n_B,
$$

the flattening gain is

$$
G(x;\beta)
= \log(n!) - \sum_{j=1}^B \log(n_j!)
= \log\frac{n!}{\prod_{j=1}^B n_j!},
$$

and the residual within-bucket comparison entropy is

$$
F_{\mathrm{res}}(x;\beta)
= \sum_{j=1}^B \log(n_j!).
$$

Radix sorting appears as the iteration of this partial-flattening principle: each ordered pass removes another layer of residual entropy until the comparison problem has been trivialized.

## Proof Verification Suite

The supporting [`proof_verification_suite/`](proof_verification_suite/) provides reproducible checks for the paper's principal mathematical claims. Install its small scientific-Python dependency set and run every check from the repository root:

```powershell
python -m pip install -r proof_verification_suite/requirements.txt
python proof_verification_suite/run_all.py
```

The suite checks the decision-tree bound, permutohedron affine geometry, fixed-coordinate comparison histories, adjacent-swap potential descent, the exact gradient-flow solution and contraction law, reverse-permutation distance and diameter, subset-sum constraints, braid hyperplanes, and target-feasible tangent-cone projection. See [`proof_verification_suite/README.md`](proof_verification_suite/README.md) for the claim-by-claim coverage table and commands for running individual scripts.

Symbolic identities are checked exactly. Exhaustive permutation checks cover explicitly documented finite ranges, while numerical optimization checks use a fixed random seed and floating-point tolerances. Those numerical experiments are diagnostics rather than formal proofs in arbitrary dimension, and the suite preserves the manuscript's distinction between comparison information and metric flow.

## Repository Status

Earlier draft materials are archived in [`old_draft/`](old_draft/).
