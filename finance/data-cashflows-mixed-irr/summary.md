# IRR method classification

I classified all 50 `runs/*/method.py` scripts by their executable code only. Comments and docstrings were used only to fill in `comments_match`. The results are in the last four columns of `summary.csv`. The earlier free-text `method` column has been kept and renamed `method_description`.

## Definitions

| field | values | meaning |
|---|---|---|
| `method` | bisection, newton, secant, brent, hybrid, library, other | How the root is found. **hybrid** means two or more methods, each of which actually runs. **library** means a library function does the root-finding. |
| `method_details` | free text | For library: the function used. For hybrid: the methods combined. For bisection: the grid and bracketing scheme, plus which root is reported when there are several. |
| `on_failure` | nan, raise, endpoint, last_iterate, none | What is written when there is no root. |
| `comments_match` | yes, no, no_comments | Whether the comments and docstrings correctly describe the method that runs. |

Classification notes:
- **`numpy.roots` counts as library.** It solves NPV = 0 as a polynomial in 1/(1+r) or 1+r, using the eigenvalues of the companion matrix. `numpy_financial.irr` does the same thing internally.
- **The two hybrids are different.** In both, a `numpy.roots` result is refined afterwards: by Newton steps in 4 Opus runs, and by `scipy.optimize.brentq` in Sonnet high_2. I ran Sonnet high_2 and confirmed `brentq` is called (16 times on this data).
- **Two Gemini Flash runs have unreachable fallbacks.** Runs high_3 and high_4 include an `np.roots` fallback that only runs if importing `numpy_financial` fails. `numpy_financial` 1.1.0 is installed, so the fallback never runs and these are classified as library `numpy_financial.irr`.
- **Every script writes a missing value when there is no root,** so `on_failure` is `nan` for all 50. The token differs: `nan`/`NaN`, `NA`, or an empty line. No script raises an error or returns an endpoint or last iterate. Each bisection runs a fixed number of iterations on a bracket that has a sign change. The Newton polishing stops quietly at its last iterate, but this does not affect the no-root case.
- **One comment mismatch.** In Sonnet low_3 the comment says the script returns "the root with the largest rate", but the code returns the *smallest* non-negative root, or failing that the lowest root.
- **A false claim that doesn't change the verdict.** Several runs (Haiku high_5, Opus high_1/2/3/5) say that "closest to zero" is the numpy_financial convention. It isn't: on line 19 npf gives 1.419227 and closest-to-zero gives −0.519384. Their description of their own method is accurate, so they are still marked `yes`.

## Method by agent (number of runs)

| agent | effort | bisection | library: npf.irr | library: numpy.roots | hybrid: roots+Newton | hybrid: roots+brentq |
|---|---|---|---|---|---|---|
| claude-haiku-5-5 | high | 2 | 0 | 3 | 0 | 0 |
| claude-haiku-5-5 | low | 5 | 0 | 0 | 0 | 0 |
| claude-opus-5-5 | high | 0 | 0 | 1 | 4 | 0 |
| claude-opus-5-5 | low | 3 | 0 | 2 | 0 | 0 |
| claude-sonnet-5-5 | high | 1 | 0 | 3 | 0 | 1 |
| claude-sonnet-5-5 | low | 4 | 0 | 1 | 0 | 0 |
| gemini-3.8-flash | high | 0 | 5 | 0 | 0 | 0 |
| gemini-3.8-flash | low | 0 | 5 | 0 | 0 | 0 |
| gemini-4-argon | high | 0 | 5 | 0 | 0 | 0 |
| gemini-4-argon | low | 0 | 5 | 0 | 0 | 0 |
| **total** | | **15** | **20** | **10** | **4** | **1** |

## Agent by method

| method | details | runs |
|---|---|---|
| library | `numpy_financial.irr` | gemini-3.8-flash (all 10), gemini-4-argon (all 10) |
| library | `numpy.roots`, closest to zero | claude-haiku-5-5 (high_1, high_4, high_5), claude-sonnet-5-5 (high_1, high_4, high_5, low_4), claude-opus-5-5 (high_2, low_3, low_4) |
| hybrid | `numpy.roots` + Newton polish | claude-opus-5-5 (high_1, high_3, high_4, high_5) |
| hybrid | `numpy.roots` + `scipy.optimize.brentq` polish | claude-sonnet-5-5 (high_2) |
| bisection | grid scan, bisect every sign change, closest to zero | claude-haiku-5-5 (high_2, high_3, low_1, low_2, low_4), claude-sonnet-5-5 (high_3, low_1, low_2, low_5), claude-opus-5-5 (low_1, low_2, low_5) |
| bisection | grid scan, lowest root | claude-haiku-5-5 (low_3; low_5 stops at the first sign change) |
| bisection | grid scan, lowest non-negative root | claude-sonnet-5-5 (low_3) |

No run uses plain newton, secant, brent or other as its main method. Every bisection run uses a fixed grid scan. None uses an expanding bracket.

## comments_match

| agent | yes | no | no_comments |
|---|---|---|---|
| claude-haiku-5-5 | 10 | 0 | 0 |
| claude-opus-5-5 | 10 | 0 | 0 |
| claude-sonnet-5-5 | 9 | 1 (low_3) | 0 |
| gemini-3.8-flash | 0 | 0 | 10 |
| gemini-4-argon | 0 | 0 | 10 |

## Observations
- **Gemini:** always calls `numpy_financial.irr` and writes no comments.
- **Claude:** never uses npf. Low-effort runs mostly bisect a grid (12 of 15). High-effort runs mostly solve the polynomial with `numpy.roots` (12 of 15). The only hybrids are high-effort runs, where Opus polishes the roots with Newton steps and Sonnet with `brentq`.
