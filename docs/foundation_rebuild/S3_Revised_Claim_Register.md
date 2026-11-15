# S3 revised claim register: every version 4.1 headline on the version 5 basis

Stage S3 of the foundation rebuild, written 15 November 2026. This register takes the 47 claim rows of S1_Claim_Register.md in its own order and marks each one on the repaired build: confirmed means the claim stands as printed, on the version 5 run; corrected means the claim is replaced by the version 5 value printed here; withdrawn means the claim is false, or rests on a superseded basis or a variant not carried into version 5, and must not be quoted again in its old form. Version 5 evidence: paper/Results_Note_v5.md, the run logs run_v5_main.txt, run_v5_caps.txt, run_v5_beet2400.txt, run_v5_wheatproc.txt, run_v5_costsens.txt, run_v5_reservealt.txt, run_v5_robust.txt and run_forecasting_v5.txt, and the unrounded results_v5 JSON files.

## A. The guarantee ladder

| Claim as printed in version 4.1 | Status | Version 5 position |
| --- | --- | --- |
| Reference tonnage 12,254,407 tonnes (wheat 4,617,795; rice 4,086,080; summer maize 3,550,533) | Corrected | 12,254,401 tonnes (wheat 4,617,795; rice 4,086,074; summer maize 3,550,533). The rice component falls by about 6 tonnes on the Menoufia yield substitution |
| Frontier margin, floor 0 percent: 403,078,762,407 | Corrected | 559,713,476,348 |
| Frontier margin, floor 50 percent: 297,739,198,932 | Corrected | 430,297,336,634 |
| Frontier margin, floor 60 percent: 262,520,406,731 | Corrected | 386,417,040,545 |
| Frontier margin, floor 70 percent: 223,222,240,454 | Corrected | 340,320,741,667 |
| Frontier margin, floor 75 percent: 202,983,384,826 | Corrected | 316,954,235,954 |
| Frontier margin, floor 80 percent: 175,143,528,384 | Corrected | 291,102,590,296 |
| Cost of the 80 percent level: 227,935,234,023 | Corrected | 268,610,886,052 |
| Step costs at 60 and 80 percent: 35,218,792,201 and 27,839,856,442 | Corrected | 43,880,296,089 and 25,851,645,658, computed on the unrounded margins the run now saves |
| Floors of 85 percent and above are infeasible | Confirmed | Infeasible on the version 5 basis as well, and under both cost escalation brackets |
| Ceiling: 9,833,867 tonnes, 80.25 percent | Corrected | 10,099,349 tonnes, 82.41 percent. The rise comes from the quartile yield bands; the drought removal contributes nothing, because the drought budget never bound |
| Ceiling under the uncapped proportional reserve split: 80.12 percent | Withdrawn | An audit side variant of the old basis, never recomputed in version 5. The version 5 reserve sensitivity is the winter first split, ceiling 80.38 percent |
| Ceiling with no reserve 90.94 percent; on scaled yields 75.62 percent; with named caps 77.44 percent | Corrected | 93.51 percent; 77.67 percent; 79.50 percent |
| At every floor level the margin optimal plan is exactly tight, smallest headroom zero tonnes, a four way tie | Corrected | Plans are tight within solver tolerance, stated at honest precision: smallest headrooms 0.016 tonnes under the floor at 50 percent, 0.039 under at 60, 0.062 under at 70, 0.024 under at 75, 0.015 over at 80. The low layer tie is three way, one cell per inflow state, because the scenario set now has three inflow states |

## B. The historical pattern

| Claim as printed | Status | Version 5 position |
| --- | --- | --- |
| Pattern expected margin: 86,006,146,997 | Corrected | 144,167,922,884 |
| Pattern expected staple tonnage: 8,908,274 tonnes, 72.69 percent | Corrected | 9,270,566 tonnes, 75.65 percent |
| Pattern worst scenario staple tonnage: 7,367,358 tonnes, 60.12 percent | Corrected | 7,684,799 tonnes, 62.71 percent, under profit seeking recourse |
| Inside this model, the pattern holds no guarantee at any level on the ladder | Withdrawn | False, as Check 1 proved on the old basis. On the version 5 test the pattern holds the 50, 60 and 65 percent levels in every scenario and fails from 70 percent. Its worst scenario capacity is 8,056,850 tonnes, 65.75 percent |
| Accounting difference: 317,072,615,410, 368.66 percent of the baseline margin | Corrected | 415,545,553,464, 288.24 percent |

## C. Warnings, stress and the beet test

| Claim as printed | Status | Version 5 position |
| --- | --- | --- |
| Potato area multiples in the unconstrained optimum: winter 16.91, summer 22.69, Nili 366.22; at the 80 percent floor: summer 9.32, Nili 97.76 | Corrected | Unconstrained: winter 16.91, summer 22.71, Nili 369.63. At the 80 percent floor: winter 2.81, summer 6.81, Nili 108.91 |
| Stress at budget scale 0.90: capacity 73.84 percent; profit choice margin 375,091,832,795 | Corrected | Capacity 9,295,584 tonnes, 75.86 percent; profit choice margin 520,907,656,409, no staples planted |
| Stress at budget scale 0.80: capacity 67.44 percent; profit choice margin 343,134,636,238 | Corrected | Capacity 8,491,820 tonnes, 69.30 percent; profit choice margin 476,620,802,204, no staples planted |
| Sugar beet at the factory price of 2,400: frontier margins identical at every level tried | Confirmed | Recomputed on the version 5 basis: margins identical at 0, 70 and 80 percent (559,713,476,348; 340,320,741,667; 291,102,590,296) |
| Winter potato cost sensitivity: unconstrained margin 436,283,724,443 at the Nili cost | Corrected | 592,918,438,384 on the version 5 basis |

## D. Water values

All four range rows are corrected, and all four now carry the standing label: one optimal dual solution of the LP relaxation at the exact floor 0.8231405524 as a share of the reference tonnage, conditional values in pounds per cubic metre. At that floor the relaxation objective is 273,356,788,636 against the mixed integer objective of 272,969,293,877, a gap of 0.142 percent.

| Claim as printed | Status | Version 5 position |
| --- | --- | --- |
| Dry state at expected layer: 47.39 to 64.32 | Corrected | 76.32 to 91.31, Damietta lowest, Kafr El Sheikh highest |
| Normal state at expected layer: 19.17 to 53.54, Damietta lowest, Sharkia highest | Corrected | 24.45 to 77.07, Damietta lowest, Qalyubia highest |
| High state at expected layer: 11.81 to 14.64 | Corrected | 18.05 to 44.94 |
| Dry state at low prices: 1,073.50 to 1,240.34 | Corrected | 826.44 to 961.74 |
| Reaudit alternative solution ranges (dry 48.63 to 64.32; Damietta normal 16.68; high 12.00 to 14.64) | Withdrawn | Values of the version 4.1 relaxation at its own floor, not recomputed for version 5. Dual non uniqueness itself stands and is disclosed in words in the version 5 note |

## E. Information values

| Claim as printed | Status | Version 5 position |
| --- | --- | --- |
| Wait and see 198,927,633,193; recourse 175,143,528,384; EVPI 23,784,104,809 | Corrected | Wait and see 304,561,061,130; recourse 291,102,590,296; EVPI 13,458,470,835, all at the 80 percent floor |
| True mean budget 10.9844 billion cubic metres | Corrected | 11.0000 billion cubic metres exactly, the drought scaling artefact removed |
| The true mean plan fails the 80 percent floor in 10 of the 12 scenarios | Corrected | It fails in 7 of the 9 scenarios. The standard VSS remains withheld |
| Penalised VSS: 7,607,863,594 at a penalty of 25,000 per tonne | Corrected | 75,931,039,486 on one consistent definition: penalised stochastic optimum 346,643,462,500 minus penalised expected value of the true mean plan 270,712,423,014, same penalty on both sides |

## F. Sampled behaviour of the 80 percent plan

| Claim as printed | Status | Version 5 position |
| --- | --- | --- |
| The plan holds its floor in 65.0 percent of 100 sampled years | Withdrawn | The mixed sample figure is withdrawn as a reading. Split by kind: the version 5 plan holds its floor in 46.0 percent of 50 single year samples and in 48.0 percent of 50 ten year window samples |
| Share range: worst 55.28, median 82.03, best 82.67 percent | Corrected | Single years: minimum 53.75, median 79.24, maximum 80.59. Window samples: minimum 75.34, median 79.98, maximum 80.59 |
| Worst decile expected shortfall 1,103,686 tonnes; mean shortfall 156,385 tonnes | Corrected | Single years: worst decile 1,911,850; mean 459,096. Window samples: worst decile 497,301; mean 158,509 |
| Sample construction: 100 draws alternating single years and ten year window means, seed 20261114, late planting frozen at the normal inflow variant | Corrected | The construction and the frozen convention are unchanged, and the saved version 5 sample file recomputes. What changes is the reporting: two distributions, never one mixed figure, and no annual reliability reading |

## G. Forecasts

| Claim as printed | Status | Version 5 position |
| --- | --- | --- |
| 2024 price forecasts with errors, drift for every crop | Corrected | 2025 price forecasts, drift for every crop among usable models: wheat 17,891.58 (RMSE 2,373.38, MAPE 16.48 percent); paddy rice 20,027.28 at horizon two (5,941.14, 25.93); maize 20,532.94 (2,359.95, 16.35); sugar beet 846.03 at horizon two (118.98, 15.07); potatoes 10,753.27 (1,452.25, 19.53) |
| 2025 yield forecasts with errors and selected models | Corrected | Point forecasts and selected models stand exactly as printed (wheat 6.6789 random forest; rice 9.1315 naive; maize 7.6834 random forest; beet 56.0570 random forest; potatoes 31.5165 ridge, with the printed errors). The bands are corrected to quartile values: wheat 6.6686 to 6.9682; rice 8.9823 to 9.2482; maize 7.5608 to 8.1134; beet 53.4131 to 57.5149; potatoes 31.0644 to 31.7627 |
| No learning model beat the simple lines on any price series; the drift line won for every crop | Confirmed | Confirmed at the used horizons, with one recorded event: for paddy rice at horizon two, ridge scored best in the backtest and diverged on the full data refit, and is recorded as failed at the forecast step in the run log. Among models that produced a usable forecast, drift won every price series |
| The low and high model layers are set by the forecast error bands | Corrected | The layers are set by the residual quartile bands, which now match the 0.25, 0.50 and 0.25 layer weights. Sequential band coverage is measured and printed in the version 5 note; for prices it runs from 0.0 to 22.2 percent against a construction value of 50 percent, and that shortfall is an open weakness, not a repaired one |

## H. Data anchors

| Claim as printed | Status | Version 5 position |
| --- | --- | --- |
| Physical cultivated area 1,676,580 hectares; annual cropped area 3,176,474 hectares | Confirmed | Same source files, unchanged, recomputed in the version 5 header |
| Inflow states: budgets 8.588, 10.502, 13.434 and 9.580; probabilities 0.2275, 0.4451, 0.3165, 0.0110 | Corrected | Three states in the simplex at probabilities 0.2300, 0.4500 and 0.3200 with budgets 8.588, 10.502 and 13.434. The 9.580 budget survives only as the drought stress budget, with no probability |
| Aswan record mean 91.94 and standard deviation 16.92 | Confirmed | Unchanged series, recomputed values stand |
| WaPOR measured total consumption mean 24.416 against modeled baseline demand 16.398 | Confirmed | Same files and the same comparison, with its role stated as a scale check only; it calibrates nothing |
| The reserve cap writes off 30,136 hectares of annual unmodeled area | Confirmed | The primary construction is unchanged, so the figure stands. It is now joined by the measured alternative: under the winter first split the ceiling is 80.38 percent and the 80 percent margin is 278,159,876,800 |
| Ceiling relaxations: tripling dry state water raises the ceiling to 87.65 percent; floor in the expected layer only 82.91 percent; water binds in 47 of 96 cells; winter land binds in all eight governorates | Withdrawn | Audit side relaxations of the old basis and of the twelve scenario set, not recomputed in version 5. The scenario set now has nine states and 72 water cells, so the cell count itself no longer exists |

## Register summary

Of the 47 rows: 7 confirmed, 35 corrected with the version 5 value, and 5 withdrawn. The withdrawals are the historical pattern guarantee sentence, the mixed sample robustness headline, the uncapped reserve ceiling, the version 4.1 audit dual solution ranges, and the version 4.1 audit ceiling relaxations. Every money figure, ceiling figure and forecast figure in the version 5 note traces to a saved unrounded output of the version 5 runs. The two claims that were false as printed, the pattern sentence and the penalised VSS, are replaced by measured values on consistent definitions, and the register records both replacements where a reader of the old paper will look for them.
