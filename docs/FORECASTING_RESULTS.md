# Forecasting results, version 4

This document reports the forecasting module built to Section 6 of docs/FOUNDATIONS.md and Part 2.1 of docs/REASSESSMENT_AND_UPGRADE_DESIGN.md. It gives the full backtest record for next season producer prices and next season national yields for wheat, rice paddy, maize, sugar beet and potatoes, the model selected for each crop, the forecast that the allocation model will consume, and the treatment of production costs after 2022. Every forecast in this document is printed beside its own backtest error. A forecast without its error beside it does not enter the model, and none does here.

## 1. Method in brief

1. Two targets per crop: producer price in Egyptian pounds per tonne, and national yield in tonnes per hectare.
2. Five candidate models per crop and target: ridge regression, random forest, gradient boosting, naive last value carried forward, and a drift line. The drift forecast is the last observed value plus the mean change per observed step over the training window, times the horizon.
3. Features for the three machine learning models use only information available before the season being forecast: the target value lagged one, two and three observed seasons, a time trend given by the target calendar year, and planted area lagged one calendar year from the FAOSTAT crops pull. The fertilizer feature is treated in Section 2.4 below.
4. The three machine learning models are fitted to the natural log of the target, and their predictions are returned to the original scale before scoring. Prices in this project grow multiplicatively, and a levels fit extrapolates that growth explosively when it is refitted on the full sample. The log specification is the standard repair, it keeps every forecast positive, and all scores are computed on the original scale so that every model is judged on one basis.
5. Backtests are rolling origin with an expanding training window. The primary horizon is one step ahead. Prices: first training window 1991 to 2010, test seasons 2011 to 2023. Yields: first training window 1961 to 2000, test seasons 2001 to 2024. Two step ahead scores are reported as a secondary table in Section 7.
6. Scores are root mean squared error (RMSE), mean absolute error (MAE), mean absolute percentage error (MAPE), and skill against naive last value, defined as the model RMSE divided by the naive last value RMSE. A skill above one means the model lost to carrying last season forward.
7. Model selection is per crop and per target, by lowest one step backtest RMSE. The naive lines compete on the same basis as the machine learning models, and where a naive line wins, it is selected and the report says so.
8. The band around each forecast is the forecast shifted by the empirical 10th and 90th percentiles of the selected model one step backtest residuals, where a residual is the actual value minus the forecast. Bands are therefore asymmetric whenever the residual distribution is asymmetric, which for prices it is, because policy jump years produce large misses in one direction.

## 2. Data and handling statements

### 2.1 Prices

Source: data/external/faostat_producer_prices_egypt.csv, FAOSTAT prices domain, Egyptian pounds per tonne. In this vintage every crop runs 1991 to 2023 and no annual price for 2024 is published for any of the five crops, so the forecast season for prices is 2024 and the last observed year is 2023 for all five crops. Wheat, maize and potatoes have no missing years. Rice paddy and sugar beet are treated in Section 2.3.

### 2.2 Yields and planted area

Source: data/external/faostat_crops_egypt.csv, the direct FAOSTAT crops domain pull. Yields and area harvested run 1961 to 2024 for wheat, rice paddy, maize and potatoes. Sugar beet yield is first published in 1979, so for sugar beet the first training window is in practice 1979 to 2000 and the test window is still 2001 to 2024. The forecast season for yields is 2025 and the last observed year is 2024 for all five crops.

### 2.3 The price hole for rice paddy and sugar beet, 2019 to 2021

Rice paddy and sugar beet producer prices have no published value for 2019, 2020 or 2021. The handling is fixed and is implemented in the code, not only described here. The two series are carried in observed year order. A lag means the previous observed year. Missing years are never training targets and are never scored, and no value is interpolated into the hole. Training for every origin uses observed years only, skipping the missing years. The test seasons for rice paddy and sugar beet prices are therefore the ten observed seasons 2011 to 2018, 2022 and 2023. One consequence is stated plainly: for these two crops the step into 2022 spans four calendar years, so that origin is a longer horizon in calendar time than its neighbours, and it is scored as published on the same basis as every other origin.

### 2.4 The fertilizer feature: a named gap

The design names a lagged fertilizer price as a feature, sourced from the World Bank Pink Sheet. The Pink Sheet file held in this project, data/external/pink_sheet_crosscheck.csv, contains no fertilizer series at all. It holds only international reference prices for wheat, maize and Thai milled rice for 2022 to 2025, which are not Egyptian farm gate prices and cover four years at the end of the sample. No lagged fertilizer feature can be built for a backtest that starts in 2011, and no substitute series has been invented. The models in this run therefore use lagged target values, the time trend and lagged planted area only. The code builds the lagged fertilizer column automatically if a fertilizer series is supplied in the expected place, so the feature enters the next run without a redesign when a real series is pulled. This is a named gap: the cost of the gap is that the price models have no input cost signal, which is one plausible reason, stated as a reason and not as a finding, why no machine learning model beat the naive lines on prices.

### 2.5 The two published yield outliers: scored as published

The provenance file for the crops pull flags two published values that stand out: maize yield in 2019, at 4.9513 tonnes per hectare against 7.7767 in 2020 on nearly unchanged production, and sugar beet yield in 2020, at 72.8148 tonnes per hectare against 48.1588 in 2019 and 49.4826 in 2021. Both values are kept exactly as published, with flag A in the source. Origins whose target year is one of those years are scored as published and count in full in every headline score in this document. Origins that use those years as lag inputs also use them as published. Nothing is dropped and nothing is smoothed. As a sensitivity only, Section 6 reports the selected model RMSE for maize and sugar beet yields with the single outlier origin removed, so a reader can see how much of each score that one origin carries. The headline selection never uses the sensitivity figures.

### 2.6 Failures

No model failed to fit for any crop in this run. If a model class fails for a crop in a future run, for example because too few observations remain after hole handling, the module records it in the score table with status failed and the reason, rather than dropping it. That behaviour is implemented in src/forecasting.py and the run log prints every failure note it records.

## 3. Backtest scores, prices, one step ahead

Prices in Egyptian pounds per tonne. Test seasons: 13 for wheat, maize and potatoes (2011 to 2023); 10 for rice paddy and sugar beet (observed seasons only, see Section 2.3).

| Crop | Model | Test seasons | RMSE | MAE | MAPE (percent) | Skill vs naive | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| wheat | ridge | 13 | 3,182.85 | 2,221.16 | 54.14 | 2.079 | ok |
| wheat | random_forest | 13 | 1,758.37 | 1,187.98 | 23.23 | 1.149 | ok |
| wheat | gradient_boosting | 13 | 1,617.74 | 1,091.24 | 21.28 | 1.057 | ok |
| wheat | naive_last | 13 | 1,530.83 | 899.20 | 14.99 | 1.000 | ok |
| wheat | drift | 13 | 1,485.60 | 886.17 | 14.61 | 0.970 | ok |
| rice_paddy | ridge | 10 | 39,725.80 | 13,868.96 | 87.91 | 10.394 | ok |
| rice_paddy | random_forest | 10 | 5,788.05 | 2,976.30 | 30.17 | 1.514 | ok |
| rice_paddy | gradient_boosting | 10 | 3,841.66 | 1,724.26 | 16.26 | 1.005 | ok |
| rice_paddy | naive_last | 10 | 3,822.15 | 1,692.30 | 15.36 | 1.000 | ok |
| rice_paddy | drift | 10 | 3,735.60 | 1,615.22 | 14.47 | 0.977 | ok |
| maize | ridge | 13 | 2,436.93 | 1,345.15 | 27.95 | 1.172 | ok |
| maize | random_forest | 13 | 3,002.56 | 1,739.46 | 27.31 | 1.444 | ok |
| maize | gradient_boosting | 13 | 2,649.77 | 1,471.13 | 21.42 | 1.274 | ok |
| maize | naive_last | 13 | 2,079.30 | 1,153.89 | 16.64 | 1.000 | ok |
| maize | drift | 13 | 1,998.12 | 1,102.57 | 15.64 | 0.961 | ok |
| sugar_beet | ridge | 10 | 235.07 | 165.95 | 30.45 | 2.368 | ok |
| sugar_beet | random_forest | 10 | 149.13 | 116.64 | 21.30 | 1.502 | ok |
| sugar_beet | gradient_boosting | 10 | 109.33 | 78.91 | 14.58 | 1.101 | ok |
| sugar_beet | naive_last | 10 | 99.26 | 56.60 | 10.35 | 1.000 | ok |
| sugar_beet | drift | 10 | 92.26 | 56.36 | 10.21 | 0.929 | ok |
| potatoes | ridge | 13 | 65,985.14 | 25,478.69 | 428.17 | 46.332 | ok |
| potatoes | random_forest | 13 | 2,040.52 | 1,307.20 | 27.32 | 1.433 | ok |
| potatoes | gradient_boosting | 13 | 1,485.15 | 894.90 | 21.01 | 1.043 | ok |
| potatoes | naive_last | 13 | 1,424.18 | 859.00 | 20.56 | 1.000 | ok |
| potatoes | drift | 13 | 1,396.76 | 810.90 | 19.52 | 0.981 | ok |

## 4. Backtest scores, yields, one step ahead

Yields in tonnes per hectare. Test seasons: 24 for every crop (2001 to 2024).

| Crop | Model | Test seasons | RMSE | MAE | MAPE (percent) | Skill vs naive | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| wheat | ridge | 24 | 0.5652 | 0.4751 | 7.47 | 1.668 | ok |
| wheat | random_forest | 24 | 0.3250 | 0.2604 | 4.05 | 0.959 | ok |
| wheat | gradient_boosting | 24 | 0.3638 | 0.2474 | 3.85 | 1.074 | ok |
| wheat | naive_last | 24 | 0.3388 | 0.2181 | 3.44 | 1.000 | ok |
| wheat | drift | 24 | 0.3476 | 0.2273 | 3.60 | 1.026 | ok |
| rice_paddy | ridge | 24 | 0.5975 | 0.5347 | 5.70 | 2.216 | ok |
| rice_paddy | random_forest | 24 | 0.3529 | 0.2801 | 2.98 | 1.309 | ok |
| rice_paddy | gradient_boosting | 24 | 0.3164 | 0.2321 | 2.48 | 1.174 | ok |
| rice_paddy | naive_last | 24 | 0.2696 | 0.1981 | 2.12 | 1.000 | ok |
| rice_paddy | drift | 24 | 0.2840 | 0.2085 | 2.23 | 1.053 | ok |
| maize | ridge | 24 | 0.9796 | 0.6970 | 10.19 | 1.167 | ok |
| maize | random_forest | 24 | 0.6912 | 0.4119 | 6.16 | 0.824 | ok |
| maize | gradient_boosting | 24 | 0.7551 | 0.4718 | 6.92 | 0.900 | ok |
| maize | naive_last | 24 | 0.8391 | 0.4500 | 6.64 | 1.000 | ok |
| maize | drift | 24 | 0.8539 | 0.4685 | 6.93 | 1.018 | ok |
| sugar_beet | ridge | 24 | 7.0892 | 4.4009 | 8.15 | 0.924 | ok |
| sugar_beet | random_forest | 24 | 5.8925 | 3.5418 | 6.39 | 0.768 | ok |
| sugar_beet | gradient_boosting | 24 | 7.8735 | 4.9946 | 9.27 | 1.026 | ok |
| sugar_beet | naive_last | 24 | 7.6717 | 4.0271 | 7.36 | 1.000 | ok |
| sugar_beet | drift | 24 | 7.8016 | 4.0217 | 7.39 | 1.017 | ok |
| potatoes | ridge | 24 | 1.4879 | 0.8369 | 3.10 | 0.926 | ok |
| potatoes | random_forest | 24 | 1.7060 | 1.3056 | 4.77 | 1.062 | ok |
| potatoes | gradient_boosting | 24 | 1.9122 | 1.2815 | 4.61 | 1.190 | ok |
| potatoes | naive_last | 24 | 1.6069 | 0.9645 | 3.52 | 1.000 | ok |
| potatoes | drift | 24 | 1.5995 | 0.9144 | 3.34 | 0.995 | ok |

## 5. Selection and forecasts

Selection metric: lowest one step backtest RMSE, per crop and per target.

| Crop | Target | Selected model | Backtest RMSE | Skill vs naive | Reading |
| --- | --- | --- | --- | --- | --- |
| wheat | price | drift | 1,485.60 | 0.970 | Naive family line won |
| rice_paddy | price | drift | 3,735.60 | 0.977 | Naive family line won |
| maize | price | drift | 1,998.12 | 0.961 | Naive family line won |
| sugar_beet | price | drift | 92.26 | 0.929 | Naive family line won |
| potatoes | price | drift | 1,396.76 | 0.981 | Naive family line won |
| wheat | yield | random_forest | 0.3250 | 0.959 | Machine learning model beat naive |
| rice_paddy | yield | naive_last | 0.2696 | 1.000 | Naive family line won |
| maize | yield | random_forest | 0.6912 | 0.824 | Machine learning model beat naive |
| sugar_beet | yield | random_forest | 5.8925 | 0.768 | Machine learning model beat naive |
| potatoes | yield | ridge | 1.4879 | 0.926 | Machine learning model beat naive |

| Crop | Target | Last observed year | Last observed value | Forecast season | Forecast | Band low | Band high | Backtest RMSE | Backtest MAE | Backtest MAPE (percent) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| wheat | price | 2023 | 10,000.00 | 2024 | 10,296.94 | 9,500.80 | 12,951.11 | 1,485.60 | 886.17 | 14.61 |
| rice_paddy | price | 2023 | 18,761.00 | 2024 | 19,394.14 | 19,324.81 | 23,480.32 | 3,735.60 | 1,615.22 | 14.47 |
| maize | price | 2023 | 14,400.00 | 2024 | 14,836.22 | 14,561.64 | 19,061.05 | 1,998.12 | 1,102.57 | 15.64 |
| sugar_beet | price | 2023 | 795.00 | 2024 | 820.52 | 793.52 | 972.06 | 92.26 | 56.36 | 10.21 |
| potatoes | price | 2023 | 8,160.00 | 2024 | 8,405.44 | 8,143.20 | 9,609.40 | 1,396.76 | 810.90 | 19.52 |
| wheat | yield | 2024 | 6.7777 | 2025 | 6.6789 | 6.4854 | 7.1477 | 0.3250 | 0.2604 | 4.05 |
| rice_paddy | yield | 2024 | 9.1315 | 2025 | 9.1315 | 8.8217 | 9.3594 | 0.2696 | 0.1981 | 2.12 |
| maize | yield | 2024 | 7.5853 | 2025 | 7.6834 | 7.3823 | 8.2055 | 0.6912 | 0.4119 | 6.16 |
| sugar_beet | yield | 2024 | 52.4121 | 2025 | 56.0570 | 51.1310 | 59.5386 | 5.8925 | 3.5418 | 6.39 |
| potatoes | yield | 2024 | 30.0944 | 2025 | 31.5165 | 30.3124 | 32.4186 | 1.4879 | 0.8369 | 3.10 |

## 6. What the results say

* Prices: the drift line is selected for all five crops. Its margin over naive last value is thin everywhere, with skill between 0.93 and 0.98. No machine learning model beat naive last value on RMSE for any price series. The honest reading is that Egyptian farm gate prices one season ahead are barely forecastable from their own history, a planted area line and a trend, and the wide bands in the forecast table are the correct expression of that. The allocation model should consume these price forecasts as weak evidence with wide scenario bands, not as points.
* Ridge regression is unstable for prices in this specification and lost heavily where it lost: skill 2.08 for wheat, 10.39 for rice paddy and 46.33 for potatoes, with a MAPE of 428.17 percent for potatoes. It is printed in full because the rule of this module is that losers ship in the table.
* Yields: a machine learning model is selected for four of five crops, random forest for wheat, maize and sugar beet, and ridge for potatoes, with skill between 0.77 and 0.96. For rice paddy yield nothing beat naive last value: every machine learning model lost, with skill from 1.17 to 2.22, so the selected forecast is the naive line itself and its band is the narrowest in the table, which matches a series that moves slowly year to year.
* Naive family selections: six of the ten selections are naive family lines, drift for all five prices and naive last value for rice paddy yield. This is a finding of the module, not a defect of it. The design gate said in advance that this outcome would be reported rather than repaired away, and it is reported here.
* Sugar beet yield forecast: the selected random forest forecast of 56.06 tonnes per hectare sits above the last observed value of 52.41 and above every observed year except the 2020 published outlier, which sits in the training targets as published. The band of 51.13 to 59.54 is correspondingly wide. A reader should weight this forecast by its RMSE of 5.89 and by the sensitivity line below before using it for anything beyond the allocation scenario band it was built for.
* Outlier sensitivity, selected models, headline scores unchanged: maize yield, origin 2019, actual 4.9513, selected model forecast 7.7164; RMSE without that single origin is 0.4075 on 23 origins against a headline 0.6912 on 24. Sugar beet yield, origin 2020, actual 72.8148, selected model forecast 49.2843; RMSE without that single origin is 3.4868 on 23 origins against a headline 5.8925 on 24. In both cases one published origin carries a large share of the headline error, and in both cases the headline score is the one that stands.

## 7. Backtest scores, two step ahead, secondary

Two step ahead scores use the same rolling origin design with a two season horizon. Training pairs use only targets at or before the origin. These tables are reported because the design protocol asks for them; no selection and no forecast in this document is taken from them.

### Prices, two step ahead

| Crop | Model | Test seasons | RMSE | MAE | MAPE (percent) | Skill vs naive | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| wheat | ridge | 13 | 3,502.59 | 2,521.77 | 57.86 | 1.897 | ok |
| wheat | random_forest | 13 | 2,123.93 | 1,508.49 | 29.27 | 1.150 | ok |
| wheat | gradient_boosting | 13 | 2,041.21 | 1,286.97 | 22.08 | 1.105 | ok |
| wheat | naive_last | 13 | 1,846.45 | 1,245.38 | 23.35 | 1.000 | ok |
| wheat | drift | 13 | 1,749.07 | 1,167.67 | 20.93 | 0.947 | ok |
| rice_paddy | ridge | 10 | 5,281.53 | 2,775.46 | 31.49 | 0.873 | ok |
| rice_paddy | random_forest | 10 | 6,383.61 | 3,341.50 | 36.25 | 1.055 | ok |
| rice_paddy | gradient_boosting | 10 | 6,059.68 | 3,059.81 | 29.33 | 1.001 | ok |
| rice_paddy | naive_last | 10 | 6,052.49 | 3,038.10 | 28.44 | 1.000 | ok |
| rice_paddy | drift | 10 | 5,941.14 | 2,932.17 | 25.93 | 0.982 | ok |
| maize | ridge | 13 | 1,373.27 | 1,035.68 | 25.70 | 0.439 | ok |
| maize | random_forest | 13 | 3,367.81 | 2,045.68 | 33.64 | 1.077 | ok |
| maize | gradient_boosting | 13 | 3,107.23 | 1,729.21 | 25.51 | 0.994 | ok |
| maize | naive_last | 13 | 3,127.09 | 1,718.46 | 25.34 | 1.000 | ok |
| maize | drift | 13 | 3,006.68 | 1,587.48 | 21.65 | 0.961 | ok |
| sugar_beet | ridge | 10 | 189.64 | 144.39 | 33.01 | 1.355 | ok |
| sugar_beet | random_forest | 10 | 185.48 | 150.21 | 27.91 | 1.325 | ok |
| sugar_beet | gradient_boosting | 10 | 152.46 | 109.03 | 18.48 | 1.089 | ok |
| sugar_beet | naive_last | 10 | 139.98 | 102.60 | 17.66 | 1.000 | ok |
| sugar_beet | drift | 10 | 118.98 | 87.63 | 15.07 | 0.850 | ok |
| potatoes | ridge | 13 | 687,702.11 | 262,821.71 | 3,856.49 | 332.585 | ok |
| potatoes | random_forest | 13 | 2,460.45 | 1,642.74 | 33.07 | 1.190 | ok |
| potatoes | gradient_boosting | 13 | 2,085.57 | 1,215.30 | 24.08 | 1.009 | ok |
| potatoes | naive_last | 13 | 2,067.75 | 1,227.58 | 24.46 | 1.000 | ok |
| potatoes | drift | 13 | 2,017.53 | 1,217.87 | 23.06 | 0.976 | ok |

### Yields, two step ahead

| Crop | Model | Test seasons | RMSE | MAE | MAPE (percent) | Skill vs naive | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| wheat | ridge | 24 | 0.7513 | 0.6374 | 10.03 | 2.147 | ok |
| wheat | random_forest | 24 | 0.3170 | 0.2439 | 3.80 | 0.906 | ok |
| wheat | gradient_boosting | 24 | 0.3535 | 0.2306 | 3.61 | 1.010 | ok |
| wheat | naive_last | 24 | 0.3499 | 0.2382 | 3.74 | 1.000 | ok |
| wheat | drift | 24 | 0.3789 | 0.2719 | 4.30 | 1.083 | ok |
| rice_paddy | ridge | 24 | 0.8541 | 0.7598 | 8.13 | 2.238 | ok |
| rice_paddy | random_forest | 24 | 0.4520 | 0.3660 | 3.90 | 1.184 | ok |
| rice_paddy | gradient_boosting | 24 | 0.4043 | 0.3406 | 3.64 | 1.059 | ok |
| rice_paddy | naive_last | 24 | 0.3817 | 0.3040 | 3.25 | 1.000 | ok |
| rice_paddy | drift | 24 | 0.4179 | 0.3342 | 3.60 | 1.095 | ok |
| maize | ridge | 24 | 1.1557 | 0.8877 | 12.70 | 1.293 | ok |
| maize | random_forest | 24 | 0.7364 | 0.4665 | 6.84 | 0.824 | ok |
| maize | gradient_boosting | 24 | 0.8983 | 0.5250 | 7.62 | 1.005 | ok |
| maize | naive_last | 24 | 0.8939 | 0.5014 | 7.35 | 1.000 | ok |
| maize | drift | 24 | 0.9353 | 0.5753 | 8.41 | 1.046 | ok |
| sugar_beet | ridge | 24 | 7.2918 | 5.0783 | 9.66 | 0.990 | ok |
| sugar_beet | random_forest | 24 | 5.8044 | 3.7007 | 6.75 | 0.788 | ok |
| sugar_beet | gradient_boosting | 24 | 7.5932 | 4.7012 | 8.72 | 1.031 | ok |
| sugar_beet | naive_last | 24 | 7.3667 | 4.1580 | 7.61 | 1.000 | ok |
| sugar_beet | drift | 24 | 7.6617 | 4.4297 | 8.24 | 1.040 | ok |
| potatoes | ridge | 24 | 1.4034 | 0.9534 | 3.62 | 0.877 | ok |
| potatoes | random_forest | 24 | 1.6799 | 1.4571 | 5.42 | 1.050 | ok |
| potatoes | gradient_boosting | 24 | 1.6678 | 1.2786 | 4.71 | 1.042 | ok |
| potatoes | naive_last | 24 | 1.6001 | 1.0424 | 3.83 | 1.000 | ok |
| potatoes | drift | 24 | 1.5202 | 0.8542 | 3.14 | 0.950 | ok |

## 8. Costs after 2022: the gap rule only

Costs are not forecast by this module, and this section states why, what the last official figures are, and what happens after them. The project rule for a stale series is: find it recent, or forecast it from history with the forecast tested on at least ten years and its error printed beside every use, or carry it as a named gap with the cost of the gap stated. Costs fail the forecast branch of that rule on arithmetic alone. The longest official cost run for any crop and season is three seasons, wheat winter and sugar beet winter in the Ministry bulletin below. The CAPMAS bulletin gives 2015 to 2016 and 2016 to 2017, and the seasons 2017 to 2018 and 2018 to 2019 appear in neither file, so the two families do not join into one continuous series. No cost series in this project can be tested on ten years, so no cost forecast with a printed error can exist, and none is printed. Any method that produced post 2022 costs from these points would be pretending a training series exists. It does not.

### 8.1 The 2022 official base

Total production cost including rent, Egyptian pounds per hectare, from the Ministry of Agriculture and Land Reclamation, Economic Affairs Sector, Bulletin of Cost Statistics and Net Return, in data/external/ministry_cost_bulletin_2019_2022.csv. The bulletin names the summer and Nili seasons by the single year 2022 and the winter season by the season label 2021 to 2022.

| Crop | Season | Bulletin season label | Cost including rent (pounds per hectare) | Bulletin table |
| --- | --- | --- | --- | --- |
| wheat | winter | 2021 to 2022 | 37,742.86 | Part 1, Table 2 |
| sugar_beet | winter | 2021 to 2022 | 39,454.76 | Part 1, Table 9 |
| rice_paddy (named rice in the bulletin) | summer | 2022 | 41,850.00 | Part 2, Table 2 |
| maize | summer | 2022 | 37,671.43 | Part 2, Table 3 |
| maize | Nili | 2022 | 37,888.10 | Part 2, Table 4 |
| potatoes | summer | 2022 | 86,657.14 | Part 2, Table 18 |
| potatoes | Nili | 2022 | 54,176.19 | Part 2, Table 19 |

Two gaps inside the base year itself are named. The delivered bulletin extract holds no winter season cost for potatoes, only summer and Nili. And the bulletin crop named rice is the model crop rice paddy; the file keeps the bulletin name and this document maps it once, here.

For context, the older CAPMAS base in data/external/production_costs_egypt.csv, season 2016 to 2017, total cost including rent in Egyptian pounds per hectare: wheat 21,473.81; sugar beet 17,607.14; rice paddy 19,902.38; maize summer 18,933.33; maize Nili 14,040.48; potatoes summer 49,533.33; potatoes Nili 28,159.52.

### 8.2 The wheat anchor as a validation check

One later wheat figure exists outside the bulletin: a government report republished on 30 May 2024 states the total production cost of wheat at about 17,000 pounds per feddan in the 2022 to 2023 season, equal to 40,476.19 pounds per hectare, with land rent of about 4,700 pounds per feddan named as a component. Its use in this project is as a validation check on the join between sources, and as a wheat only continuation. The check is this. Inside the Ministry bulletin, wheat winter cost rose by 10.22 percent in its first step and by 23.53 percent in its second step, reaching 37,742.86 pounds per hectare in the 2021 to 2022 season. The step from that bulletin figure to the anchor is 7.24 percent, a ratio of 1.0724. That step is smaller than both steps inside the bulletin and in the same direction, so the two sources join without the level break that would signal a change of definition or of coverage. Verdict: the anchor is consistent with the bulletin for wheat, and it validates wheat only.

### 8.3 Why the wheat ratio is not applied to other crops

Escalating every crop from its 2022 base by the wheat anchor ratio would assume that costs grow at the wheat rate for every crop. The bulletin itself refutes that assumption with crop specific evidence. Inside the bulletin, sugar beet winter cost rose by 10.33 percent and then by 46.37 percent in the two steps where wheat rose by 10.22 percent and then by 23.53 percent. Over 2020 to 2022, two year cost growth was 68.90 percent for rice, 47.88 percent for maize summer, 96.41 percent for maize Nili, 27.83 percent for potatoes summer and 42.95 percent for potatoes Nili. Growth paths that differ by a factor of three across crops cannot be carried by one ratio. The wheat anchor ratio method is therefore rejected for every crop except as the wheat continuation it actually measures, and no escalated figure for any other crop is printed anywhere in this project on that basis.

### 8.4 Post 2022 treatment, crop by crop

* Wheat: the 2022 to 2023 figure of 40,476.19 pounds per hectare is carried as a reported figure, with its basis stated in Section 8.2. It is not an official bulletin table and is never labelled as one. The same government report states an expected 2023 to 2024 wheat cost of about 22,000 pounds per feddan, equal to 52,380.95 pounds per hectare. That figure is labelled estimate wherever it is used, with this basis: it is a forecast stated inside its own source, no backtest error exists for it, and none is claimed. From 2024 to 2025 onward, wheat cost is a named gap.
* Rice paddy, maize, sugar beet and potatoes: named gap from 2023 onward. No post 2022 cost figure for these crops is printed, estimated or carried in this project, because no published figure was found and no forecast method with a printed error can be built under Section 8.
* The cost of the gap, stated as the rule requires: pound margins for the forecast season cannot be computed for rice paddy, maize, sugar beet or potatoes until a post 2022 official cost source is found. The allocation step must either run those crops on the 2022 official base with this gap printed beside every margin it produces, or wait for the source. Wheat margins may use the two labelled figures above, and their labels travel with them into any table that prints them.

## 9. Files and reproducibility

* Code: src/forecasting.py, run with the project venv python as .venv/bin/python src/forecasting.py from the project root.
* Run log: data/processed/run_forecasting_v4.txt, with the selected model, forecast, band and backtest error for every crop and target.
* Machine readable forecasts: data/processed/forecast_prices_yields_v4.csv, with crop, target, last observed year, forecast season, selected model, forecast value, band low, band high, and the backtest RMSE and MAPE of the selected model.
* Machine readable scores: data/processed/backtest_scores_v4.csv, with every score in Sections 3, 4 and 7.
* Random seeds are fixed in the code, so the run reproduces exactly.
