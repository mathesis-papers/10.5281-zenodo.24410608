# Hardin's six-column trace recurrence and Barker's generating functions

**Authors:** Haobo Ma, Wenlin Zhang

We prove the empirical recurrence in R. H. Hardin's OEIS entry A185765, revision 9, sole FORMULA field (October 3, 2025; submitted February 3, 2011). It counts labeled (n+1)-by-6 binary arrays whose contiguous 2-by-2 blocks have unequal traces at horizontal and vertical neighbors. A row-pair transfer operator reduces the all-length assertion to three exact finite identities. The recurrence holds for every n >= 13 and fails at n = 12, where its residual is -4160. Its reduced rational generating function proves that nine is the least possible eventual recurrence order over Q. The same method proves the smaller-width recurrences and Colin Barker's conjectural generating functions in A185761-A185764, including his two-column closed form. Transposition, divisibility by eight, and rationality at every fixed width give further consequences for Hardin's bivariate table A185769.

- PDF: [frozen public file](paper.pdf)
- DOI: [https://doi.org/10.5281/zenodo.24410609](https://doi.org/10.5281/zenodo.24410609)
- Concept DOI: [https://doi.org/10.5281/zenodo.24410608](https://doi.org/10.5281/zenodo.24410608)
- License: CC-BY-4.0
- Version: 2
- Mathesis record: [hardin185765](https://mathesis-omega-research.apps.chrono-ai.fun/papers/hardin185765?version=2)

## How to cite

Haobo Ma, Wenlin Zhang (2026). Hardin's six-column trace recurrence and Barker's generating functions. Mathesis, version 2. https://doi.org/10.5281/zenodo.24410609

## Statement progress

| Statement | Formalization status | Source | Verification basis |
|---|---|---|---|
| Theorem (s1) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/66c49bfe9a1295ceea872b6e6a1d8146fb351237/D5/S3/Combinatorics/TraceAvoidingArrays/HardinA185765Recurrence.lean) | No public receipt |
| Lemma (s2) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/66c49bfe9a1295ceea872b6e6a1d8146fb351237/D5/S3/Combinatorics/TraceAvoidingArrays/HardinA185765Recurrence.lean) | No public receipt |
| Corollary (s3) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/66c49bfe9a1295ceea872b6e6a1d8146fb351237/D5/S3/Combinatorics/TraceAvoidingArrays/HardinA185765Recurrence.lean) | No public receipt |
| Corollary (s4) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/66c49bfe9a1295ceea872b6e6a1d8146fb351237/D5/S3/Combinatorics/TraceAvoidingArrays/HardinA185765Recurrence.lean) | No public receipt |
| Corollary (s5) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/66c49bfe9a1295ceea872b6e6a1d8146fb351237/D5/S3/Combinatorics/TraceAvoidingArrays/HardinA185765Recurrence.lean) | No public receipt |
| Corollary (s6) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/66c49bfe9a1295ceea872b6e6a1d8146fb351237/D5/S3/Combinatorics/TraceAvoidingArrays/HardinA185765Recurrence.lean) | No public receipt |
| Corollary (s7) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/66c49bfe9a1295ceea872b6e6a1d8146fb351237/D5/S3/Combinatorics/TraceAvoidingArrays/HardinA185765Recurrence.lean) | No public receipt |

## Contributions

Original authors are listed above. Formalization contributors and attribution are retained in `formalization/nodes.json`; repository pull requests do not confer verification or credit. Submit formalization attempts through the Mathesis attempt path described in [CONTRIBUTING.md](CONTRIBUTING.md).
