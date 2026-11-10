# IRR method classification: data-cashflows-mixed-irr

50 runs: 5 models × 2 effort levels (low, high) × 5 runs. Each `runs/<model>_<effort>_<n>/method.py` was classified from its executable code only. Per-run results are in the new columns of `summary.csv`.

## Classification scheme

| Column | Values | Meaning |
|---|---|---|
| `method` | bisection, newton, secant, brent, hybrid, library, other | Root-finding approach that actually runs. **hybrid** means two or more methods, each reachable at runtime. **library** means the root-find is handed to a library function. |
| `method_details` | free text | For hybrid: the methods combined. For library: the function used. For bisection: how the bracket is found (grid range, spacing, step count). Also records the literal output token when it is not `nan`. |
| `on_failure` | nan, raise, endpoint, last_iterate, none | What is output when no root is found. In practice this is always a missing-value marker (`nan`, `NaN`, `NA` or an empty line); these are all recorded as `nan`. |
| `multiple_roots` | all, smallest, largest, closest to X, default, other | Which root is reported when there is more than one. **default** means the selection is left to the library function. |
| `comments_match` | yes, no, no_comments | Whether the comments and docstrings describe what the code actually does. |

Notes:
- `numpy.roots` (polynomial root-finding in x = 1+r or v = 1/(1+r), via companion-matrix eigenvalues) counts as **library**. If those roots are then refined with Newton or `brentq`, the run counts as **hybrid**.
- Every bisection script uses the same pattern: scan a fixed grid of rates for sign changes in NPV, then bisect each bracket. No script uses an expanding bracket.
- `numpy_financial.irr` (v1.1.0) also uses `numpy.roots`. It returns `nan` when there is no real root. When there are several, it chooses by a sign heuristic and then takes the root closest to zero.
- gemini-3.8-flash high runs 3 and 4 include a re-implementation of `npf.irr` using `numpy.roots`, but it only runs if importing `numpy_financial` fails. `numpy_financial` is installed here, so they are classified as library.

## Methods by agent

| Model | Effort | bisection | library | hybrid |
|---|---|---|---|---|
| claude-haiku-5-5 | low | 5 | 0 | 0 |
| claude-haiku-5-5 | high | 2 | 3 | 0 |
| claude-sonnet-5-5 | low | 4 | 1 | 0 |
| claude-sonnet-5-5 | high | 1 | 3 | 1 |
| claude-opus-5-5 | low | 3 | 2 | 0 |
| claude-opus-5-5 | high | 0 | 1 | 4 |
| gemini-3.8-flash | low | 0 | 5 | 0 |
| gemini-3.8-flash | high | 0 | 5 | 0 |
| gemini-4-argon | low | 0 | 5 | 0 |
| gemini-4-argon | high | 0 | 5 | 0 |
| **Total** | | **15** | **30** | **5** |

No run used newton, secant or brent on its own, or a method classed as other.

## Agents by method

| Method | Detail | Runs (model effort: run numbers) |
|---|---|---|
| bisection | grid scan + bisection | haiku low: 1–5; haiku high: 2, 3; sonnet low: 1, 2, 3, 5; sonnet high: 3; opus low: 1, 2, 5 |
| library | `numpy.roots` | haiku high: 1, 4, 5; sonnet low: 4; sonnet high: 1, 4, 5; opus low: 3, 4; opus high: 2 |
| library | `numpy_financial.irr` | gemini-3.8-flash low & high: 1–5; gemini-4-argon low & high: 1–5 |
| hybrid | `numpy.roots` + Newton polish | opus high: 1, 3, 4, 5 |
| hybrid | `numpy.roots` + `scipy.optimize.brentq` polish | sonnet high: 2 |

## Multiple roots, failure handling, comments

| Model | multiple_roots | on_failure | comments_match |
|---|---|---|---|
| claude-haiku-5-5 | closest to 0 (8), smallest (2: low 3, low 5) | nan (10) | yes (10) |
| claude-sonnet-5-5 | closest to 0 (9), other (1: low 3) | nan (10; 9 as an empty line) | yes (9), no (1: low 3) |
| claude-opus-5-5 | closest to 0 (10) | nan (10) | yes (10) |
| gemini-3.8-flash | default (10) | nan (10) | no_comments (10) |
| gemini-4-argon | default (10) | nan (10) | no_comments (10) |

- **sonnet low 3** is the only mismatch. Its comment says it returns "the root with the largest rate", but the code returns the smallest non-negative root, or the most negative root if there is no non-negative one.
- **haiku low 5** stops at the first bracket it finds. **haiku low 3** finds all roots but returns the first. Both therefore report the smallest root in their search range.
- No script raises an exception or returns a bracket endpoint on failure. Bisection loops run a fixed number of iterations, and Newton polishing keeps its last iterate. Neither of those is a failure path that can be reached.
