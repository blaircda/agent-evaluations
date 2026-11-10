# IRR method classification

All 50 runs produced a `method.py`. Each script is classified from its executable code only. Comments and docstrings are used only for the `comments_match` column. Results are in the new columns of `summary.csv`.

## Classification scheme

| column | values | meaning |
|---|---|---|
| `method` | `bisection` \| `newton` \| `secant` \| `brent` \| `hybrid` \| `library` \| `other` | Root-finder used to solve NPV(r) = Σ c_t/(1+r)^t = 0. `hybrid` = two or more methods, each reachable at runtime. `library` = the root-find is handed to a library. |
| `method_details` | free text | `hybrid`: the methods combined. `library`: the function called. Otherwise, distinguishing features (fixed vs expanding bracket, initial guess, whether the bracket's sign is checked). |
| `on_failure` | `nan` \| `raise` \| `endpoint` \| `last_iterate` \| `none` | What the script outputs when no root is found or iterations run out. |
| `comments_match` | `yes` \| `no` \| `no_comments` | Whether the comments/docstrings that describe the method match the code. |

Notes on how edge cases were classified:
- **`numpy.roots`** (solving NPV as a polynomial in 1+r or 1/(1+r)) is classified as `library`.
- **gemini-3.8-flash high_2** is `hybrid`: if `numpy.roots` finds no positive real root, the code falls through to Newton, so Newton can run even with numpy installed. **gemini-3.8-flash high_4** is `library`: its Newton code is defined only in the `except ImportError` branch, so it never runs when numpy is installed.
- **`nan`** includes three Sonnet runs (high_1, high_2, high_4) that return `None` and write an **empty line** in place of a value.
- **`endpoint`**: the script does bisection without checking for a sign change, so when there is no root it converges to an end of the bracket. claude-haiku-5-5 high_4 also doubles its upper bound with no cap, so it would loop forever if NPV never turns negative.
- **gemini-4-argon low_5**: its comment says "Newton-Raphson with bisection fallback", but the code is pure bisection, so `comments_match = no`. This is the only mismatch.

## Method by agent (runs; n = 5 per agent)

| agent | bisection | newton | library | hybrid |
|---|---|---|---|---|
| claude-haiku-5-5 / low | 5 | 0 | 0 | 0 |
| claude-haiku-5-5 / high | 5 | 0 | 0 | 0 |
| claude-sonnet-5-5 / low | 5 | 0 | 0 | 0 |
| claude-sonnet-5-5 / high | 5 | 0 | 0 | 0 |
| claude-opus-5-5 / low | 5 | 0 | 0 | 0 |
| claude-opus-5-5 / high | 5 | 0 | 0 | 0 |
| gemini-3.8-flash / low | 0 | 0 | 5 | 0 |
| gemini-3.8-flash / high | 0 | 0 | 4 | 1 |
| gemini-4-argon / low | 3 | 2 | 0 | 0 |
| gemini-4-argon / high | 4 | 1 | 0 | 0 |
| **total** | **37** | **3** | **9** | **1** |

No runs used `secant`, `brent` (hand-written) or `other`.

Bisection bracket style: 14 runs use an expanding bracket (1 Haiku, 6 Sonnet, 7 Opus) and 23 use a fixed bracket. All gemini-4-argon bisection runs use a fixed bracket with no sign check.

## Agent by method

| method | runs | agents (runs) | details |
|---|---|---|---|
| `bisection` | 37 | claude-haiku-5-5 low (5), high (5); claude-sonnet-5-5 low (5), high (5); claude-opus-5-5 low (5), high (5); gemini-4-argon low (3), high (4) | fixed bracket ×23, expanding ×14 |
| `library` | 9 | gemini-3.8-flash low (5), high (4) | `numpy.roots` ×8, `scipy.optimize.brentq` ×1 (low_1) |
| `newton` | 3 | gemini-4-argon low (2), high (1) | analytic derivative; x0 = 0.1 ×2, 0.5 ×1 |
| `hybrid` | 1 | gemini-3.8-flash high (1) | `numpy.roots` + Newton |

## Failure behaviour by agent

| agent | raise | nan | endpoint | last_iterate |
|---|---|---|---|---|
| claude-haiku-5-5 / low | 5 | 0 | 0 | 0 |
| claude-haiku-5-5 / high | 4 | 0 | 1 | 0 |
| claude-sonnet-5-5 / low | 0 | 2 | 3 | 0 |
| claude-sonnet-5-5 / high | 1 | 4 | 0 | 0 |
| claude-opus-5-5 / low | 0 | 3 | 2 | 0 |
| claude-opus-5-5 / high | 4 | 1 | 0 | 0 |
| gemini-3.8-flash / low | 3 | 2 | 0 | 0 |
| gemini-3.8-flash / high | 3 | 1 | 0 | 1 |
| gemini-4-argon / low | 0 | 0 | 3 | 2 |
| gemini-4-argon / high | 0 | 0 | 4 | 1 |
| **total** | **20** | **13** | **13** | **4** |

## Comments match code, by agent

| agent | yes | no | no_comments |
|---|---|---|---|
| claude-haiku-5-5 / low | 0 | 0 | 5 |
| claude-haiku-5-5 / high | 1 | 0 | 4 |
| claude-sonnet-5-5 / low | 0 | 0 | 5 |
| claude-sonnet-5-5 / high | 2 | 0 | 3 |
| claude-opus-5-5 / low | 0 | 0 | 5 |
| claude-opus-5-5 / high | 3 | 0 | 2 |
| gemini-3.8-flash / low | 4 | 0 | 1 |
| gemini-3.8-flash / high | 3 | 0 | 2 |
| gemini-4-argon / low | 2 | 1 | 2 |
| gemini-4-argon / high | 0 | 0 | 5 |
