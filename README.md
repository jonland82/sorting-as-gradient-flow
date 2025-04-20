
### Sorting as Gradient Flow on the Permutohedron

- Jonathan Landers, 2025

This repository accompanies the paper *"Sorting as Gradient Flow on the Permutohedron"* (Landers, 2025), which introduces a novel continuous-time geometric formulation of sorting. The formulation yields an independent derivation of the classical $\Omega(n \log n)$ lower bound for comparison-based sorting.

#### Summary

Efficient sorting algorithms are known to navigate an exponentially large permutation space using only $O(n \log n)$ comparisons. This work provides a continuous geometric explanation for this efficiency by modeling sorting as gradient flow on the permutohedron—a polytope whose vertices represent permutations.

#### Main Contribution

- **Gradient Flow Interpretation**: Sorting is expressed as a continuous dynamical system
  $$
  \dot{x}(t) = v_s - x(t),
  $$
  where $v_s = (1, 2, \dots, n)$ is the sorted vector. The system contracts exponentially:
  $$
  \|x(t) - v_s\|^2 = \|x(0) - v_s\|^2 e^{-2t}.
  $$

- **Independent Lower Bound Proof**: If each comparison corresponds to an $O(1/n)$ step along the flow, then total comparisons required satisfy $T = \Theta(n \log n)$, recovering the classical lower bound.

- **Geometric Constraint View**: Each comparison defines a linear constraint that intersects the permutohedron. A sequence of $O(n \log n)$ such constraints suffices to isolate the sorted permutation as a unique vertex.

- **Unifying Framework**: The continuous formulation complements classical decision-tree and combinatorial arguments, offering a unified perspective on why structure enables efficient traversal of exponential spaces.
