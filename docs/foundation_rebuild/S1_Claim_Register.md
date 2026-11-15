# S1 Claim Register: every headline claim in the Nile Delta paper

Paper: paper/Nile_Delta_Paper.md, saved 14 November 2026 at 18:14. Register written 15 November 2026 under Stage S1. Status words follow the brief: Confirmed computation means the value traces to saved unrounded outputs, or was recomputed in S1 from a saved file, and agrees. Reported means the value or sentence appears in prose with no saved output behind it, or with saved output that supports only a weaker form. Unverified means the trail is missing or the saved record contradicts the statement as written. No model was rerun for this register.

## A. The guarantee ladder (paper Section 6.1 and Abstract)

| Claim as printed | Inputs | Generating file or calculation | Status |
| --- | --- | --- | --- |
| Reference tonnage 12,254,407 tonnes: wheat 4,617,795, paddy rice 4,086,080, summer maize 3,550,533 | Ministry panel areas and published district yields, data/external capmas tables | Run log construction in data/processed/run_v4_1_main.txt; audit recompute in audit_v4_1_work/basics.json at unrounded 12,254,407.16 with components 4,617,794.97, 4,086,079.58 and 3,550,532.61 | Confirmed computation |
| Frontier margin, floor 0 percent: 403,078,762,407 pounds | Forecast 2024 prices, official 2022 costs, published district yields | Run log frontier table; audit frontier.json primary_0 at 403,078,762,406.87 | Confirmed computation |
| Frontier margin, floor 50 percent: 297,739,198,932 pounds | Same basis | Run log frontier table; audit frontier_scaled.json primary_50_scaled at 297,739,198,931.58. The audit unscaled solve in frontier.json sits 7,713,181 pounds lower; Audit_Log_v4_1.md explains the gap as a solver scaling effect and records the scaled solve as the match | Confirmed computation, with the scaling note |
| Frontier margin, floor 60 percent: 262,520,406,731 pounds | Same basis | Run log frontier table; audit frontier.json primary_60 at 262,520,406,731.25 | Confirmed computation |
| Frontier margin, floor 70 percent: 223,222,240,454 pounds | Same basis | Run log frontier table; audit frontier.json primary_70 at 223,222,240,454.35 | Confirmed computation |
| Frontier margin, floor 75 percent: 202,983,384,826 pounds | Same basis | Run log frontier table; audit frontier.json primary_75 at 202,983,384,826.24 | Confirmed computation |
| Frontier margin, floor 80 percent: 175,143,528,384 pounds | Same basis | Run log frontier table; audit frontier_scaled.json primary_80_scaled at 175,143,528,383.63. The audit unscaled solve sits 325,601 pounds lower, same scaling note as at 50 percent | Confirmed computation, with the scaling note |
| Cost of the 80 percent level against the unconstrained optimum: 227,935,234,023 pounds | The two margins above | Exact arithmetic on the printed margins; run log cost column; audit verified | Confirmed computation |
| Step cost at 60 percent: 35,218,792,201 pounds; step cost at 80 percent: 27,839,856,442 pounds | The printed margins at 50, 60, 75 and 80 percent | Exact arithmetic on the printed margins, as corrected in paper/Results_Note_v4_2.md. The raw run log prints the 80 percent step as 27,839,856,443, one pound against its own margins; see S1_Defect_List.md item 6 | Confirmed computation, through the correction note |
| Floors of 85 percent and above are infeasible | The version 4.1 formulation | Run log frontier table, status Infeasible at 85 percent; audit frontier.json primary_85, status Infeasible | Confirmed computation |
| Ceiling: 9,833,867 tonnes, 80.25 percent of the reference | Ceiling maximisation in the version 4.1 code | Run log ceiling line; audit ceilings.json primary at 9,833,866.8 tonnes and 80.2476 percent, identical in the linear and binary forms | Confirmed computation |
| Ceiling under the uncapped proportional reserve split: 80.12 percent | Audit side relaxation of the reserve construction | Audit ceilings.json uncapped_proportional at 9,818,690.3 tonnes; Audit_Log_v4_1.md. No author run log on disk prints this variant | Confirmed computation, audit side only |
| Ceiling with no reserve: 90.94 percent; on scaled yields: 75.62 percent; with named caps: 77.44 percent | Labelled variants of the ceiling run | Run log ceiling bound lines (90.94 and 75.62 percent); run_v4_1_caps.txt ceiling line at 9,490,156 tonnes (77.44 percent); audit ceilings.json matches all three | Confirmed computation |
| At every floor level the margin optimal plan is exactly tight: smallest headroom zero tonnes, a four way tie across the low layer in all four inflow states | Saved plans plan_v4_1_floor50 to floor80; clearance maximisations | Run log prints clearance 0.0 tonnes in the four low layer cells. The audit unrounded values in clearance.json are hundredths of a tonne: positive at floor 50 (0.029 to 0.095) and slightly negative at floors 60 to 80 (down to 0.052 below zero) in the audit cell bound evaluation. The tie is exact only at whole tonne print precision | Reported in its exact form; the saved unrounded output supports the rounded form only. See S1_Defect_List.md item 5 |

## B. The historical pattern (paper Section 6.2)

| Claim as printed | Inputs | Generating file or calculation | Status |
| --- | --- | --- | --- |
| Historical pattern expected margin: 86,006,146,997 pounds | Observed areas evaluated on the paper price and cost basis | Run log baseline section, data/processed/run_v4_1_main.txt | Confirmed computation |
| Historical pattern expected staple tonnage: 8,908,274 tonnes, 72.69 percent of the reference | Same evaluation | Run log baseline section | Confirmed computation |
| Historical pattern worst scenario staple tonnage: 7,367,358 tonnes, 60.12 percent of the reference | Same evaluation | Run log baseline section | Confirmed computation |
| Inside this model, the pattern Egypt actually plants holds no guarantee at any level on the ladder | The three values above | No saved output shows the pattern failing the 50 percent level. Its own worst scenario value, 60.12 percent, sits above the 50 percent floor tonnage of 6,127,204 tonnes, so under the plain reading of holds the two printed statements clash. No per scenario feasibility record for the pattern exists on disk to settle which reading the build used | Unverified as stated; definition clash. See S1_Defect_List.md item 1 |
| Accounting difference between the optimised and historical margins: 317,072,615,410 pounds, 368.66 percent of the baseline margin | The two margins above | Run log baseline section; arithmetic checks | Confirmed computation |

## C. Warnings, stress and the beet test (paper Sections 6.3, 6.4, 6.8)

| Claim as printed | Inputs | Generating file or calculation | Status |
| --- | --- | --- | --- |
| Potato area multiples in the unconstrained optimum: winter 16.91, summer 22.69, Nili 366.22 times observed; at the 80 percent floor: summer 9.32, Nili 97.76 | Optimised planted areas against observed areas | Run log market absorption warnings at the 0 and 80 percent levels | Confirmed computation |
| Stress at budget scale 0.90: capacity 9,049,077 tonnes (73.84 percent); profit choice zero staples at margin 375,091,832,795 pounds | Version 4.1 stress runs, no floor | Run log stress section | Confirmed computation |
| Stress at budget scale 0.80: capacity 8,264,287 tonnes (67.44 percent); profit choice zero staples at margin 343,134,636,238 pounds | Same | Run log stress section | Confirmed computation |
| Sugar beet at the factory price of 2,400 pounds per tonne: frontier margins identical at every level tried | Variant run with the beet price swapped | data/processed/run_v4_1_beet2400.txt; audit frontier.json beet2400 entries match the primary margins at 0, 70 and 80 percent | Confirmed computation |
| Winter potato cost sensitivity: at the Nili potato cost the unconstrained margin rises to 436,283,724,443 pounds | Variant run with the winter potato cost swapped | Run log variant line; audit frontier.json winterpot_nilicost_0 at 436,283,724,443.03 | Confirmed computation |

## D. Water values (paper Section 6.5 and Appendix D)

| Claim as printed | Inputs | Generating file or calculation | Status |
| --- | --- | --- | --- |
| Dry state at expected layer: 47.39 to 64.32 pounds per cubic metre, water binding in all eight governorates | Linear relaxation duals at floor 80.15 percent, author solution | Run log water values section: dry expected row prints 47.39 (Gharbia) to 64.32 (Qalyubia) | Confirmed computation |
| Normal state at expected layer: 19.17 to 53.54, Damietta lowest, Sharkia highest | Same | Run log water values section: normal expected row prints 19.17 (Damietta) to 53.54 (Sharkia) | Confirmed computation |
| High state at expected layer: 11.81 to 14.64 | Same | Run log water values section: high expected row | Confirmed computation |
| Dry state at low prices: duals spike to 1,073.50 to 1,240.34 | Same | Run log water values section: dry low row prints 1,073.50 (Qalyubia) to 1,240.34 (Dakahlia) | Confirmed computation |
| Reaudit alternative solution: dry 48.63 to 64.32; high 12.00 to 14.64; Damietta in the normal state at 16.68 | Audit side solve of the same relaxation | Audit duals.json, unrounded values: dry expected minimum 48.628 (Beheira), normal expected Damietta 16.682, high expected minimum 12.002 | Confirmed computation |

## E. Information values (paper Section 6.6)

| Claim as printed | Inputs | Generating file or calculation | Status |
| --- | --- | --- | --- |
| Wait and see value 198,927,633,193 pounds; recourse value 175,143,528,384; expected value of perfect information 23,784,104,809 pounds | Twelve deterministic solves and the 80 percent recourse solve | Audit info_stress.json unrounded: 198,927,633,192.55, 175,143,528,383.63 and 23,784,104,808.92; run log information section prints the same values and the twelve scenario margins | Confirmed computation |
| True mean budget 10.9844 billion cubic metres | State budgets 8.588, 10.502, 13.434, 9.580 at probabilities 0.2275, 0.4451, 0.3165, 0.0110 | Audit info_stress.json true_mean_budget at 10.98439951; the weighted sum of the printed state values agrees | Confirmed computation |
| The plan built on true means fails the 80 percent floor in 10 of the 12 scenarios, holding only in the normal and high inflow states at high prices | Expected value problem solve, then evaluation across the twelve scenarios | Run log finding line names the ten failing scenarios; audit info_stress.json ev_fails agrees | Confirmed computation |
| Penalised value of the stochastic solution: 7,607,863,594 pounds at a penalty of 25,000 pounds per tonne | Penalised recourse evaluation | Audit penalised.json penalised_vss_mine at 7,607,863,593.78 and penalised_eev at 167,535,664,789.85; run log prints the exact difference of its printed components. Note: audit info_stress.json carries stray penalised fields that contradict this file; see S1_Defect_List.md item 7 | Confirmed computation |

## F. Sampled behaviour of the 80 percent plan (paper Section 6.7)

| Claim as printed | Inputs | Generating file or calculation | Status |
| --- | --- | --- | --- |
| The plan holds its floor in 65.0 percent of 100 sampled years | The saved sample file | Recomputed in S1 from data/processed/robustness_samples_v4_1.csv: 65 of 100 samples reach at least the floor tonnage of 9,803,525.7 tonnes | Confirmed computation |
| Maximum share range: worst sample 55.28 percent, median 82.03 percent, best 82.67 percent | Same file | Recomputed in S1 from the same file: minimum 55.28, median 82.03, maximum 82.67 | Confirmed computation |
| Worst decile expected shortfall 1,103,686 tonnes; mean shortfall across all samples 156,385 tonnes | Same file | Recomputed in S1: worst decile mean shortfall 1,103,685.6 tonnes; overall mean 156,385.0 tonnes | Confirmed computation |
| Sample construction: 100 draws alternating single years and ten year window means, seed 20261114, late planting frozen at the normal inflow variant | The Aswan record and the fixed 80 percent plan | Paper Appendix C states the construction; audit robust_numerics.json rederives the saved sample ratios and tonnages with differences at most 2 in a billion | Confirmed computation |

## G. Forecasts (paper Section 4 and Appendix A)

| Claim as printed | Inputs | Generating file or calculation | Status |
| --- | --- | --- | --- |
| 2024 price forecasts with errors: wheat 10,296.94 (RMSE 1,485.60, MAPE 14.61 percent); paddy rice 19,394.14 (3,735.60, 14.47); maize 14,836.22 (1,998.12, 15.64); sugar beet 820.52 (92.26, 10.21); potatoes 8,405.44 (1,396.76, 19.52) | FAOSTAT price series to 2023; five candidate models per crop | data/processed/forecast_prices_yields_v4.csv holds every value unrounded and matching; data/processed/backtest_scores_v4.csv holds the full score table; run_forecasting_v4.txt is the run record | Confirmed computation |
| 2025 yield forecasts with errors: wheat 6.6789 (random forest), paddy rice 9.1315 (naive last value), maize 7.6834 (random forest), sugar beet 56.0570 (random forest), potatoes 31.5165 (ridge), with the printed RMSE and MAPE values | FAOSTAT crops series to 2024 | Same forecast file, unrounded and matching | Confirmed computation |
| No learning model beat the simple lines on any price series; the drift line won for every crop | The backtest score table | backtest_scores_v4.csv records the drift model as the selected row for all five price crops in forecast_prices_yields_v4.csv, with test counts of 13 seasons for wheat, maize and potatoes and 10 for paddy rice and sugar beet; yield test counts are 24 seasons for every crop, matching the paper text | Confirmed computation |
| The low and high model layers are set by the forecast error bands | Forecast bands in the same file | Paper Appendix C prints the band values the model consumes; the forecast file band columns match them | Confirmed computation |

## H. Data anchors (paper Sections 1 and 3 and Appendix A)

| Claim as printed | Inputs | Generating file or calculation | Status |
| --- | --- | --- | --- |
| Physical cultivated area 1,676,580 hectares; annual cropped area 3,176,474 hectares | Ministry bulletin tables via capmas_governorate_total_cropped_area.csv | Audit basics.json at unrounded 1,676,580.36 and 3,176,473.86 | Confirmed computation |
| Inflow states: budgets 8.588, 10.502, 13.434 and 9.580 billion cubic metres; probabilities 0.2275, 0.4451, 0.3165, 0.0110; ratios 0.7807, 0.9547, 1.2213, 0.8709 | Aswan gauged record 1871 to 1970 in nile_inflow_aswan_series.csv; anchor 11.00 billion cubic metres, a stated calibration | Audit basics.json inflow section recomputed from the series; run log prints the construction. The anchor itself is an assumption, labelled as one in the paper and in the code | Confirmed computation; the anchor is a stated assumption |
| Aswan record mean 91.94 and standard deviation 16.92 billion cubic metres | The same series | Audit basics.json records the recomputed values 91.935 and 16.9228 | Confirmed computation |
| WaPOR measured total consumption, eight governorates, mean 24.416 billion cubic metres a year over 2018 to 2025; modeled baseline demand at full duties 16.398 | wapor_aeti_governorate_2018_2025.csv and WAPOR_METHODS.md; baseline areas times applied duties | Run log WaPOR comparison table prints both totals, 16.398 against 24.416 | Confirmed computation |
| The reserve cap writes off 30,136 hectares of annual unmodeled area (Kafr El Sheikh 11,084; Menoufia 10,933; Qalyubia 7,031; Damietta 1,088) | Reserve construction in the code | Paper Appendix C states it; Audit_Log_v4_1.md replays the construction pool by pool and reaches the same total | Confirmed computation |
| Ceiling relaxations: tripling dry state water raises the ceiling to 87.65 percent; holding the floor in the expected layer only raises it to 82.91 percent; water binds in 47 of 96 cells; winter land binds in all eight governorates | Audit side relaxations of the ceiling problem | Audit ceilings.json relax entries; Audit_Log_v4_1.md reports each figure | Confirmed computation |

## Register summary

Of the 47 claim rows above, 45 are confirmed computations. Four of those 45 carry a stated note: the frontier margins at 50 and 80 percent rest on the audit scaled solve, the step costs rest on the correction note layer, and the uncapped reserve ceiling rests on the audit side alone. One row is reported in a form stronger than its saved unrounded output supports (the clearance sentence), and one row is unverified as stated (the historical pattern guarantee sentence, which clashes with the pattern own worst scenario figure). No headline money figure, ceiling figure, forecast figure or robustness figure in the paper lacks a saved output behind it. The weaknesses are concentrated in wording precision and in the version trail, and they are listed in S1_Defect_List.md.
