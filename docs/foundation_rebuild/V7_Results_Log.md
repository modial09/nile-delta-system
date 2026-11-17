# V7 Results Log: The Procurement Price Extension

Date: 17 November 2026
Code: src/allocation_model_v7.py, src/methods_v7.py, src/check_v7.py
Run records: data/processed/run_v7_grid.txt, run_v7_mc.txt, run_v7_breakeven.txt, run_v7_sensitivity.txt, run_v7_check.txt
Results: data/processed/results_v7_grid.json, results_v7_methods.json, montecarlo_samples_v7.csv, plan_v7_free_price{price}.csv and plan_v7_floor_price{price}.csv for each grid price
Evidence: docs/foundation_rebuild/V7_Delivery_Response_Evidence.md, data/external/v7_delivery_evidence.csv
Verification: docs/foundation_rebuild/CheckV7_Independent_Verification.md

Version 6 files were not modified. This log is the exact figure record. Money here is unrounded; any summary built on this log rounds to billions with one decimal, as version 6 did.

## 1. What was built

The procurement price is now a decision variable. Three parts were built in order. First, a delivery response fitted from the public record of eight seasons: the share of national wheat production that reaches state collection points, as a line in the ratio of the procurement price to the farm gate price. Second, a price grid from 2,200 to 3,500 pounds per ardeb: at each price, expected tonnes delivered, the wheat cover and months of stock those tonnes buy, and two cropping plan readings from the version 6 model under its caps, its rice decree bound, berseem and its storage scenarios. Third, a financial layer: the procurement bill, the import gap against the announced delivery target of 5.0 million tonnes priced at world price scenarios with a stated shipping lag, the carrying and financing cost of the stock bought, and the total state programme cost. Robustness follows the version 6 standard: Monte Carlo over the response curves, production history and world price scenarios; a break even analysis of wheat against berseem by governorate; and a sensitivity ranking of the new inputs. An independent check replays the headline plans under a second solver.

## 2. The delivery response in one paragraph

Central curve, fitted on 2019 to 2024: share = 0.2611 + 0.1682 times ratio, slope standard error 0.0331, residual standard deviation 0.0105, R squared 0.866. Low curve: share = 0.2893 + 0.1351 times ratio. High curve, fitted on all eight seasons with a constructed alternative price for 2025 and 2026: share = 0.2464 + 0.1989 times ratio. Refit without 2022, the season with a legal delivery requirement: share = 0.2831 + 0.1384 times ratio. Validation: the central curve underpredicts 2025 (fitted 0.3990, actual 0.4301) and 2026 (fitted 0.4178, actual 0.4804). The full record, the confounders and the labels are in the evidence note.

## 3. The price grid, central curve and central financial parameters

Production basis 10,200,000 tonnes. Cover is delivered tonnes divided by national consumption of 20,600,000 tonnes. Rows at prices of 2,800 and above carry a ratio above 1.000 and are extrapolations of the fitted line beyond its observed range; they are marked in the last column.

| Price per ardeb | Price per tonne | Ratio | Share, low, central, high | Delivered, tonnes | Cover, percent | Months | Bill, pounds | Gap, tonnes | Gap cost, pounds | Carrying, pounds | Total, pounds | Step cost per extra tonne, pounds | Extrapolated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2200 | 14,666.67 | 0.8198 | 0.4001, 0.3990, 0.4095 | 4,069,547 | 19.76 | 2.37 | 59,686,684,313 | 930,453 | 16,090,562,261 | 7,438,226,947 | 83,215,473,521 | first row | no |
| 2350 | 15,666.67 | 0.8756 | 0.4076, 0.4084, 0.4206 | 4,165,458 | 20.22 | 2.43 | 65,258,834,792 | 834,542 | 14,431,951,398 | 8,047,432,553 | 87,738,218,743 | 47,156 | no |
| 2500 | 16,666.67 | 0.9315 | 0.4152, 0.4178, 0.4317 | 4,261,368 | 20.69 | 2.48 | 71,022,807,035 | 738,632 | 12,773,340,534 | 8,676,619,593 | 92,472,767,162 | 49,364 | no |
| 2650 | 17,666.67 | 0.9874 | 0.4228, 0.4272, 0.4428 | 4,357,279 | 21.15 | 2.54 | 76,978,601,043 | 642,721 | 11,114,729,670 | 9,325,788,067 | 97,419,118,780 | 51,572 | no |
| 2800 | 18,666.67 | 1.0433 | 0.4303, 0.4366, 0.4540 | 4,453,190 | 21.62 | 2.59 | 83,126,216,815 | 546,810 | 9,456,118,807 | 9,994,937,974 | 102,577,273,596 | 53,781 | yes |
| 3000 | 20,000.00 | 1.1178 | 0.4404, 0.4491, 0.4688 | 4,581,071 | 22.24 | 2.67 | 91,621,427,256 | 418,929 | 7,244,637,655 | 10,918,220,081 | 109,784,284,993 | 56,357 | yes |
| 3250 | 21,666.67 | 1.2110 | 0.4530, 0.4648, 0.4873 | 4,740,923 | 23.01 | 2.76 | 102,719,994,718 | 259,077 | 4,480,286,216 | 12,122,276,300 | 119,322,557,234 | 59,670 | yes |
| 3500 | 23,333.33 | 1.3042 | 0.4656, 0.4805, 0.5058 | 4,900,774 | 23.79 | 2.85 | 114,351,400,415 | 99,226 | 1,715,934,776 | 13,381,836,501 | 129,449,171,692 | 63,350 | yes |

Three readings of this table matter most.

First, the announced price of 2,650 buys, on the central curve, 4,357,279 tonnes: a cover of 21.15 percent, 2.54 months of stock, at a total programme cost of 97,419,118,780 pounds. It does not reach the announced target of 5.0 million tonnes. The gap of 642,721 tonnes must be imported at the arrival quarter world price.

Second, the step cost per extra tonne runs from 47,156 pounds at the first step to 63,350 pounds at the last, roughly three times the procurement price itself at every step. The reason is arithmetic, not modelling: a higher price is paid on every tonne delivered, not only on the extra tonnes it attracts, and the import saving on the shrinking gap offsets only a small part of that. Moving from the announced 2,650 to the bottom of the demand range at 3,000 buys 223,792 extra tonnes for 12,365,166,213 extra pounds, an average of 55,254 pounds per extra tonne over that move.

Third, even the top of the demand range does not close the target on the central curve. At 3,500 the state buys 4,900,774 tonnes, still 99,226 tonnes short of 5.0 million, at a total of 129,449,171,692 pounds. On the high curve the same price delivers 5,159,464 tonnes and passes the target; the target question is therefore a question about which response curve the recent record supports, and the evidence note shows the two most recent seasons running above the central curve.

One smaller observation, recorded because it is easy to misread: at the bottom of the grid the total is almost flat across the response curves. At 2,200 the low curve total is 83,206,350,303 pounds and the high curve total is 83,129,833,894 pounds, both a little below the central total of 83,215,473,521, because at a low price an extra delivered tonne swaps an import tonne at the world price for a local tonne at a similar all in cost. Higher up the grid the bill dominates and the total rises with the curve. The curve band on the total at 3,500 runs from 128,115,071,643 pounds (low curve) to 134,475,697,241 pounds (high curve).

## 4. The plan readings at each price

Wheat in the version 6 model earns the blended price: the central delivery share valued at the state price, the rest at the model farm gate price of the same layer. The free plan plants what margin alone would plant under the caps. The pattern floor plan holds wheat production at 4,610,705 tonnes in every scenario, the level the version 6 pattern test found the observed pattern can hold (a cover of 22.38 percent on production, before any delivery share is applied).

| Price per ardeb | Free plan wheat area, hectares | Free plan expected wheat production, tonnes | Floor plan wheat area, hectares | Floor plan expected wheat production, tonnes | Cost of holding the floor at this price, pounds | Study area deliveries from the floor plan, tonnes |
| --- | --- | --- | --- | --- | --- | --- |
| 2200 | 0 | 0 | 670,548 | 4,654,407 | 30,208,738,042 | 1,856,993 |
| 2350 | 0 | 0 | 670,548 | 4,654,407 | 28,457,266,055 | 1,900,758 |
| 2500 | 0 | 0 | 670,548 | 4,654,407 | 26,618,263,038 | 1,944,524 |
| 2650 | 0 | 0 | 670,548 | 4,654,407 | 24,691,728,991 | 1,988,289 |
| 2800 | 0 | 0 | 670,539 | 4,654,426 | 22,677,660,509 | 2,032,063 |
| 3000 | 22,921 | 169,949 | 670,539 | 4,654,426 | 19,856,104,740 | 2,090,417 |
| 3250 | 90,402 | 670,299 | 670,457 | 4,656,813 | 16,450,808,730 | 2,164,470 |
| 3500 | 116,250 | 857,409 | 670,457 | 4,666,030 | 13,055,748,926 | 2,241,879 |

The entry threshold: the free plan first plants wheat on its own at a blended price of about 19,027 pounds per tonne. On the central response curve, that blended price is reached at a state price of about 20,398 pounds per tonne, 3,060 pounds per ardeb. That point sits inside the demand range. Below about 3,060 per ardeb, on the model basis, every hectare of wheat in the Delta is there because of the floor, the pattern and motives outside margin, not because margin alone plants it. Above that point the price starts to plant wheat by itself, though even at 3,500 the free plan plants only 116,250 hectares against the pattern 672,606 hectares, because potatoes and berseem still take the land and water first.

The cost of holding pattern production falls as the price rises, from 30,208,738,042 pounds at 2,200 to 13,055,748,926 pounds at 3,500. A higher state price is therefore also a cheaper guarantee: the same production promise costs the farm economy less to keep when wheat is worth more at the collection point.

## 5. Monte Carlo, 2,000 draws per price, seed 20261117

Draws combine the three response curves (weights 0.25, 0.50, 0.25), a production multiplier from a whole year drawn from the FAOSTAT production record of 2015 to 2024 (multipliers 0.914 to 1.078 around the ten year mean of 9,131,135 tonnes), an alternative price drawn from the three version 6 wheat price layers, and a world price scenario drawn from the three scenarios, converted at the central exchange rate. The promised cover at each price is the central case cover of section 3.

| Price per ardeb | Mean delivered, tonnes | Draws reaching the 5.0 million tonne target, percent | Draws reaching the promised cover, percent | Mean total cost, pounds | Worst quarter mean total cost, pounds | Total cost, 10th percentile | Total cost, 90th percentile |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2200 | 4,088,801 | 0.0 | 56.0 | 83,667,004,204 | 87,450,780,211 | 80,744,767,712 | 87,760,658,849 |
| 2350 | 4,181,952 | 0.0 | 56.0 | 88,258,256,902 | 91,805,045,341 | 85,626,946,826 | 91,917,964,755 |
| 2500 | 4,276,066 | 0.0 | 55.4 | 92,921,741,014 | 96,029,335,111 | 90,417,965,229 | 96,127,434,730 |
| 2650 | 4,372,309 | 0.0 | 54.6 | 97,863,751,799 | 100,533,845,324 | 95,642,275,353 | 100,580,467,008 |
| 2800 | 4,462,880 | 0.6 | 55.1 | 102,899,682,493 | 105,189,975,614 | 100,780,599,733 | 105,234,373,080 |
| 3000 | 4,582,704 | 6.4 | 53.2 | 110,107,000,197 | 112,268,994,242 | 107,552,215,050 | 111,865,717,976 |
| 3250 | 4,753,294 | 19.6 | 51.9 | 120,073,814,598 | 124,009,068,531 | 116,451,072,695 | 124,000,397,705 |
| 3500 | 4,910,191 | 44.5 | 50.1 | 131,128,487,430 | 138,104,106,067 | 125,765,687,226 | 137,962,901,637 |

The target reading is the hard one. At the announced price, no draw in 2,000 reaches 5.0 million tonnes. At 3,000, 6.4 percent of draws reach it. Only at 3,500 does reaching the target become a realistic prospect, at 44.5 percent of draws, and the worst quarter mean cost there is 138,104,106,067 pounds against a central case total of 129,449,171,692. The promised cover reading sits near one half at every price by construction, because the promise is the central case and the draws are centred near it; it is reported for completeness and should not be quoted as a confidence level.

## 6. Break even, wheat against berseem, by governorate

On the model basis, berseem earns a margin of 129,327 pounds per hectare (price 2,566.62 pounds per tonne on the constructed feed value of version 6, yield 68.183 tonnes per hectare, cost 45,674 pounds per hectare). Wheat must therefore earn revenue of 211,394 pounds per hectare to match it, against a wheat cost of 82,067 pounds per hectare. The break even state price has two readings: at the blended value, where only the delivered share earns the state price and the rest earns the farm gate price on the central curve; and at full delivery, where every tonne is valued at the state price, the most favourable case for wheat.

| Governorate | Wheat yield, tonnes per hectare | Break even at the blended value, pounds per ardeb | Break even at full delivery, pounds per ardeb |
| --- | --- | --- | --- |
| Beheira | 6.838 | 5,808 | 4,637 |
| Sharkia | 7.338 | 5,412 | 4,321 |
| Dakahlia | 6.593 | 6,015 | 4,810 |
| Kafr El Sheikh | 6.314 | 6,261 | 5,022 |
| Gharbia | 6.876 | 5,777 | 4,612 |
| Menoufia | 7.045 | 5,640 | 4,501 |
| Qalyubia | 6.786 | 5,852 | 4,673 |
| Damietta | 6.569 | 6,036 | 4,827 |

No price in the grid, and no price in the demand range, makes wheat beat berseem on margin in any governorate. Even at full delivery the break even sits at 4,321 to 5,022 pounds per ardeb, above the top demand of 3,500. The caveats are part of the result and travel with it: the berseem price is a constructed feed value, not a market price; berseem in the Delta feeds the farmer own animals, so its margin is largely avoided feed cost rather than cash; wheat straw and household flour carry value the model does not price; and berseem area cannot grow past livestock demand, which the model cap of 30 percent of district land reflects. The honest reading is that the delivery response of section 2 is not a berseem margin story. Farmers deliver more at a higher price through payment speed, obligation, input access and the state price anchoring the trader price, channels the fitted share summarises and the margin comparison cannot see. That is why version 7 fits the response to the record instead of deriving it from margins.

## 7. Sensitivity ranking of the new inputs, at the announced price

Each input moved between its low and its high value, all else at central. Base deliveries 4,357,279 tonnes, base total 97,419,118,780 pounds.

| Rank | Input | Total at low, pounds | Total at high, pounds | Swing in total, pounds | Swing in deliveries, tonnes |
| --- | --- | --- | --- | --- | --- |
| 1 | Holding period (3 to 7 months, labelled assumption) | 93,688,803,554 | 101,149,434,007 | 7,460,630,453 | 0 |
| 2 | World price (265 to 400 dollars per tonne) | 95,714,623,495 | 100,508,516,484 | 4,793,892,989 | 0 |
| 3 | Production basis (historical multiplier range) | 96,480,496,639 | 98,272,299,924 | 1,791,803,286 | 712,817 |
| 4 | Storage cost (40 to 90 pounds per tonne per month, labelled assumption) | 96,983,390,850 | 98,072,710,676 | 1,089,319,826 | 0 |
| 5 | Financing rate (0.23956 to 0.2635) | 97,084,261,866 | 97,852,123,411 | 767,861,545 | 0 |
| 6 | Response curve (low against high) | 97,305,535,578 | 97,820,417,610 | 514,882,031 | 204,831 |
| 7 | Exchange rate (54.47 to 57.00 pounds per dollar) | 97,262,204,950 | 97,771,169,041 | 508,964,092 | 0 |

The ranking carries a warning the user asked this build to surface. At the announced price, the total programme cost is more sensitive to the holding period, a labelled assumption with no public source, than to any measured input, and more sensitive to the world price than to the delivery response itself. The response curve moves deliveries by 204,831 tonnes between its low and high forms but moves the total by only about 0.5 billion pounds, because extra local tonnes replace import tonnes at similar money. Anyone quoting the total at 2,650 should quote the holding period assumption beside it.

## 8. Assumptions register, everything that carries weight

1. Delivery response, central curve fitted on six seasons. The single most important behavioural input. Its own record, confounders and validation misses are in the evidence note. Low and high curves are defined there and used throughout.
2. Production basis of 10.2 million tonnes, the FAO record 2026 harvest carried as the coming season planning basis. Labelled. No 2027 harvest forecast exists at the time of writing. The Monte Carlo varies production across its 2015 to 2024 historical multipliers.
3. Alternative price for the coming season: the model farm gate wheat price of 17,891.58 pounds per tonne. This is the version 6 expected layer on the 2025 basis. If the trader price in the coming season runs higher, every ratio in the grid falls and deliveries at each price fall with it.
4. Delivery target of 5.0 million tonnes, the announced goal for the 2026 season, carried as the target for the coming season. The gap and its cost are measured against this target and against nothing else.
5. World price scenarios of 265, 313 and 400 dollars per tonne cost and freight, each anchored on a named dated observation in the evidence note, section 7.
6. Exchange rate of 54.47, 55.25 and 57.00 pounds per dollar. The high value is a stated stress above the early November 2026 record low near 56.
7. Financing rate of 0.23956, 0.25 and 0.2635, on treasury bill yields of August to November 2026, not on the policy rate.
8. Holding period of 3, 5 and 7 months. Labelled assumption, no public source. Ranked first in the sensitivity of the total cost.
9. Storage cost of 40, 60 and 90 pounds per tonne per month. Labelled assumption, no public source.
10. Shipping lag of 75 days on gap imports. Labelled assumption. Its cost is carried by pricing gap tonnes at the arrival quarter world scenario, and in the worst quarter Monte Carlo reading through the drawn world price; no separate lag premium is added.
11. Carrying cost is charged on delivered local tonnes only. Gap import tonnes are treated as bought against immediate need at season close. A stated modelling choice.
12. The total state programme cost counts the procurement bill, the target gap import cost and the carrying cost. It does not count the baseline import programme for the rest of consumption (consumption less production, about 10.4 million tonnes on the basis used here), which does not change across the grid in the central case, nor the bread subsidy system downstream of the stock.
13. Grid rows at 2,800 and above extrapolate the fitted response beyond its observed ratio range of 0.654 to 1.000. They are marked in the grid table.
14. Inherited from version 6, unchanged: district water split by land share from the built anchor of 11.00 billion cubic metres; price and yield layers with weak measured coverage; the berseem price as a constructed feed value; recourse that sees the full scenario, so plan margins are lower bound readings in the same sense as version 6.

## 9. Verification status

The independent check routine src/check_v7.py ran on 17 November 2026. Thirteen of thirteen checks pass, including HiGHS replays of the announced price free plan (221,699,178,210 pounds against the CBC figure of 221,699,177,650) and floor plan (197,007,449,422 against 197,007,448,659), a recomputation of the response fit by a second method, and recomputation of the Monte Carlo shares from the saved samples. One check passes weakly and is recorded as such in the verification note: the rice decree check on the saved floor plan, because the optimised plans plant no rice and the bound does not bind them. The full record is docs/foundation_rebuild/CheckV7_Independent_Verification.md.

## 10. The label

Version 7 remains a numerically verified exploratory model study on a stated basis. It is not validated empirical evidence. What version 7 adds to version 6 is a priced answer to a live decision, the procurement price, built on the thinnest evidence base in the project: six fit seasons of delivery behaviour in a market where the state sets the price and buys the crop. The grid is a planning instrument with its uncertainty printed beside every row, in the curve band, in the Monte Carlo shares and in the sensitivity ranking. It should be quoted that way or not at all.
