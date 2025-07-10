**Sorting as Gradient Flow on the Permutohedron**  
Jonathan Landers, 2025  

- [Manuscript PDF](https://github.com/jonland82/sorting-as-gradient-flow/blob/main/sorting-as-gradient-flow.pdf)
- [Proof Verification Scripts](https://github.com/jonland82/sorting-as-gradient-flow/blob/main/sorting-as-gradient-flow_proof-verifications.ipynb)
- [Manuscript Figure Generation Code](https://github.com/jonland82/sorting-as-gradient-flow/blob/main/sorting-as-gradient-flow_paper-figures.ipynb)

This repository accompanies the paper *"Sorting as Gradient Flow on the Permutohedron"* (Landers, 2025), which presents a novel continuous-time geometric formulation of sorting. The formulation provides an independent derivation of the classical Ω(n log n) lower bound for comparison-based sorting.

**Summary**  
Efficient sorting algorithms are known to navigate an exponentially large space of permutations using only O(n log n) comparisons. This work offers a continuous geometric explanation for this efficiency by modeling sorting as a gradient flow on the permutohedron—a polytope whose vertices correspond to permutations.

**Main Contribution**

- **Gradient Flow Interpretation**: Sorting is expressed as a continuous-time dynamical system governed by the differential equation dx/dt = v_s - x(t), where v_s is the sorted vector (1, 2, ..., n). The system exhibits exponential contraction toward the sorted vector.

- **Independent Lower Bound Proof**: Assuming each comparison corresponds to a step of size O(1/n) along the continuous flow, the total number of comparisons required is shown to satisfy T = Θ(n log n), thus recovering the classical lower bound through geometric reasoning.

- **Geometric Constraint Perspective**: Each comparison imposes a linear constraint intersecting the permutohedron. A sequence of O(n log n) such constraints is sufficient to isolate the sorted permutation as a unique vertex of the polytope.

- **Unifying Framework**: The continuous formulation complements traditional decision-tree and combinatorial approaches, offering a unified perspective on how structure enables efficient traversal of exponential spaces.
