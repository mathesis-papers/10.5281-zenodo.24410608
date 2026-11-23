# Hardin's six-column trace recurrence and Barker's generating functions

Haobo Ma — ChronoAI Pte Ltd, Singapore  
Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore

## Results

The note proves the recurrence in [OEIS A185765](https://oeis.org/A185765), revision 9, FORMULA (October 3, 2025), for every index `n >= 13`. It fails at `n = 12`, with residual `-4160`. Its reduced generating-function denominator has degree nine, proving that no rational-coefficient homogeneous recurrence of smaller order holds eventually.

The same transfer argument proves the empirical recurrences and Colin Barker's conjectural generating functions in [A185761](https://oeis.org/A185761), [A185762](https://oeis.org/A185762), [A185763](https://oeis.org/A185763) and [A185764](https://oeis.org/A185764), together with Barker's two-column closed form. Their recurrence starting indices are 3, 4, 7 and 10, respectively. The formulas retain their attribution to Hardin and Barker.

For [A185769](https://oeis.org/A185769), transposition proves symmetry and transfers these column results to rows. Every count is divisible by eight, and every fixed row or column has a rational generating function. The particular larger-width recurrences in A185766 and A185768 are outside the stated coverage.

## Build

This is a self-contained LaTeX source with an embedded bibliography. Build with Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively use a standard LaTeX distribution with `geometry`, `amsmath`, `amssymb`, `amsthm`, `booktabs`, `array`, `lmodern` and `hyperref`:

```sh
pdflatex note.tex
pdflatex note.tex
```

No BibTeX step is needed because the bibliography is embedded in `note.tex`.

## Exact finite verification

Python 3.8 or later, standard library only:

```sh
python3 verify.py
```

The output matches `verification.txt`. It checks every six-column state and edge in two encodings, literally enumerates all two-row and three-row arrays, checks all four source examples, and evaluates the finite polynomial identities coordinate by coordinate. It also checks the smaller-width identities, Barker's generating-function numerators, the modular Euclidean algorithm, all 70 displayed A185769 counts and its seven examples. Infinite conclusions follow from the note's written bijection, propagation and algebraic proofs, not from extrapolation of initial terms.

To compare all 200 A185765 terms with their primary table, download [b185765.txt](https://oeis.org/A185765/b185765.txt), then run:

```sh
python3 verify.py --oeis b185765.txt
```

That adds the 200-term comparison and the data-file hash to the output. The downloaded OEIS data retain the [OEIS reuse terms](https://oeis.org/LICENSE) and are not included in this archive.

## Mathematical and formal coverage

The pinned Lean source revision is `66c49bfe9a1295ceea872b6e6a1d8146fb351237`. In the namespace `D5.S3.Combinatorics.TraceAvoidingArrays`:

- [`HardinA185765Transfer.counting_bridge`](https://github.com/the-omega-institute/trureturing/blob/66c49bfe9a1295ceea872b6e6a1d8146fb351237/D5/S3/Combinatorics/TraceAvoidingArrays/HardinA185765Transfer.lean) identifies the literal six-column array cardinality at `n = k+1`, embedded in the integers, with the sum of continuation counts `u k` over the `64^2` row pairs. Inactive row pairs contribute zero.
- [`HardinA185765Recurrence.finite_certificate`](https://github.com/the-omega-institute/trureturing/blob/66c49bfe9a1295ceea872b6e6a1d8146fb351237/D5/S3/Combinatorics/TraceAvoidingArrays/HardinA185765Recurrence.lean) establishes the vector identity `T^5 Q(T) 1 = 0` and the scalar identities `1^T T^k Q(T) 1 = 0` for `k = 3, 4`.
- [`HardinA185765Recurrence.result`](https://github.com/the-omega-institute/trureturing/blob/66c49bfe9a1295ceea872b6e6a1d8146fb351237/D5/S3/Combinatorics/TraceAvoidingArrays/HardinA185765Recurrence.lean) gives the stated recurrence for every `n >= 13`, with natural-number counts embedded in the integers before signed arithmetic.

The six-column generating function and least-order result, smaller-width formulas, transposition, divisibility and fixed-width rationality have the written proofs and finite identities specified in the note. The displayed Lean declarations cover the six-column bridge and recurrence, not those additional consequences.

## Files and license

The source archive contains `note.tex`, this `README.md`, `metadata.json`, `verify.py`, `verification.txt` and their per-file SHA-256 manifest `manifest.json`.

Copyright 2026 Haobo Ma and Wenlin Zhang. The note, original explanatory text and verification code are licensed under Creative Commons Attribution 4.0 International, CC BY 4.0 (`cc-by-4.0`). Linked OEIS entries and Lean files retain their respective source terms.
