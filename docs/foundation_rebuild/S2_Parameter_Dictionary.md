# S2 parameter dictionary for the Nile Delta model

Stage S2 of the foundation rebuild, written 15 November 2026. This dictionary lists every parameter that enters the generating model, src/allocation_model_v4_1.py, and the forecasting module, src/forecasting.py, that feeds it. Each entry gives the value or range, the unit, the location, the season, the year, the source, the transformation applied, and a status. Status words: observed means the value sits in a named source as published; computed means project arithmetic on observed values, with the operation stated; forecast means the output of the forecasting module with its backtest error; assumed means a judgment, a calibration or a substitution chosen by the project; gap means no defensible value exists and the entry states what the model does instead.

Currency basis for every money figure in the model: nominal Egyptian pounds of the year named in the entry. No figure is adjusted for inflation anywhere in the build, so prices, costs and margins from different years are combined in nominal terms. Source identifiers refer to the S2 source register in this folder.

## 1. Land

### Physical cultivated area, by governorate

* Value, hectares, 2020 to 2021: Beheira 387,541; Sharkia 375,274; Dakahlia 271,077; Kafr El Sheikh 228,118; Gharbia 159,439; Menoufia 141,087; Qalyubia 66,784; Damietta 47,260. Total 1,676,580. Exact values sit in the source file.
* Unit and location: hectares, each of the eight governorates. Season: the physical stock, binding in every season pool. Year: agricultural year 2020 to 2021.
* Source: register entry 4, measure cultivated area, Ministry Agricultural Statistics Bulletin Part 2, Table 17.
* Transformation: feddan as published times 0.42.
* Status: observed.

### Annual cropped area, by governorate

* Value, hectares, 2020 to 2021: total 3,176,474 across the eight governorates.
* Role: a descriptor of the year and the base from which the unmodeled crop area is computed. It constrains nothing directly.
* Source: register entry 4, measure total cropped area, Table 19 of the same bulletin. Transformation and status: as above, observed.

### Baseline observed areas, by crop and governorate

* Wheat and sugar beet, winter, 2020 to 2021: register entry 1, Tables 2 and 12. Status: observed.
* Rice and summer maize, summer, 2020 to 2021: register entry 1, Tables 20 and 22. Status: observed, with one exception below.
* Menoufia rice area, summer: the 2020 to 2021 source table carries no Menoufia row. The model substitutes the published 2019 to 2020 value of 19 feddan, equal to 7.98 hectares, from register entry 1, Table 20 of the 2019 to 2020 bulletin. Status: observed for a different year, substituted. The value is two orders of magnitude below every other governorate (the next smallest is Qalyubia at 5,400 feddan in the same table) and is carried as published.
* Nili maize, 2020 to 2021: register entry 13, Tables 27, 28 and 30. Published for four governorates; the other four are absent in the source and enter the baseline as zero area because no row exists. Status: observed where published; absent in source elsewhere.
* Potatoes, winter, summer and Nili, 2021 to 2022: register entry 15, Tables 76, 77 and 78. Nili potatoes are published for Beheira only (1,252 feddan). Status: observed where published; absent in source elsewhere. Note the year differs from the rest of the baseline: the potato areas are 2021 to 2022, every other baseline area is 2020 to 2021, because the season split exists on disk only for 2021 to 2022.

### Seasonal reserve and pool land limits

* Construction, computed in the loader: the annual unmodeled crop area of a governorate is its annual cropped area minus the total observed modeled area. That amount is split across the winter, summer and Nili pools in proportion to the observed modeled area in each pool. Each pool reserve is then capped at the physical area the observed modeled pattern leaves free in that pool. The pool limit is the physical cultivated area minus the capped reserve.
* Status: assumed construction. No file on disk gives a seasonal total for all crops, so the seasonal reserve is built, not observed. Its one consistency property is stated in the code and verified in every run log: no pool limit falls below the observed modeled area of that pool, so the historical pattern is feasible against every limit (24 of 24 pools pass).

### Crop area caps, sensitivity runs only

* Value: share of physical cultivated area, by crop: wheat 0.50; sugar beet 0.30; rice 0.35; summer maize 0.40; Nili maize 0.40; potatoes 0.15 in each season.
* Role: applied only in the caps runs. The primary run carries no caps.
* Source: none. Status: assumed judgment, carried from earlier model versions.

## 2. Yields

### Published district yields, the primary basis

* Value: tonnes per hectare, by governorate and crop, 2020 to 2021, from register entry 3, with potato yields by season from register entry 15 (2021 to 2022). Production weighted means across the eight governorates, computed in S2 from the panel and matching the foundation: wheat 6.87; rice 9.14 over the seven governorates that report rice; summer maize 8.79; sugar beet 49.37; potatoes, all seasons in the panel, 28.39.
* Transformation: tons per feddan as published divided by 0.42.
* Status: observed. No rescaling to any national figure is applied in the primary run. The rescaled construction of version 4 survives only as a labelled sensitivity inside the code.
* District yield normalisation, stated because the brief asks: there is none in the primary run. The model uses the published district yields directly. The only normalisation like operation is the fill rule below.

### Yield fills for blank source cells

* Rule, computed in the loader: a missing district yield is filled with the area weighted mean of the published district yields for that crop, weighted by baseline areas.
* Cells filled, all recorded in the run logs: rice in Menoufia, 9.138 tonnes per hectare; Nili maize in Kafr El Sheikh, Menoufia, Qalyubia and Damietta, 8.358 tonnes per hectare; Nili potatoes in Sharkia, Dakahlia, Kafr El Sheikh, Gharbia, Menoufia, Qalyubia and Damietta, 18.12 tonnes per hectare, which is the single published Nili potato yield (Beheira) carried to the other seven.
* Status: computed fill. The fills are recorded in code and in run logs, not in any data file. The Nili potato fills are inert in the baseline, because those governorates have no Nili potato area, but they are live in any optimised plan that plants Nili potatoes there. One inconsistency is named: Menoufia rice area comes from 2019 to 2020 while its yield is this cross governorate fill, although Menoufia has a published 2019 to 2020 yield of 8.395 tonnes per hectare in register entry 3, which the loader does not use.

### National yield forecasts and the yield layer

* Values, tonnes per hectare, target season 2025, from register Part 2, forecast_prices_yields_v4.csv: wheat 6.679 (random forest; band 6.485 to 7.148; backtest RMSE 0.325, MAPE 4.05 percent); rice paddy 9.132 (naive last value; band 8.822 to 9.359; RMSE 0.270, MAPE 2.12 percent); maize 7.683 (random forest; band 7.382 to 8.206; RMSE 0.691, MAPE 6.16 percent); sugar beet 56.057 (random forest; band 51.131 to 59.539; RMSE 5.892, MAPE 6.39 percent); potatoes 31.516 (ridge; band 30.312 to 32.419; RMSE 1.488, MAPE 3.10 percent).
* Source series: register entry 9, FAOSTAT crops domain, December 2025 vintage, 1961 to 2024.
* Role in the primary run: the forecasts themselves do not enter. Only their band ratios enter: the low yield state multiplies each published district yield by band low divided by forecast, the high state by band high divided by forecast, and the expected state uses the published yields unchanged. Status: forecast derived ratios on an observed base.

## 3. Prices

### Price forecasts, the model price layer

* Values, Egyptian pounds per tonne, target year 2024, drift model selected for all five crops, from forecast_prices_yields_v4.csv: wheat 10,296.94 (band 9,500.80 to 12,951.11; backtest RMSE 1,485.60, MAPE 14.61 percent); rice paddy 19,394.14 (band 19,324.81 to 23,480.32; RMSE 3,735.60, MAPE 14.47 percent); maize 14,836.22 (band 14,561.64 to 19,061.05; RMSE 1,998.12, MAPE 15.64 percent); sugar beet 820.52 (band 793.52 to 972.06; RMSE 92.26, MAPE 10.21 percent); potatoes 8,405.44 (band 8,143.20 to 9,609.40; RMSE 1,396.76, MAPE 19.52 percent).
* Source series: register entry 10, FAOSTAT producer prices, farm gate concept, 1991 to 2023. The sugar beet figure is the farm gate concept. Rice is paddy rice.
* Transformation: rolling origin backtest over the series; the drift model won for every crop against ridge, random forest, gradient boosting and the naive last value line; the band is the spread of one step backtest errors, between the 10th and 90th percentile error quantiles as set in the forecasting module.
* Status: forecast. Known defect, stated here because the dictionary must carry it: observed 2024 farm gate prices exist in the December 2025 FAOSTAT vintage for wheat (17,380), maize (19,942) and potatoes (10,446), mined in the second sweep, but the prices file on disk was never updated, so the model prices are forecasts of a year whose outcome is already published for three of five crops. The forecasts sit below the observed values by 41 percent for wheat, 26 percent for maize and 20 percent for potatoes. See the data quality report, finding 1.

### Sugar beet factory price, alternate run only

* Value: 2,400 pounds per tonne at 16 percent sugar content, before bonuses, season 2024 to 2025.
* Source: register entry 16. Status: observed as announced.
* Role: replaces the farm gate forecast only in the beet2400 run. The two beet prices are different concepts (farm gate against factory procurement) and different years move with the concept, so no comparison between the runs attributes their difference to the price concept alone.

### Price and yield layer probabilities

* Value: low 0.25, expected 0.50, high 0.25, applied to both the price layer and the yield layer, which move together inside a scenario.
* Status: assumed judgment. The model header describes the reading as treating the forecast band as quartiles. A mismatch is named: the forecasting module builds the band from the 10th and 90th percentile backtest errors, so the band edges are not quartiles, and the tail probability of 0.25 on each side does not match the band construction. The two modules state different conventions for the same band.

## 4. Costs

### Official 2022 costs, the model cost basis

* Values, pounds per hectare, rent included, nominal: wheat 37,742.86 (winter 2021 to 2022); sugar beet 39,454.76 (winter 2021 to 2022); rice 41,850.00 (summer 2022); summer maize 37,671.43 (summer 2022); Nili maize 37,888.10 (summer 2022); summer potatoes 86,657.14 (summer 2022); Nili potatoes 54,176.19 (summer 2022).
* Source: register entry 11, Ministry Bulletin of Cost Statistics and Net Return, national general average rows. Tables: Part 1 Table 2 and Table 9; Part 2 Tables 2, 3, 4, 18 and 19.
* Transformation: pounds per feddan as published divided by 0.42. The values enter the model as constants in the code; S2 verified each against the file to the cent.
* Status: observed. Location basis: national general average, applied to all eight governorates alike, although the bulletin also publishes governorate level costs that the model does not use.

### Winter potato cost

* Status: gap. No winter potato table exists in Part 1 of the cost bulletin; potatoes appear only as summer and Nili crops in Part 2. The cost cells on the winter rows of register entry 15 are empty and name this gap.
* What the model does: the primary run substitutes the summer potato cost, 86,657.14 pounds per hectare, for winter potatoes, stated as an assumption in the code and in every run header. A sensitivity repeats key levels at the Nili cost of 54,176.19. The gap therefore moves winter potato margins by up to 32,480.95 pounds per hectare between the two stated choices.

### Costs after 2022

* Status: gap. The Ministry catalogue for the cost bulletin ends at 2022 and no official cost table exists for 2023 onward. The model makes no attempt to carry costs forward: its margin basis is 2024 level prices against 2022 costs, stated in the code header. Any reading of the margins as a single year margin is wrong; they are a stated composite.

## 5. Water

### Applied water duties

* Values, cubic metres per hectare, applied basis: wheat 5,126; rice 16,600; summer maize 9,305; Nili maize 7,433.
* Source: register entry 6, the Abdelwahab and coauthors (2024) rows printing the CAPMAS (2017) requirements: 2,153, 6,972, 3,908 and 3,122 cubic metres per feddan. This is a second hand printing of an official table that could not be read in its original form. The source labels the figures water requirement without stating net or gross; the foundation treats them as applied, and the model follows that treatment.
* Transformation: per feddan values divided by 0.42. The values enter the model as constants; S2 verified them exactly against the file.
* Status: observed as published in the printing, on a basis the source does not state.

### Sugar beet duty

* Value: 6,100 cubic metres per hectare in the primary run.
* Source: the arbitrated range of 5,600 to 6,600, built in the second sweep from five Sakha field trials and two modelled sets read in the original (applied water 4,940 to 7,500 per hectare across the trials). The two foundation extremes, 9,426 from the CAPMAS printing and 3,927 net from Gabr (2022), fall outside every Egyptian source found and are not used.
* Status: assumed midpoint of an observed range. The range ends, 5,600 and 6,600, are run as sensitivities on the ceiling.

### Potato duties

* Winter potatoes: 4,079 cubic metres per hectare; summer potatoes: 6,145. Source: register entry 6, the Abdelwahab rows (1,713 and 2,581 cubic metres per feddan, divided by 0.42). Status: observed as published in the printing.
* Nili potato water: status gap. No Nili potato water figure exists in any source the project holds; the water cells on the Nili rows of register entry 15 are empty and name the gap. What the model does: substitutes the summer duty of 6,145, stated in the code.

### Yield response factors (Ky)

* Values, dimensionless, seasonal: wheat 1.05; maize 1.25 for both seasons; sugar beet 1.00; potatoes 1.10 in all three seasons.
* Source: register entry 8, FAO Paper 56 Table 24 and FAO Paper 66 Table 1, both summarising FAO Paper 33 (1979). Status: observed in the secondary tables. The 1979 original was not read.
* Rice Ky: value used 1.20. Status: gap, carried labelled unverified in the code. Neither secondary table carries a seasonal rice value, and a weakly hosted paper attributes 1.2 to the vegetative stage of rice in Paper 33, so the value may be a stage value mistaken for a seasonal one. The ceiling is run at 1.00 and 1.40 as sensitivities around it.

### Model area water budget

* Anchor: 11.00 billion cubic metres for the eight governorates in the normal state. Status: assumed calibration, carried from version 3. No official water budget exists for the model area, and no source reached publishes Delta releases by year. The anchor is set, in the words of the foundation, just under the water demand of the current cropping pattern.
* District split: each governorate receives the state budget in proportion to its physical cultivated area. Status: assumed split. No published district allocation series exists.
* Satellite check: register entry 18 gives measured whole governorate consumption of 24.081 to 24.802 billion cubic metres per year for 2018 to 2025. It is not a parameter: no value in the model is derived from it, and the two quantities are on different bases (consumption over all surfaces against applied duties for five crops), so no conversion between them is defensible on the files held.

### Inflow states, ratios and probabilities

* Source series: register entry 12, gauged flow at Aswan, 1871 to 1970, mean 91.935 billion cubic metres.
* Construction, computed in the loader under Derivation A of the foundation: band edges at 0.85 and 1.08 of the record mean. Dry: the 23 years below the low edge, mean ratio 0.7807. Normal: the 45 years inside the band, mean ratio 0.9547. High: the 32 years above the high edge, mean ratio 1.2213. Drought: a fourth state built from ten year window means; its ratio is the lowest window mean ratio, 0.8709, and its raw probability is the share of the 91 windows at or below that ratio, which is one window, 0.0110. The three single year probabilities (0.23, 0.45, 0.32) are scaled by one minus the drought share, giving dry 0.2275, normal 0.4451, high 0.3165, drought 0.0110, summing to one.
* Budgets, billion cubic metres, anchor times ratio: dry 8.588; normal 10.502; high 13.434; drought 9.580.
* Status: computed from the observed record, under two assumed choices: the band edges, and the drought construction. One property must travel with the numbers: the drought budget (9.580) is larger than the dry budget (8.588), because the worst ten year mean is less severe than the mean of single dry years. The drought state is a persistence state, not the driest state.
* Layer combination: the four inflow states combine with the three price and yield layer states into twelve scenarios, with independence between the inflow layer and the price and yield layer stated in the code as a named assumption. Scenario probabilities are the products of the two layers and sum to one (verified in S2).

## 6. Model settings that act as parameters

* Minimum viable water share: 0.30. A kept crop must receive at least 30 percent of its full duty. Status: assumed, stated in the code. Abandonment is the alternative: water zero, output zero, planting cost sunk.
* Floor penalty for the penalised variant: 25,000 pounds per tonne of staple shortfall. Status: assumed, named wherever the penalised value of the stochastic solution is printed.
* Stress budget scales: 0.90 and 0.80 of the state budgets. Status: assumed scenario choices.
* Robustness sampling: 100 samples, alternating random single years and random ten year window means drawn from the 1871 to 1970 record, seed 20261114, so the run reproduces exactly. Status: computational setting, recorded in the code and in robustness_samples_v4_1.csv.
* Reference tonnage: 12,254,407 tonnes of aggregate wheat, paddy rice and summer maize, computed as baseline areas times published district yields (wheat 4,617,795; rice 4,086,080; summer maize 3,550,533). Status: computed. The guarantee floors are shares of this quantity.
* Solver scaling: water is carried inside the solver in thousand cubic metres (duties and budgets divided by 1000) after an earlier build found that CBC returned suboptimal solutions labelled optimal at full scale. Printed figures are converted back to cubic metres. Status: computational setting, verified dimensionally in S2: the production term multiplies yield by Ky divided by the scaled duty and by the scaled water variable, which returns tonnes.
* Solver tolerance: CBC primal and dual feasibility tolerance of 0.0000001, the CBC default, held deliberately after a tighter setting of 0.000000001 made presolve falsely prove a feasible fixed plan infeasible during the build. Relative gap zero. Status: computational setting, recorded in the code.

## 7. Forecasting module settings and the fertilizer gap

* Candidates raced per crop and target: ridge regression, random forest, gradient boosting, naive last value and drift. Selection is per crop by rolling origin backtest score: prices use at least ten test seasons from a first training end of 2010; yields use a first training end of 2000 over the 1961 to 2024 series. Features use only information available before the season forecast: lagged values, a time trend, lagged planted area, and lagged fertilizer price where a series exists. Random state 42.
* Fertilizer price feature: status gap. The design names a lagged fertilizer price feature, but the only Pink Sheet file the project holds (register entry 14) contains wheat, rice and maize prices and no fertilizer series. The loader therefore returns no fertilizer series and the feature is absent from every fit. The absence is recorded in the forecasting run log, not hidden. Consequence: the fitted models use lagged values, trend and lagged area only, and any claim that fertilizer prices inform the forecasts would be false.
* Outlier handling: none. Two published values are flagged in the code, maize yield in 2019 (4.9513 tonnes per hectare against 7.5 to 7.8 in the neighbouring years) and sugar beet yield in 2020 (72.8148 against about 48 to 50), both flag A in the source and both kept exactly as published. The backtest code computes scores with the outlier origin removed as a recorded sensitivity, so the effect of each on model selection can be read from backtest_scores_v4.csv and the run log.
