# Acceptance tests

These are proposed execution requirements. They have not been run on the revised project by preparing this handoff. Owners and exact contracts are in stages.json. Numerical tolerances must be specified in the unit of each quantity before interpreting a difference; arbitrary tight rounding is not validation.

| ID | Stages | Owner | Required evidence |
|---|---|---|---|
| A01 | S1 | Research lead | Inventory/hashes identify the generating model version; every headline has a source/calculation/status. |
| A02 | S2 | Data analyst | Unique keys, join cardinality, missingness, unit conversions, and source totals reconcile with original records; exceptions are explicit. |
| A03 | S2,S3 | Hydrology and economic reviewers | Dates, water boundaries, physical calendar occupancy, unmodeled crop reserves, and market/reference bases are coherent or explicitly bounded. |
| A04 | S3,S4 | OR/verification analyst | Information timeline and code enforce nonanticipativity; forecast preprocessing/selection respect the historical cutoff. |
| A05 | S4 | Verification analyst | Independent replay of expected values, costs, floor opportunity costs, capacity, and comparison definitions; exact solver status/gap retained. |
| A06 | S4 | Verification analyst | Hand-solvable fixture, feasible plan residuals, valid production/abandonment costs, and applicable objective/capacity monotonicity checks. |
| A07 | S4 | Verification analyst | Baseline 60.12%/no-floor contradiction resolved with consistent definitions and outputs, or claim withdrawn. |
| A08 | S4 | Verification/hydrology analyst | Sampling horizon, adaptive policy, dependence assumptions, and distributional uncertainty are explicit; sample frequencies are not misrepresented as annual reliability. |
| A09 | S4,S6 | Verification/data analyst | Relaxation duals, full-MIP finite increments, LP/MIP differences, and uncertainty in rankings are labeled correctly. |
| A10 | S5 | Editor/Mohamed | Main memo, <=300-word summary, appendix, and contribution account use accepted records and truthful authorship; material caveats remain with claims. |
| A11 | S6 | UX/data analyst | Every chart/control maps to an actual run; unsupported combinations, infeasibility, errors, stale/missing values, and units behave honestly. |
| A12 | S6 | UX reviewer/Mohamed | Observed/modeled/synthetic modes persist; keyboard/mobile/reader checks recorded; prototype remains private until authorized release. |

Gate A depends on A01–A09, with limitations determining whether claims are empirical or illustrative. Gate B depends on the applicable Gate A scope and A10–A12. External specialist review complements the numerical evidence. A separate model vendor is not equivalent to an Egyptian irrigation expert.
