# V7 Delivery Response Evidence: How Wheat Deliveries Answer the Procurement Price

Date: 17 November 2026
Data file: data/external/v7_delivery_evidence.csv
Code: src/allocation_model_v7.py (the fit is computed there from the data file, and recomputed independently by src/check_v7.py)

## 1. The question

Version 7 treats the wheat procurement price as a decision variable. That needs one behavioural input the earlier versions did not: when the state raises the announced price, how much more of the wheat grown actually arrives at state collection points, instead of going to traders, to home use, or to animal feed? This note assembles the public record on that question, fits the simplest defensible response to it, and labels every place where the record runs out and an assumption takes over.

## 2. The evidence table

Eight seasons, harvest years 2019 to 2026. For each season the table in the data file records the top grade procurement price in pounds per ardeb of 150 kilograms and in pounds per tonne, the tonnage the state bought, national production, the delivery share (bought divided by production), and the farm gate alternative price where one is published. Every cell carries its own named source in the data file. The sources are, in the main, USDA Foreign Agricultural Service Cairo reports (Grain and Feed Annual EG2020-0005 of 15 March 2020, Grain and Feed Update EG2021-0020 of 20 October 2021, Grain and Feed Annual EG2022-0009 of 28 March 2022, Grain and Feed Update EG2023-0025 of 15 November 2023, Grain and Feed Annual EG2025-0009 of 27 March 2025), FAO GIEWS Country Briefs for Egypt (archive briefs to 30 June 2026), the Ministry of Supply and Internal Trade announcement of April 2025, Reuters of 11 June 2026 and 24 October 2026, and the FAOSTAT producer price series of December 2025 vintage already held by this project.

The headline shape of the record:

| Season | Price, pounds per ardeb | Bought, million tonnes | Production, million tonnes | Share delivered |
| --- | --- | --- | --- | --- |
| 2019 | 685 | 3.27 | 8.77 | 0.373 |
| 2020 | 700 | 3.50 | 8.90 | 0.393 |
| 2021 | 725 | 3.60 | 9.00 | 0.400 |
| 2022 | 885 | 4.20 | 9.50 | 0.442 |
| 2023 | 1500 | 3.80 | 8.87 | 0.428 |
| 2024 | 2000 | 3.60 | 9.20 | 0.391 |
| 2025 | 2200 | 4.00 | 9.30 | 0.430 |
| 2026 | 2500 | 4.90 | 10.20 | 0.480 |

## 3. The response variable and the price variable

The response is the delivery share. The price variable is a ratio: the procurement price per tonne divided by the farm gate price of wheat per tonne in the same season, both in pounds. The ratio is the right shape for the farmer decision, because the state price competes with the price the trader and the open market offer for the same tonne. The farm gate series is the FAOSTAT producer price for Egypt, the same series family the model prices come from, observed for 2019 to 2024.

Two warnings travel with this ratio, and neither is hidden. First, in 2022 and 2023 the FAOSTAT farm gate price equals the procurement price exactly (5,900 and 10,000 pounds per tonne), so the ratio reads 1.000 in those years by construction of the sources, not by market observation. The official farm price series appears to be partly administered. Second, in 2022 a ministerial decree required every wheat producer to sell a minimum of 12 ardeb per feddan to government purveyors (USDA EG2022-0009), so part of the 2022 share was required by law rather than chosen at the price. The fit below is therefore a summary of how the share and the price ratio moved together in a short, policy heavy record. It is not a clean market experiment, and version 7 does not present it as one.

## 4. The fit

An ordinary least squares line of delivery share on the price ratio, fitted on the six seasons with a published farm gate price, 2019 to 2024:

share = 0.2611 + 0.1682 times ratio

The slope carries a standard error of 0.0331 and the intercept a standard error of 0.0286. The residual standard deviation is 0.0105 of share, and the line accounts for 0.866 of the variance of the six shares. Read in words: when the state price rises from equal to the farm gate price to 10 percent above it, the fitted share rises by about 1.7 points, from about 0.429 to about 0.446.

Refitted without 2022, the season with the legal delivery requirement, the line is share = 0.2831 + 0.1384 times ratio. The slope falls by about a fifth. The 2022 season is kept in the headline fit because the requirement bound only a minimum per feddan and the season still contains price information, but the refit is reported here and the difference is part of the uncertainty the three curves below have to carry.

## 5. Validation on the two seasons outside the fit

No FAOSTAT farm gate price is published for 2025 or 2026, so those seasons cannot be fit points. They can still be used as checks, with the alternative price set to the project 2025 forecast wheat price of 17,892 pounds per tonne, carried unchanged. That alternative is a labelled construction, and the checks inherit the label.

For 2025, the ratio is 0.820 and the fitted share is 0.399, against an actual share of 0.430. The line underpredicts the season by about 3 points of share, about 0.3 million tonnes.
For 2026, the ratio is 0.932 and the fitted share is 0.418, against an actual share of 0.480. The line underpredicts by about 6 points of share, about 0.6 million tonnes.

The misses are in one direction and they are informative. The response of 2025 and 2026 ran stronger than the 2019 to 2024 record, and the public record says why in part: planted area rose to a record of about 3.7 million feddans in 2026 (Ministry of Agriculture, reported by AgriInsite on 2 June 2026), payment within 48 hours was publicised, and the price for 2026 was announced before sowing and then raised again in April 2026. The six season fit holds production fixed, so it cannot see the planting half of the response. Version 7 handles this in three stated ways: the headline grid holds production fixed and says so; the high response curve below is fitted on all eight seasons; and the Monte Carlo in src/methods_v7.py varies production across its historical range on top of the response curves.

## 6. The three response curves used in version 7

Central. The six season fit: share = 0.2611 + 0.1682 times ratio.
Low. The same fit with the slope reduced by one standard error, pivoted at the sample mean ratio of 0.854 and mean share of 0.405: share = 0.2894 + 0.1351 times ratio. This is a statistical lower curve on the fit sample.
High. A fit on all eight seasons, with the 2025 and 2026 ratios built on the carried alternative price: share = 0.2465 + 0.1989 times ratio. This curve is not a statistical bound. It is the line the full record, including the two strong recent seasons, supports, and it rests on a constructed alternative price for those two seasons. It is labelled that way wherever it is used.

At the announced price for the coming season, 2,650 pounds per ardeb, the ratio against the model farm gate price of 17,892 pounds per tonne is 0.987, and the three curves give shares of 0.422 (low), 0.428 (central) and 0.443 (high). At the top of the demand range, 3,500 pounds per ardeb, the ratio is 1.304 and the shares are 0.466, 0.481 and 0.506. The curves are used inside their observed ratio range of 0.654 to 1.000 and modestly beyond it; every grid point above a ratio of 1.000 is an extrapolation and the results log says so at those rows.

## 7. The financial parameters of version 7, each with its source or its label

Production basis for the coming season: 10.2 million tonnes, the FAO forecast of a record 2026 harvest (FAO GIEWS, June 2026, at about 10 million tonnes; the 10.2 figure reported by Brief News, 8 November 2026). Labelled: this is the 2026 harvest carried as the planning basis for the coming season, because no 2027 harvest forecast exists at the time of writing.
Delivery target: 5.0 million tonnes, the goal the government announced for the 2026 season (Reuters, 11 June 2026; Tridge summary of the October 2026 announcement).
World price for gap imports, dollars per tonne cost and freight to Egypt: low 265 (the GASC tender of 12 August 2024 cleared at an average of 265.85 cost and freight, as reviewed in the Grain Trade Ukraine report of the 4 November 2024 tender; a trader quoted about 260 as a tender clearing level to Reuters in June 2026); central 313 (the S and P Global price for wheat delivered to Egypt on 8 October 2026, reported in the Black Sea ports report of 15 October 2026); high 400 (the top of the 300 to 400 range paid for five European cargoes bought in the week of 19 October 2026, trader Hesham Soliman reported by Brief News, 8 November 2026).
Exchange rate, pounds per dollar: low 54.47 (Central Bank of Egypt official sell rate at the fixing of 21 October 2026); central 55.25 (Reuters, 24 October 2026, reporting the 2,650 announcement at 1 dollar to 55.25 pounds); high 57.00 (a stated stress, set above the record lows near 56 reported in early November 2026).
Financing rate for carrying stock: low 0.23956 (the accepted weighted average yield on 91 day treasury bills at the Central Bank auction of 18 October 2026); central 0.25 (364 day bills cleared at 24.95 to 25.28 percent and 273 day bills at 25.38 to 25.74 percent at the auctions of August to October 2026, and the 91 day average reached 25.0 percent in November 2026, Al Arabiya); high 0.2635 (the 273 day average of November 2026, Al Arabiya). The policy rate for reference: the Central Bank raised the overnight deposit rate to 20.0 percent on 29 October 2026. The bill yields are used because they are the marginal cost of government borrowing, which is what carrying a stock actually costs the state.
Average holding period of the delivered stock: low 3, central 5, high 7 months. Labelled assumption. Deliveries land between April and August and the stock is drawn against bread demand through the year. No public series gives the average holding period of the state stock.
Storage cost: low 40, central 60, high 90 pounds per tonne per month. Labelled assumption. No public silo tariff was found in the searches for this build.
Shipping lag on gap imports: 75 days, central. Labelled assumption. Gap orders can only be placed once the delivery shortfall is known at the close of the season in mid August, and tender, contracting and voyage time put arrival in late October to November. The cost of the lag is carried in the accounts by pricing gap tonnes at the world scenario of the arrival quarter, and in the worst quarter calculation at the high world scenario. No separate lag premium is added, and that choice is stated here rather than buried.

## 8. What this evidence cannot do

The record is eight seasons, six of them fit points, in a market where the state is both the price setter and the largest buyer, where one season carried a legal delivery requirement, and where the alternative price series is partly administered. The fitted slope is a planning input with wide honest uncertainty, not a measured elasticity of a free market. Every version 7 result that depends on it is reported across the three curves or across the Monte Carlo spread, never on the central curve alone without the band beside it.
