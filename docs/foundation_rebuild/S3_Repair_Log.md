# S3 repair log: version 5 of the Nile Delta model

Stage S3 of the foundation rebuild, written 15 November 2026 by the repair lead. Every repair below was ordered by the rebuild brief, by the S2 data quality report, or by one of the two independent checks in this folder. Each entry states the defect, the fix, and the numerical effect measured in the repaired run. Nothing from version 4.1 was overwritten or deleted: the repaired build is src/forecasting_v5.py and src/allocation_model_v5.py, its inputs and outputs carry version 5 names, and every version 4.1 file keeps its 14 November timestamp.

Run record for version 5: data/processed/run_forecasting_v5.txt, run_v5_main.txt, run_v5_caps.txt, run_v5_beet2400.txt, run_v5_wheatproc.txt, run_v5_costsens.txt, run_v5_reservealt.txt and run_v5_robust.txt. Unrounded headline results sit in data/processed/results_v5_main.json and its companion files, one per run mode.

## Repair 1. Prices vintage and target year

Defect (S2 finding 1 and finding 2). The prices file ended at 2023 while observed 2024 farm gate prices existed in the December 2025 FAOSTAT vintage, recorded in the second mining sweep and never written into the file. The model therefore consumed forecasts of a year already observed, and its price target year (2024) differed from its yield target year (2025).

Fix. A corrected prices extract is saved as data/external/faostat_producer_prices_egypt_dec2025.csv: the full series of the old file plus the three observed 2024 values, wheat 17,380, maize 19,942 and potatoes 10,446 pounds per tonne, each row carrying its provenance in the source column. Paddy rice and sugar beet end at 2023 in every vintage held, so no 2024 row exists for them. The version 5 forecasting module reads the corrected extract and targets 2025 for every price: one step from the 2024 observation for wheat, maize and potatoes, and two steps from the 2023 observation for paddy rice and sugar beet, with model selection and bands computed at the horizon actually used. The price basis of the whole run is stated in one sentence, printed in the run header and in the results note: prices are 2025 forecasts from the FAOSTAT farm gate series, observed to 2024 for wheat, maize and potatoes and to 2023 for paddy rice and sugar beet, with costs held at official 2022 values.

Effect. The expected price layer moved from the version 4.1 values to: wheat 10,296.94 to 17,891.58; paddy rice 19,394.14 to 20,027.28; maize 14,836.22 to 20,532.94; sugar beet 820.52 to 846.03; potatoes 8,405.44 to 10,753.27 pounds per tonne. No learning model beat the drift line on any price series at the used horizon, with one event recorded under Repair 2. Every margin in the paper inherits this change; the frontier effects are collected in the summary table at the end of this log.

## Repair 2. Band convention, and one recorded forecast failure

Defect (S2 finding 5; Check 2 item 4.2). The forecasting module built its low and high layers from the 10th and 90th percentile backtest residuals, while the allocation model weighted the layers 0.25, 0.50 and 0.25 as if the band edges were quartiles. The two conventions contradicted each other, and band coverage was reported nowhere.

Fix. The version 5 forecasting module builds the band at the 25th and 75th percentiles of the backtest residuals, the residual quartiles, so the construction and the weights now describe the same object. The module also reports sequential band coverage for every crop and target: for each backtest origin in year order, the band is built from the residuals of the earlier origins only, and the coverage is the share of later origins whose realised residual fell inside that band.

Effect on the layers. The bands narrowed for every crop, because a quartile band is narrower than a 10th to 90th percentile band. Example: the wheat yield low ratio moved from 6.485 divided by 6.679 to 6.669 divided by 6.679, so the low yield layer now sits about 2.8 percent higher than it did; the ceiling effect of the narrower bands is measured in the summary table.

Measured coverage. The sequential coverage of the quartile band is far below the 50 percent its construction implies, for prices above all: wheat 0.0 percent over 9 later origins, maize 11.1 percent, potatoes 22.2 percent, paddy rice 20.0 percent over 5 origins at horizon two, sugar beet 20.0 percent. Yield coverage: wheat 21.1 percent, paddy rice 15.8 percent, maize 57.9 percent, sugar beet 26.3 percent, potatoes 26.3 percent, each over 19 later origins. The cause is visible in the data: the residuals are dominated by the low price era, and the recent origins carry errors many times larger, so a band calibrated on the pooled history undercovers the current regime when read in sequence. This is reported, not repaired, because the repair order fixed the convention, not the calibration window. It is carried into the Gate A assessment as an open weakness: the hard floor results do not depend on the layer probabilities, but every expected money figure does.

Recorded failure during this repair. The first version 5 forecasting run returned an infinite rice price forecast: the ridge model scored best in the two step backtest (RMSE 5,281.53) but its full data refit diverged, returning 15,716,051 pounds per tonne at step one and infinity at step two. The module now applies one stated condition, in the open: a model that wins the backtest must also return a finite positive forecast when refitted at the used horizon, and a model that fails that test is recorded as failed in the run log while selection passes to the next model in score order. Under that rule the rice price selection is drift (RMSE 5,941.14), and the failure note stands in run_forecasting_v5.txt. No value was adjusted by hand.

## Repair 3. The baseline claim

Defect (S1 defect item 1; Check 1 check 1, verdict fail). The paper printed that the historical pattern holds no guarantee at any level on the ladder, beside its own worst scenario figure of 60.12 percent of the reference, above the lowest rung. Check 1 proved the sentence false on the version 4.1 basis: the pattern holds the 50 and 60 percent floors in every scenario and fails from 65 percent.

Fix. The false sentence dies. The version 5 main run evaluates the fixed historical pattern scenario by scenario with staple maximising recourse and tests it against every ladder level, printing the per scenario capacities and the highest level held.

Effect on the repaired basis. The pattern capacity by scenario runs from 8,056,850 tonnes in the dry state at the low layer (65.75 percent of the reference) to 11,392,530 tonnes in the high state at the high layer (92.97 percent). The pattern holds the 50, 60 and 65 percent levels in every scenario and fails from 70 percent. Its delivered tonnage under profit seeking recourse, a separate and weaker reading, has a minimum of 7,684,799 tonnes (62.71 percent) and an expectation of 9,270,566 tonnes (75.65 percent), so the delivered reading by itself clears the 50 and 60 percent rungs. The pattern expected margin on the new price basis is 144,167,922,884 pounds, against 86,006,146,997 on the old basis.

## Repair 4. Penalised VSS on one consistent definition

Defect (Check 1 check 4, verdict fail). The printed penalised value of the stochastic solution, 7,607,863,594 pounds, paired the hard floor optimum on one side with a penalised evaluation on the other. The penalised stochastic problem itself had never been solved.

Fix. The version 5 information section solves the penalised stochastic problem and the penalised evaluation of the true mean plan under the same penalty of 25,000 pounds per tonne of shortfall, and reports their difference as the penalised VSS. The standard VSS remains withheld, because the true mean plan still cannot hold the floor, now in 7 of the 9 scenarios.

Effect. Penalised stochastic optimum 346,643,462,500 pounds; penalised expected value of the true mean plan 270,712,423,014 pounds; penalised VSS 75,931,039,486 pounds. On the version 4.1 basis Check 1 computed the consistent figure as 48,898,727,094 pounds, so the defect was worth about 41 billion pounds of understatement there. The other information values moved with the new basis: recourse value 291,102,590,296, wait and see value 304,561,061,130, EVPI 13,458,470,835 pounds (against 23,784,104,809 before). The true mean budget is now exactly 11.0000 billion cubic metres, because the three state ratios are band means of the same record and their counts weight them back to the record mean; the version 4.1 figure of 10.9844 was an artefact of the drought scaling removed in Repair 5.

## Repair 5. Drought state out of the simplex

Defect (Check 2 item 4.1; S2 finding 4). The drought state was built from ten year window means of the inflow record. Its probability was one window in 91 by construction, and its budget of 9.580 billion cubic metres is wetter than the dry budget of 8.588, yet it sat inside the probability weights of every expected number in the paper.

Fix. The drought state leaves the simplex. The three genuine states are renormalised from the record counts: dry 0.2300 (23 of 100 years), normal 0.4500 (45 of 100), high 0.3200 (32 of 100), with budgets unchanged at 8.588, 10.502 and 13.434 billion cubic metres. The scenario set is now nine. The drought budget runs as a named stress beside the frontier and enters no expected value.

Effect. At the drought budget of 9.580 billion cubic metres, expected prices and yields, the maximum staple capacity is 11,104,798 tonnes (90.62 percent of the reference) and the profit choice earns 502,602,629,209 pounds while planting no staples. Both figures are single state values and are labelled as such wherever they travel. No expected figure in version 5 contains any drought weight.

## Repair 6. Wheat procurement variant

Defect (Check 2 item 2.3). The price concept variant had been run for sugar beet, where it changes nothing, and never for wheat, where the documented procurement price sat far from the price the model paid.

Fix. A wheatproc run mode prices wheat at the documented procurement price of 14,666.67 pounds per tonne (2025 harvest, top grade, 2,200 pounds per ardab of 150 kilograms) in every layer state, all else equal, exactly as the beet variant is built.

Effect, and a reversed direction. In version 4.1 the farm gate forecast of 10,296.94 sat about 42 percent below the procurement price. After Repair 1 the farm gate forecast of 17,891.58 sits about 22 percent above it, so the variant now cuts wheat revenue instead of raising it, and the floor becomes more expensive to hold: margins fall at every floored level, by 10,281,100,823 pounds at the 50 percent level and by 20,278,776,706 at the 80 percent level, where the margin is 270,823,813,589 against 291,102,590,296 in the primary run. The cost of the 80 percent guarantee under procurement pricing is 288,889,662,759 pounds, against 268,610,886,052 in the primary run. The unconstrained margin is unchanged, because the unconstrained plan plants no wheat.

## Repair 7. Yield fills documented, Menoufia corrected

Defect (S1 defect item 4; S2 finding 6 and finding 7; Check 2 item 5.3). The code filled twelve district yield cells; the paper documented one. The Menoufia rice fill paired a 2019 to 2020 area with a cross governorate yield although Menoufia own published yield for that year sat unused in the yield file.

Fix. The loader now substitutes Menoufia own published 2019 to 2020 rice yield of 8.395 tonnes per hectare for that cell, recorded as a substitution in the run header. The remaining eleven fills are printed in the run header and listed in full in the version 5 results note: Nili maize in Kafr El Sheikh, Menoufia, Qalyubia and Damietta at 8.358 tonnes per hectare, and Nili potatoes in Sharkia, Dakahlia, Kafr El Sheikh, Gharbia, Menoufia, Qalyubia and Damietta at 18.120 tonnes per hectare, the single published Nili potato yield of Beheira carried across. Together with the Menoufia substitution, all twelve loader actions on blank cells are now on the printed record.

Effect. The rice reference tonnage falls by about 6 tonnes, from 4,086,080 to 4,086,074, and the total reference from 12,254,407 to 12,254,401 tonnes. No headline moves; the repair is to the audit trail.

## Repair 8. The cost gap priced

Defect (Check 2 item 2.1). Margins combine 2025 level prices with official 2022 costs. The gap was named in the paper and never priced.

Fix. A costsens run mode reprices the whole ladder with every 2022 cost multiplied by a stated factor. No official cost table exists after 2022 and no price index series is held in the project sources (the CAPMAS inflation releases located in the second sweep give percentage changes only, with no level series from which a factor could be computed), so no measured factor exists. Two bracketing factors are therefore run and labelled as assumptions: times 1.50 and times 2.00.

Effect. Under costs times 1.50: unconstrained margin 470,416,628,116; margin at the 80 percent level 245,866,973,983; cost of the 80 percent guarantee 224,549,654,133 pounds. Under costs times 2.00: unconstrained 381,199,155,435; at 80 percent 201,057,193,458; cost of the guarantee 180,141,961,977 pounds. The absolute cost of the guarantee falls as costs rise, because the unconstrained potato plan is the most cost intensive plan on the ladder, so scaling costs compresses the gap it is measured against. The ladder keeps its order under both factors and the 85 percent level stays infeasible under both. The gap is now priced; it is not closed, and the primary run still carries 2022 costs, stated in its basis sentence.

## Repair 9. Reserve split sensitivity

Defect (Check 2 item 1.2). The seasonal reserve splits each governorate annual unmodeled area across the season pools in proportion to the observed modeled area, then caps each pool reserve at the free land of that pool, writing off 30,136 hectares. The only sensitivity offered varied the cap while sharing the same split, so the split itself was never tested, although the largest unmodeled Delta crop, berseem clover, is a winter crop and a season true split would load the winter pool more heavily.

Fix. A reservealt run mode builds the winter first allocation: each governorate unmodeled area fills the winter pool reserve up to its free land first, then summer, then Nili, under the same caps. This is the winter heavy bound of the split, a bounding construction rather than an estimate, and it is labelled as such in the code and the note.

Effect. Under the winter first split the ceiling falls from 82.41 percent to 80.38 percent (9,849,668 tonnes), and the margin at the 80 percent level falls from 291,102,590,296 to 278,159,876,800 pounds. The split assumption is therefore worth about two points of ceiling and about 12.9 billion pounds at the top rung: material, bounded, and now measured instead of asserted.

## Repair 10. Precision and labels

Defects (S1 defect items 5 and 10; Check 1 checks 5 and 8; Check 2 item 3.4). Floor headrooms were printed as exact zeros while the unrounded values sat hundredths of a tonne either side. The dual run floor was printed to two decimals while the quoted ranges are exact only at the seventh decimal. The robustness headline mixed single year samples with ten year window means in one figure read as a frequency. Headline results survived only as whole pound prints in a text log.

Fixes. Clearance is now printed to a thousandth of a tonne, with a standing sentence that a headroom below one tonne means the plan is tight at its floor within solver tolerance, not exact. The dual section prints the exact floor, 0.8231405524 as a share of the reference tonnage, labels its table as one optimal dual solution of the LP relaxation at that floor, and prints the mixed integer objective at the same floor beside the relaxation objective. The robustness run reports the two sample kinds as two separate distributions and never as one figure. Every run mode writes its headline results unrounded to a JSON results file.

Effects. Smallest floor headrooms in the primary run: 0.016 tonnes under the floor tonnage at the 50 percent level (a three way tie across the low layer, one cell per inflow state), 0.039 under at 60 percent, 0.062 under at 70 percent, 0.024 under at 75 percent, and 0.015 over at 80 percent. The negative hundredths are solver tolerance artefacts of a few hundredths of a tonne against floors of millions of tonnes; the substance, that the margin optimal plans are tight at their floors, stands at honest precision. Relaxation against integer at the dual floor: 273,356,788,636 against 272,969,293,877 pounds, a gap of 387,494,759 pounds or 0.142 percent. Robustness of the 80 percent plan, split as ordered: over 50 single year samples the plan holds its floor in 46.0 percent, with median feasible share 79.24 percent, minimum 53.75 percent, worst decile mean shortfall 1,911,850 tonnes and mean shortfall 459,096 tonnes; over 50 ten year window samples it holds in 48.0 percent, with median 79.98 percent, minimum 75.34 percent, worst decile mean shortfall 497,301 tonnes and mean shortfall 158,509 tonnes. The version 4.1 mixed figure of 65.0 percent is withdrawn: it was flattered by the window half of the sample, exactly as Check 2 item 3.4 warned.

## Summary of the largest numerical changes

| Quantity | Version 4.1 | Version 5 |
| --- | --- | --- |
| Unconstrained expected margin | 403,078,762,407 | 559,713,476,348 |
| Margin at the 80 percent level | 175,143,528,384 | 291,102,590,296 |
| Cost of the 80 percent guarantee | 227,935,234,023 | 268,610,886,052 |
| Ceiling | 80.25 percent | 82.41 percent |
| Historical pattern expected margin | 86,006,146,997 | 144,167,922,884 |
| Highest ladder level the pattern holds | claimed none; measured 60 | 65 |
| EVPI at the 80 percent level | 23,784,104,809 | 13,458,470,835 |
| Penalised VSS | 7,607,863,594, inconsistent definition | 75,931,039,486, consistent definition |
| Robustness hold share | 65.0 percent, mixed sample | 46.0 percent single years; 48.0 percent windows |

Attribution, stated once and plainly: the margin increases come almost entirely from Repair 1, the price vintage, with a smaller contribution from Repair 2 through the yield layers. The ceiling increase comes from Repair 2, the narrower quartile bands raising the low yield layer, with Repair 5 contributing nothing to it because the drought budget never bound. The pattern and robustness corrections move in the opposite direction to the price effect, which is why they are printed beside it rather than behind it.
