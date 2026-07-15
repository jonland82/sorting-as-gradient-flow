# Sorting as Gradient Flow on the Permutohedron

Jonathan Robert Landers, 2026

This repository accompanies the updated LaTeX manuscript **Sorting as Gradient Flow on the Permutohedron**. The paper's main innovation is a continuous-time formulation of sorting as an ambient gradient flow on the permutohedron, placed alongside the discrete geometries induced by sorting operations themselves: adjacent swaps traverse edges and pay inversion distance one step at a time, arbitrary comparisons impose global half-space constraints on candidate rank maps, and the Euclidean flow follows straight-line contraction inside the convex permutohedron.

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

Its vertices are rank words. Adjacent transpositions are edges of the 1-skeleton, so adjacent-swap algorithms move locally from vertex to vertex. That local geometry resolves inversions one at a time and naturally gives the quadratic regime.

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

This is the manuscript's central modeling move. It is not claimed to be the literal path of a discrete sorting algorithm; it is a relaxation that puts local walks, global comparison constraints, and straight-line rank-displacement contraction inside one frame. If $m$ denotes the number of comparisons, the manuscript defines the per-item comparison clock

$$
\tau=\frac{m}{n}.
$$

One binary comparison advances $\tau$ by $1/n$. On this normalization, the continuous threshold time

$$
t=\Theta(\log n)
$$

corresponds to $\tau=\Theta(\log n)$ and therefore to the optimal comparison scale

$$
m=\Theta(n \log n),
$$

The rigorous lower-bound proof remains the classical decision-tree argument; the flow supplies a compatible asymptotic scale.

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

## Repository Status

The updated manuscript, companion draft, figure script, README, and GitHub Pages entry point now live at the repository root. Earlier draft artifacts have been moved into [`old_draft/`](old_draft/).
