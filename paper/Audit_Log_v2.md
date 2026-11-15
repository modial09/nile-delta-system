# Audit log, Problem One, version two

Auditor role: skeptical senior reviewer, independent of the version one build. Date of audit: 12 November 2026. Scope: Problem One only (allocation). Files audited: docs/design.md, docs/problem_statement.md, src/allocation_model.py, data/SOURCES.md, paper/Results_Note_v1.md, data/processed/run_v1_output.txt, and the raw OWID files in data/raw. Version one files were not modified. Version two code lives in src/allocation_model_v2.py and its run in data/processed/run_v2_output.txt.

## Iteration 1: promise inventory

Every promise the design and problem statement make for Problem One, marked kept, bent, or broken in version one.

1. Two stage stochastic linear program in extensive form over three scenarios. KEPT.
2. Stage two decision variables include the shortfall against the ideal water requirement. BENT. Shortfall is implicit in the delivered water variable; no explicit shortfall variable exists. Substance kept, form changed.
3. Objective carries a penalty on water shortfall that reflects yield loss. BENT. Yield loss lives inside the production function rather than in a separate penalty term. Economically equivalent here, but it is not the structure the design describes.
4. Land constraint per district. KEPT.
5. Total water per scenario at or below the scenario budget. BENT. The code imposes district budgets allocated by land share, so water can never move between districts. The design contradicts itself on this point: its dual section names district water constraints, its constraint list names a scenario total. The code followed the dual reading and declares the simplification.
6. Food security floor on staple production. KEPT as a constraint, with a caveat that becomes the largest finding of this audit: the floor level of 90 percent is a declared choice, and the headline depends on it more than on anything else (see Iteration 4).
7. Water per planting at or below its agronomic requirement. KEPT.
8. District shadow prices reported as the water value map, a primary output. BENT. Extraction code is correct (verified twice, see Iteration 2), but version one reported probability weighted duals while its prose described conditional values, and its cross scenario comparison was wrong as a result.
9. Expected value of perfect information reported. KEPT. EGP 10,369,763,357, reproduced exactly.
10. Value of the stochastic solution reported. BROKEN as specified. Version one reports no VSS number. Its reason is principled (the average year plan breaks the food floor in the low scenario, so its floored score does not exist), but the design promised a number and the paper should either produce one under stated rules or amend the design.
11. Scenario parameters produced by the forecasting module, means and spread from backtests. BROKEN in version one. The module is not built. Scenario budgets are scaled by judgment factors 0.85 and 1.08 and probabilities 0.25, 0.50, 0.25 are declared judgment. Disclosed in the note and in SOURCES.md.
12. Baseline test against the actual cropping pattern, same prices, same water. BENT. The baseline is the real national crop mix placed uniformly on an illustrative district land base. The comparison binds at crop mix level only. Disclosed.
13. Falsification rule: the optimised allocation must beat the actual pattern in margin per unit of water by a meaningful margin. BENT. It passes at 11.52 percent under the 90 percent food floor. At full staple protection it passes only at 2.55 percent on the per cubic metre metric and fails outright on total margin. The claim as headlined is floor dependent.
14. Backtest on earlier years. BROKEN in version one. Not run. It belongs to the forecasting timeline in the design schedule, but the testing plan lists it without that qualification.
15. Stress tests at 10 and 20 percent water cuts. KEPT, and the 20 percent case is reported honestly (food breach sized, margin flagged as not comparable).
16. Sensitivity analysis: prices and costs moved across plausible bands, shadow price stability reported. BROKEN in version one. Explicitly deferred in the note. Run in this audit (Iterations 3 and 5) and now part of the version two pipeline. Shadow price stability under the moved parameters is still not tabulated; logged as remaining work.
17. Crop coverage implied by the problem statement, including cotton, the Delta crop with the strongest water claim. BROKEN. Cotton is absent because the mirror carries no series. Disclosed.
18. Every number in the paper traces to a file and a transformation. BENT. Yields, areas and the crop mix trace to files in data/raw. All prices except wheat, all costs, all water requirements, the district land base, the district yield multipliers and the scenario budgets are constants declared in code. One auditable place, but not files.

Tally: kept 6, bent 7, broken 5.

## Iteration 2: reproduction and code audit

Reran src/allocation_model.py end to end. The full printed output is byte identical to data/processed/run_v1_output.txt. Headline reproduces exactly: optimised expected margin EGP 130,437,402,453, baseline EGP 118,106,628,859, gain EGP 12,330,773,594, 10.44 percent. Runtime about 2 seconds. The arithmetic of version one is trustworthy. Its framing is where the faults sit.

Formulation checks:

1. Production function. Production equals yield times (1 minus ky) times hectares plus yield times ky over requirement times water delivered. At full water it returns full yield; the algebra is correct. For response factors above one (rice 1.20, maize 1.25, potatoes 1.10) the form extrapolates below zero once the shortfall share passes 1 over ky. In the main version one solution this region is never entered: the only zero water plantings are sugar beet (factor exactly 1.00, production exactly zero), and every rice, maize and potato planting is fully watered in every scenario. But see item 3 below: the region IS entered in the 20 percent stress run.
2. Plan anatomy, previously unreported. Total full water demand of the optimised plan is exactly 11.0000 billion cubic metres, equal to the expected scenario budget to five significant figures, and equal district by district (demand to budget ratio 1.000 in all eight districts). In the low scenario the shortfall is 1.650 billion cubic metres, and total sugar beet water demand is 1.650 billion cubic metres: the model covers the entire dry year shortfall by delivering zero water to all 317,308 hectares of sugar beet. Every other planting is fully watered in every scenario. The version one note describes the plan crop by crop and never mentions the write off.
3. Negative production in the 20 percent stress run. With the food floor dropped by the fallback path, the version one solver reports negative production on 8 rice plantings, the largest about minus 14,586 tons (Beheira, low scenario). Negative harvest is revenue negative, so the solver uses it to shed staple output it is forced to plant. Any number downstream of that run in version one (staple fall 6,173,477 tons, no floor margin EGP 143.56 billion) is computed partly by a physically impossible device.
4. Baseline evaluation. The baseline is evaluated without the food floor, which is correct for describing the status quo, and under identical prices, costs and budgets, as the design requires. One asymmetry deserves note: at a 100 percent floor the optimised plan must keep a promise in every scenario that the baseline itself breaks in the dry year. The strict floor run therefore charges the plan for insurance the status quo does not buy. Both readings are reported in the version two note.
5. Duals. Brute force check inside the stochastic model: raising the Dakahlia expected scenario budget by 1 percent raises expected margin by exactly the reported raw dual, 4.961 EGP per cubic metre. Extraction is correct. Version one's own check compared duals inside the deterministic model (13.681 EGP per cubic metre), a model whose duals appear nowhere in its results. The verification verified code, but on the wrong model, and the note implied more than that.
6. Dual units. The extensive form objective weights scenario revenue by probability, so each scenario water dual is a probability weighted value. Conditional values (raw dual divided by scenario probability) are: expected year EGP 8.02 to 10.21 per cubic metre, low year EGP 33.03 to 37.90, high year zero. The version one sentence claiming the dry year value roughly doubles the normal year value compares weighted numbers; the conditional ratio is about 3.8. Wrong claim, now corrected in the note and in the version two output tables.
7. Water value map ranking. Spearman rank correlation between the district shadow prices and the declared district yield multipliers is exactly 1.000. District budgets are forced proportional to land, so water per hectare is identical across districts and the multipliers are the only district level signal in the model. The ranking is the assumption table restated. Levels still carry information; the order does not, until CAPMAS.
8. Information values. The wait and see value is built from deterministic solves that include the food floor, consistently with the recourse problem. EVPI is sound. The version one code silently substituted zero for any wait and see solve that returned a non optimal status; all three statuses were optimal here, so no number changed, but the silence is a defect. Version two records and reports the statuses.
9. Environment note. requirements.txt lists scipy, but scipy is not installed in the project venv (import failed during this audit). Nothing in Problem One needs it today; the forecasting module will. Logged so the gap is found now, not in week five.

## Iteration 3: price sensitivity, as the design promised

Per hectare margins at national yield and full water identify the two highest margin crops: rice at EGP 104,473 per hectare and potatoes at EGP 101,607 per hectare (sugar beet third at EGP 94,468). Both headline prices are illustrative, which is what makes them the right attack surface. In every run below, the baseline is reevaluated under the same moved prices, as the design requires.

1. Rice price times 0.8: gain EGP 10,549,887,732, 9.46 percent.
2. Rice price times 1.2: gain EGP 12,329,287,498, 9.75 percent.
3. Potatoes price times 0.8: gain EGP 15,801,096,384, 13.91 percent. The gain rises when the potato price falls, because the baseline plants potatoes everywhere at the national mix, including low multiplier districts, while the optimised plan concentrates them and can retreat.
4. Potatoes price times 1.2: gain EGP 13,577,948,774, 11.07 percent.
5. Both prices times 0.8: gain EGP 14,145,757,955, 13.21 percent.
6. Both prices times 1.2: gain EGP 13,990,482,501, 10.68 percent.

Verdict: the headline at the 90 percent floor is robust to the two largest illustrative prices. Band across these runs: 9.46 to 13.91 percent.

## Iteration 4: the food floor curve

The floor is the dial the headline hangs on. Baseline margin is EGP 118,106,628,859 in all rows (the baseline carries no floor).

1. Floor at 0.90 of current staple production: optimised EGP 130,437,402,453. Gain EGP 12,330,773,594, 10.44 percent. Per cubic metre gain 11.52 percent.
2. Floor at 0.95: optimised EGP 123,466,268,775. Gain EGP 5,359,639,916, 4.54 percent.
3. Floor at 1.00, held in every scenario: optimised EGP 114,351,765,691 on 10.093 billion cubic metres. Total margin gain is negative: minus EGP 3,754,863,168, minus 3.18 percent. Margin per cubic metre still leads, EGP 11.33 against EGP 11.05, plus 2.55 percent, because the strict plan uses less water. The falsification rule in its stated per cubic metre form technically passes; the margin claim a reader takes from the headline fails.
4. Feasibility: the 1.00 floor is feasible in all three scenarios (deterministic solves all optimal), and the highest floor share feasible in all scenarios is about 1.039. The negative result at 1.00 is economics, not infeasibility.
5. Decomposition: of the EGP 12.33 billion headline at the 0.90 floor, EGP 16,085,636,762 is created by relaxing the guarantee from 1.00 to 0.90, and the reallocation component at full protection is minus EGP 3,754,863,168. The staple trade is worth more than the entire headline.
6. Fairness reference point: the current pattern delivers about 94.5 percent of its full water staple production in expectation. A guarantee set at the level the status quo actually delivers sits between rows 1 and 2 of this curve, near the 4.54 percent row.

## Iteration 5: cost and budget sensitivity

1. All production costs times 0.8: gain EGP 11,811,891,481, 8.94 percent.
2. All production costs times 1.2: gain EGP 12,862,094,410, 12.35 percent.
3. Potato production cost times 1.2 alone: gain 11.61 percent. Times 0.8 alone: 10.46 percent. The single most uncertain cost barely moves the result, because planting adjusts.
4. All scenario water budgets times 0.95: gain EGP 11,615,727,163, 10.37 percent.
5. All scenario water budgets times 1.05: gain EGP 14,435,404,728, 11.75 percent.

Verdict: the calibrated budget level (set just under baseline demand, the choice SOURCES.md declares) is not what manufactures the gain. The floor is.

## Iteration 6: fixes applied in version two

All fixes are in src/allocation_model_v2.py. src/allocation_model.py is untouched, and data/processed/run_v1_output.txt is untouched.

1. Production floor constraint. Every planting and scenario now carries production at or above zero, fencing the linear yield response form at the point where the agronomy says production stops. Effect on the main run: none (the fence does not bind; headline reproduces to the pound). Effect on the 20 percent stress run: negative production is gone; staple output at the cut is 6,160,529 tons against version one's 6,173,477, and the no floor margin is EGP 143.39 billion against version one's EGP 143.56 billion. Small numbers, impossible physics removed.
2. Dual reporting in two labelled units. extract_shadow_prices now also returns the conditional value per scenario, and the run prints both tables with their units in words.
3. Water coverage table. The run prints delivered share of requirement by crop and scenario. The sugar beet write off in the low scenario now appears in the standard output.
4. Sensitivity as pipeline. sensitivity_report runs the price swings, cost swings, budget scalings and the floor curve on every version two run, and prints the table the note quotes.
5. Stochastic dual verification. dual_check_stochastic verifies the reported duals inside the model that produced them. Dakahlia expected: reported 4.961, brute force 4.961.
6. Wait and see status reporting. information_values records each deterministic status and the run warns if any is not optimal, replacing the silent zero.

## What remains weak

1. The money is still illustrative. Four of five prices, all costs and all water requirements are declared midpoints. The gain band of 9 to 14 percent is a statement about this parameter family, not about Egypt. The FAOSTAT producer price pull is the single highest value next step.
2. The district layer is still assumed: land base, yield multipliers and budgets by land share. The water map ranking is an echo of the multipliers (Spearman 1.000) and will stay one until CAPMAS lands.
3. The baseline is still the national mix, not the district pattern, so the falsification test binds at mix level only.
4. Cotton is still missing, and with it the crop whose water politics matter most in the Delta.
5. VSS still has no number. The honest treatment is in the note, but the design promised a number; either the design must be amended in writing or a floored scoring convention for infeasible plans must be defined and the number produced.
6. The linear yield response is still linear. The fence at zero fixed the impossible region, not the shape. Real response curves bend, and the dry year results lean on the shape.
7. Scenario probabilities and scaling remain judgment, untested by any hydrology pull.
8. Shadow price stability across the sensitivity runs is still not tabulated; the design asks for it and this audit priced margins, not duals, under moved parameters.

## Auditor verdict

The version one model is well built and its arithmetic is exact. Its reporting was not at the same standard: a headline that belongs to a policy choice was presented as a property of the allocation, a water value map was quoted in units its prose did not describe, and the plan's defining dry year move went unmentioned. Version two keeps the model, fences its one impossible region, and rewrites the claims at the level the evidence supports: a gain of roughly nine to fourteen percent if a planner accepts a ninety percent staple guarantee, about four and a half percent at the protection level the current pattern actually delivers, and no gain at full protection. The next work is data, in this order: FAOSTAT prices, CAPMAS districts, Ministry quota, hydrology, extension values.

## Correction, 12 November 2026

An independent recheck of the noon set on 12 November 2026 found one material framing error in the decision section of paper/Results_Note_v2.md. The note said the current crop mix earns what it earns largely because it protects staple output at full current levels in every year, wet or dry. That sentence contradicted the note, in its own staple section, and this audit: the current pattern delivers about 94.5 percent of its full water staple output in expectation and falls short in a dry year. The sentence was corrected in the note on 12 November 2026 to state that the current pattern falls short in a dry year, and that an optimised plan held to a full guarantee in every year must keep a promise the current pattern itself does not keep. No number in the note changes.
