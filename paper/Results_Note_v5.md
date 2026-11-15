# Results Note, version 5

Written 15 November 2026 from the version 5 run record: data/processed/run_v5_main.txt, run_v5_caps.txt, run_v5_beet2400.txt, run_v5_wheatproc.txt, run_v5_costsens.txt, run_v5_reservealt.txt, run_v5_robust.txt and run_forecasting_v5.txt, with unrounded values in the results_v5 JSON files. This note supersedes Results_Note_v4_2.md as the current statement of the results. Version 4.1 and its notes stay on disk unchanged as the audited record.

## 1. The basis, in one sentence

Prices are 2025 forecasts from the FAOSTAT farm gate series, observed to 2024 for wheat, maize and potatoes and to 2023 for paddy rice and sugar beet, and costs are official 2022 values, in nominal pounds throughout. Yields are the published district yields of 2020 to 2021, with the forecast band ratios of the 2025 national yield forecasts applied for the low and high yield states. Land binds by season against physical cultivated area with the stated reserve construction. The scenario set is nine: three inflow states from the 1871 to 1970 Aswan record (dry 0.2300, normal 0.4500, high 0.3200; budgets 8.588, 10.502 and 13.434 billion cubic metres on the 11.00 calibration) combined with three price and yield layers weighted 0.25, 0.50 and 0.25, the bands now built at the quartiles of the backtest residuals so the weights and the construction agree. The drought object built from ten year window means carries no probability and appears only as a named stress in Section 6.

Reference tonnage: 12,254,401 tonnes of aggregate wheat, paddy rice and summer maize (wheat 4,617,795; rice 4,086,074; summer maize 3,550,533), computed as observed areas times published district yields. The guarantee floors are shares of this quantity, held in every one of the nine scenarios.

## 2. The frontier

| Level | Expected margin, pounds | Cost against unconstrained | Cost against next lower level |
| --- | --- | --- | --- |
| 0 percent | 559,713,476,348 | 0 | 0 |
| 50 percent | 430,297,336,634 | 129,416,139,714 | 129,416,139,714 |
| 60 percent | 386,417,040,545 | 173,296,435,803 | 43,880,296,089 |
| 70 percent | 340,320,741,667 | 219,392,734,681 | 46,096,298,878 |
| 75 percent | 316,954,235,954 | 242,759,240,394 | 23,366,505,713 |
| 80 percent | 291,102,590,296 | 268,610,886,052 | 25,851,645,658 |
| 85 percent and above | infeasible | | |

The margin optimal plan at every level is tight at its floor within solver tolerance. Smallest headrooms, printed to a thousandth of a tonne in the run log: 0.016 tonnes under the floor tonnage at the 50 percent level, a three way tie across the low layer in the three inflow states; 0.039 under at 60 percent; 0.062 under at 70 percent; 0.024 under at 75 percent; 0.015 over at 80 percent. A headroom below one tonne means tight within tolerance, not exact, and no sentence in this note claims exactness.

The ceiling, the largest share any plan can hold in every scenario, is 82.41 percent (10,099,349 tonnes). Around it: 93.51 percent with no reserve held; 77.67 percent on yields scaled to the forecast national level, a labelled sensitivity; 80.38 percent under the winter first reserve split of Section 9; 79.50 percent under the named crop caps of Section 8. The ceiling does not move with the sugar beet duty at either end of its arbitrated range, nor with the rice response factor at 1.00 or 1.40 around the carried value of 1.20, which remains unverified.

## 3. The historical pattern

Evaluated on the same basis, the pattern Egypt actually plants earns an expected margin of 144,167,922,884 pounds, delivers an expected staple tonnage of 9,270,566 tonnes (75.65 percent of the reference) and a worst scenario delivered tonnage of 7,684,799 tonnes (62.71 percent) under profit seeking recourse. The accounting difference between the optimised unconstrained margin and the pattern margin is 415,545,553,464 pounds, 288.24 percent of the pattern margin. No input is said to have caused any share of that difference.

Tested against the ladder with staple maximising recourse, scenario by scenario, the pattern capacity runs from 8,056,850 tonnes in the dry state at the low layer to 11,392,530 tonnes in the high state at the high layer. The pattern holds the 50, 60 and 65 percent levels in every scenario and fails from 70 percent. This replaces the version 4.1 sentence that the pattern holds no guarantee at any level, which was false on that build own numbers and is withdrawn.

## 4. Market absorption warnings

The fixed prices of this model stop being credible where a plan plants a crop at many times its observed area, and the run prints those warnings at every level. In the unconstrained optimum: winter potatoes at 16.91 times their observed area, summer potatoes at 22.71 times, Nili potatoes at 369.63 times, and no staples planted at all. At the 80 percent floor: winter potatoes 2.81 times, summer potatoes 6.81 times, Nili potatoes 108.91 times. The frontier of Section 2 is therefore the price of the guarantee in the relaxed world, read with Section 8, which prices the same ladder under named caps.

## 5. Water values

The table below is one optimal dual solution of the LP relaxation of the same formulation, computed at the exact floor 0.8231405524 as a share of the reference tonnage, the ceiling share minus 0.001, printed here in full because the ranges are exact only at that floor. These values are marginal duals of the relaxation, conditional on the scenario, in pounds per cubic metre. They are not marginal values of the mixed integer model and they are not prices. Dual solutions are not unique; another optimal solution can carry different governorate values. At this floor the relaxation objective is 273,356,788,636 pounds against the mixed integer objective of 272,969,293,877, a gap of 387,494,759 pounds or 0.142 percent. Water binds in all eight governorates in every scenario printed.

| Scenario | Range across governorates | Lowest | Highest |
| --- | --- | --- | --- |
| Dry inflow, expected layer | 76.32 to 91.31 | Damietta | Kafr El Sheikh |
| Normal inflow, expected layer | 24.45 to 77.07 | Damietta | Qalyubia |
| High inflow, expected layer | 18.05 to 44.94 | Gharbia | Dakahlia |
| Dry inflow, low layer | 826.44 to 961.74 | Qalyubia | Dakahlia |

## 6. Stress runs, capacity and choice side by side

At budgets scaled to 0.90: maximum staple capacity 9,295,584 tonnes (75.86 percent of the reference); the profit objective chooses a margin of 520,907,656,409 pounds and plants no staples. At 0.80: capacity 8,491,820 tonnes (69.30 percent); profit choice 476,620,802,204 pounds, no staples. A reader who reports only one of the two numbers in each pair misleads.

Drought stress, named and without probability: at the drought budget of 9.580 billion cubic metres, the lowest ten year window mean of the record, with expected prices and yields, maximum staple capacity is 11,104,798 tonnes (90.62 percent of the reference) and the profit choice earns 502,602,629,209 pounds with no staples planted. These are single state values at a budget wetter than the dry state budget; the binding state for every floor remains the dry state.

## 7. Information values at the 80 percent level

True mean budget: 11.0000 billion cubic metres, the probability weighted mean of the three state budgets. Recourse value 291,102,590,296 pounds. Wait and see value 304,561,061,130 pounds. EVPI 13,458,470,835 pounds. The plan built on true means cannot hold the 80 percent floor in 7 of the 9 scenarios, so no standard VSS exists for this benchmark and none is reported. On one consistent penalised definition, penalty 25,000 pounds per tonne of shortfall on both sides: penalised stochastic optimum 346,643,462,500 pounds; penalised expected value of the true mean plan 270,712,423,014 pounds; penalised VSS 75,931,039,486 pounds. This replaces the version 4.1 figure of 7,607,863,594, which paired the hard floor optimum with a penalised evaluation and is withdrawn as a definition, not only as a number.

## 8. The capped ladder

Under the named constraints (wheat 0.50, rice 0.35, maize 0.40 in each season, sugar beet 0.30, potatoes 0.15 of district physical land in each season, a modelling device carried from earlier versions), the ladder reads: unconstrained 294,692,290,467; 50 percent 291,680,482,929; 60 percent 286,069,274,763; 70 percent 272,681,269,682; 75 percent 262,025,472,882; 80 percent infeasible, because the capped ceiling is 79.50 percent. The cost of the 75 percent guarantee in the capped world is 32,666,817,585 pounds. The capped ladder is the market sane companion to Section 2: far cheaper rungs, and a ceiling below the top rung of the relaxed ladder.

## 9. Named variants and sensitivities

Wheat at its documented procurement price of 14,666.67 pounds per tonne in every layer (2025 harvest, top grade): the unconstrained margin is unchanged at 559,713,476,348, because the unconstrained plan plants no wheat, and margins fall at every floored level, to 420,016,235,811 at 50 percent and 270,823,813,589 at 80 percent. The cost of the 80 percent guarantee under procurement pricing is 288,889,662,759 pounds. The direction is the reverse of the version 4.1 relationship, because the forecast farm gate price now sits above the procurement price; the variant measures the concept difference on the current basis and attributes nothing to the concept alone.

Sugar beet at the factory price of 2,400 pounds per tonne: frontier margins identical to the primary run at every level tried (0, 70 and 80 percent), because the model plants no beet at either price.

Costs carried forward by assumption: with every 2022 cost multiplied by 1.50, the cost of the 80 percent guarantee is 224,549,654,133 pounds; multiplied by 2.00, it is 180,141,961,977 pounds. The factors are bracketing assumptions, stated as such, because no official cost table exists after 2022 and no price index series is held. The primary run keeps 2022 costs and says so in its basis.

Reserve split: under the winter first allocation of the unmodeled crop reserve, the ceiling is 80.38 percent and the margin at the 80 percent level is 278,159,876,800 pounds, against 82.41 percent and 291,102,590,296 under the primary proportional split.

Winter potato cost: at the Nili potato cost of 54,176.19 pounds per hectare in place of the summer cost carried in the primary run, the unconstrained margin rises to 592,918,438,384 pounds. The winter potato cost remains a named gap; no winter potato table exists in the cost bulletin.

## 10. Robustness of the 80 percent plan, reported in two distributions

The fixed 80 percent plan is evaluated at sampled budgets drawn from the 1871 to 1970 record, seed 20261114, with late season planting frozen at the normal inflow variant and staple tonnage maximised under recourse. The two sample kinds are reported separately, and no figure mixes them. A ten year window mean is not a year, and no figure here is an annual reliability.

Single year samples, 50 draws: the plan holds its floor in 46.0 percent of draws. Feasible share: minimum 53.75 percent, 10th percentile 69.12, median 79.24, mean 76.52, maximum 80.59. Worst decile mean shortfall against the floor tonnage of 9,803,521 tonnes: 1,911,850 tonnes. Mean shortfall across the draws: 459,096 tonnes.

Ten year window samples, 50 draws: the plan holds its floor in 48.0 percent of draws. Feasible share: minimum 75.34 percent, 10th percentile 76.58, median 79.98, mean 78.94, maximum 80.59. Worst decile mean shortfall: 497,301 tonnes. Mean shortfall: 158,509 tonnes.

The version 4.1 headline, that the plan holds its floor in 65.0 percent of a mixed sample, is withdrawn. On single years alone the plan holds less than half the time under best recourse, and that weaker statement is the true one.

## 11. Forecasts and their errors

Prices, target year 2025, drift selected for every crop: wheat 17,891.58 (band 17,812.31 to 18,693.76; backtest RMSE 2,373.38, MAPE 16.48 percent); paddy rice 20,027.28 at horizon two (band 19,978.19 to 21,226.86; RMSE 5,941.14, MAPE 25.93 percent); maize 20,532.94 (band 20,493.93 to 22,439.90; RMSE 2,359.95, MAPE 16.35 percent); sugar beet 846.03 at horizon two (band 832.74 to 979.34; RMSE 118.98, MAPE 15.07 percent); potatoes 10,753.27 (band 10,876.83 to 11,481.15; RMSE 1,452.25, MAPE 19.53 percent). No learning model beat the simple lines on any price series among models that produced a usable forecast. One exception is recorded in the run log, not hidden: for paddy rice at horizon two the ridge model scored best in the backtest and then diverged on the full data refit, returning an infinite forecast; it is recorded as failed at the forecast step and drift was selected in its place. The potato band sits above its own forecast at the low edge, because the drift residuals for potatoes are mostly positive over the backtest; the property is a fact of that residual distribution and is stated here rather than smoothed.

Yields, target year 2025: wheat 6.6789 by random forest (band 6.6686 to 6.9682); paddy rice 9.1315 by the naive last value line (band 8.9823 to 9.2482); maize 7.6834 by random forest (band 7.5608 to 8.1134); sugar beet 56.0570 by random forest (band 53.4131 to 57.5149); potatoes 31.5165 by ridge (band 31.0644 to 31.7627). Point forecasts and selected models are unchanged from version 4.1; the bands are narrower because they are now quartile bands.

Band coverage, measured sequentially as defined in the repair log: prices 0.0 percent for wheat, 11.1 for maize, 22.2 for potatoes, 20.0 for paddy rice and 20.0 for sugar beet; yields 21.1 for wheat, 15.8 for paddy rice, 57.9 for maize, 26.3 for sugar beet and 26.3 for potatoes. The construction value of a quartile band is 50 percent. The shortfall is concentrated in prices and is the weakest measured property of this build: the pooled residual history is dominated by the low price era, so the layers understate the spread of the current regime. Expected money figures inherit that thinness; the hard floor and ceiling results do not depend on the layer weights.

## 12. The twelve loader actions on blank yield cells

Eleven fills by the stated rule, the area weighted mean of the published district yields for the crop: Nili maize in Kafr El Sheikh, Menoufia, Qalyubia and Damietta at 8.358 tonnes per hectare; Nili potatoes in Sharkia, Dakahlia, Kafr El Sheikh, Gharbia, Menoufia, Qalyubia and Damietta at 18.120 tonnes per hectare, which is the single published Nili potato yield, Beheira, carried to the seven governorates that publish none. Those seven cells are inert in the baseline, because those governorates plant no Nili potatoes in the observed pattern, and live in any optimised plan that plants Nili potatoes there. One substitution, not a fill: rice in Menoufia at 8.395 tonnes per hectare, Menoufia own published yield for 2019 to 2020, the year its substituted baseline area comes from. The Menoufia rice area itself, 7.98 hectares from the 2019 to 2020 panel, is the one baseline area not taken from the 2020 to 2021 panel, as stated in every run header.

## 13. What this note does not claim

The water budgets rest on a calibration of 11.00 billion cubic metres that no source publishes, split across governorates by physical land share; the ladder has not been repriced at scaled anchors in this build, and that sensitivity remains open from the domain critique. The guarantee protects aggregate tonnage of three staples summed over eight governorates; it does not protect any single crop, milled rice, calories or household access. WaPOR satellite totals are used as a scale check only and calibrate nothing. Costs after 2022 do not exist in any official table the project holds; Section 9 prices that gap with labelled assumptions and does not close it.
