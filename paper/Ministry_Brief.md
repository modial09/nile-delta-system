# Wheat Procurement Price: What Each Candidate Price Buys

Planning brief. Nile Delta wheat model, version 7. Mohamed Diallo, 18 November 2026.

**Finding.** In October the state announced a price of 2,650 pounds per ardeb and a delivery target of 5,000,000 tonnes. On the delivery record of the last eight seasons, that price brings 4,357,279 tonnes to the collection points. The remaining 642,721 tonnes arrive later, by ship, at world prices: 11.1 billion pounds of imports inside a total programme cost of 97.4 billion pounds. In 2,000 simulated seasons at this price, no season reaches the target.

## The price grid, central response curve

| Price per ardeb | Delivered, tonnes | Cover, percent | Months of stock | Total programme cost, pounds | Step cost per extra tonne, pounds |
| --- | --- | --- | --- | --- | --- |
| 2200 | 4,069,547 | 19.76 | 2.37 | 83,215,473,521 | first row |
| 2350 | 4,165,458 | 20.22 | 2.43 | 87,738,218,743 | 47,156 |
| 2500 | 4,261,368 | 20.69 | 2.48 | 92,472,767,162 | 49,364 |
| 2650 | 4,357,279 | 21.15 | 2.54 | 97,419,118,780 | 51,572 |
| 2800 | 4,453,190 | 21.62 | 2.59 | 102,577,273,596 | 53,781 |
| 3000 | 4,581,071 | 22.24 | 2.67 | 109,784,284,993 | 56,357 |
| 3250 | 4,740,923 | 23.01 | 2.76 | 119,322,557,234 | 59,670 |
| 3500 | 4,900,774 | 23.79 | 2.85 | 129,449,171,692 | 63,350 |

## The cost build at four prices, pounds

| Price per ardeb | Procurement bill | Gap, tonnes | Gap import cost | Carrying cost | Total |
| --- | --- | --- | --- | --- | --- |
| 2200 | 59,686,684,313 | 930,453 | 16,090,562,261 | 7,438,226,947 | 83,215,473,521 |
| 2650 | 76,978,601,043 | 642,721 | 11,114,729,670 | 9,325,788,067 | 97,419,118,780 |
| 3000 | 91,621,427,256 | 418,929 | 7,244,637,655 | 10,918,220,081 | 109,784,284,993 |
| 3500 | 114,351,400,415 | 99,226 | 1,715,934,776 | 13,381,836,501 | 129,449,171,692 |

## Readings

**The target.** The question is which response curve the record supports, reported that way rather than as a flat failure. On the central curve, fitted on 2019 to 2024, even the top of the demand range falls short: at 3,500 pounds, deliveries of 4,900,774 tonnes miss the target by 99,226 tonnes. On the high curve, fitted on all eight seasons, the same price delivers 5,159,464 tonnes and passes. The two most recent seasons ran above the central curve.

**The step.** Each extra tonne a higher price attracts costs 47,156 to 63,350 pounds, roughly three times the price itself. The reason is arithmetic: the higher price is paid on every tonne delivered, not only on the extra tonnes. The move from 2,650 to 3,000 buys 223,792 extra tonnes for 12,365,166,213 extra pounds, an average of 55,254 pounds per extra tonne.

**The risk.** Monte Carlo simulation, 2,000 draws per price across the three response curves, the production history of 2015 to 2024 and the world price scenarios: draws reaching the target run at 0.0 percent at 2,650, 6.4 percent at 3,000 and 44.5 percent at 3,500. The worst quarter mean total at 2,650 is 100,533,845,324 pounds.

**The planting side.** Inside the cropping model, margin alone first plants Delta wheat at a state price of about 3,060 pounds per ardeb. Below that point the wheat area stands on the observed planting pattern, not on margin. Holding pattern production costs the farm economy 30.2 billion pounds at a price of 2,200 and 13.1 billion at 3,500: a higher price is a more expensive purchase and a cheaper production guarantee at the same time.

## Basis and assumptions

Production basis 10,200,000 tonnes; national consumption 20,600,000 tonnes; delivery target 5,000,000 tonnes. Central world price 313 dollars per tonne, cost and freight; exchange rate 55.25 pounds per dollar; financing at 25 percent a year, on treasury bill yields. Delivery response: share equals 0.2611 plus 0.1682 times the ratio of the state price to the farm gate price, fitted on six seasons, 2019 to 2024, R squared 0.866. The fit underpredicts the delivered share in 2025 and in 2026, which is why low, central and high curves are carried through every table. Carrying is charged on delivered local tonnes over a holding period of five months, financing on the bill, storage at 60 pounds per tonne per month. The holding period is a labelled assumption with no public source, and the largest single sensitivity of the total: between three and seven months it swings the total at the announced price by 7.5 billion pounds, ahead of the world price at 4.8 billion. Grid rows at 2,800 pounds and above extend the fitted response beyond its observed ratio range of 0.654 to 1.000 and are extrapolations. The total counts the bill, the gap import cost and carrying only; the baseline import programme for the rest of consumption is excluded, as is the bread subsidy system downstream.

Verification: an independent check recomputed the fit, the grid arithmetic and the Monte Carlo shares, and replayed the announced price plans under a second solver. Thirteen of thirteen checks pass; one passes weakly, the rice decree bound, which does not bind the optimised plans. Label: a numerically verified exploratory planning instrument on a stated basis, not validated empirical evidence.
