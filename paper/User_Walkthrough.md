# My Nile Delta Project: The Price Announcement

Mohamed Diallo, November 2026

## It starts with one number

Every autumn, Egypt announces one number: the price the state will pay for wheat, in pounds per ardeb. This year the number is 2,650. Parliament argued for 3,000 to 3,500. A committee deputy put the cost of growing one feddan at about 50,000 pounds, and the crop on that feddan, sold fully to the state at 2,650, returns about 47,700. On those figures, the farmer loses money on every feddan he delivers in full.

Then spring comes, and the argument meets a man with a harvest in front of him. He has two buyers. The state collection point pays the announced price and pays fast, inside 48 hours. The trader stands at his gate and pays cash on the spot. What the state does not collect from him and from thousands like him, it buys later, by ship, at world prices, in a hurry. The August 2024 tender went out looking for 3.8 million tonnes and came back with 280,000.

My project asks a plain question about that number. What does each price actually buy?

## What I built first, and why it was not enough

The first model, version 6, priced a promise about land. It moves cropping across eight governorates and nine crops, winter planting chosen before the water year is known, summer planting adapting once it is. It said what a wheat guarantee costs: a ceiling of 27.83 percent of the wheat Egypt eats, and 28.9 billion pounds to hold 25 percent in every scenario.

But a plan grows wheat; it does not deliver one tonne to a silo. Between the field and the silo stands the farmer choice, and the choice answers to the announcement. Version 7 prices the announcement itself.

## The delivery answer, and why it is a line fitted to the record

I took the public record of eight seasons, 2019 to 2026: the announced price, the tonnes the state bought and the tonnes grown. The share that reached the state runs from 0.373 in 2019 to 0.480 in 2026.

A price means little alone. It means something against the other price in the farmer hand, the trader price for the same tonne. So I worked with a ratio, the state price divided by the farm gate price, and fitted one line on the six seasons with a published farm gate price: share equals 0.2611 plus 0.1682 times the ratio. In plain words, when the state price rises from equal to the farm price to ten percent above it, the share that arrives rises by about 1.7 points. The line explains 0.866 of the movement in those six shares.

I fitted the answer to the record because the other road, working the answer out from crop margins, fails. The berseem test below shows where it fails. But the line has already failed once, in the open: tested on 2025 and 2026, two seasons it never saw, it reads low both times, 0.399 against an actual 0.430 and 0.418 against an actual 0.480. The real answer ran stronger, in part because planted area rose to a record and payment sped up, and my grid holds the crop fixed at 10.2 million tonnes, so it cannot see that planting half. That failure is why every result below travels on three curves, low, central and high.

## The money layer, because a tonne is not a cost

At each price the model counts three costs. The bill: the price times the tonnes delivered. The gap cost: the tonnes still missing from the state target of 5.0 million, imported at a world price. The carrying cost: the interest and the storage on the stock the state now holds. The sum is the total programme cost, the number a minister should see before he signs the price, not after the ships are booked.

| Price per ardeb | Share delivered | Delivered, million tonnes | Cover, percent | Months of stock | Total cost, billion pounds | Cost of each extra tonne, pounds |
| --- | --- | --- | --- | --- | --- | --- |
| 2200 | 0.399 | 4.070 | 19.76 | 2.37 | 83.2 | first row |
| 2350 | 0.408 | 4.165 | 20.22 | 2.43 | 87.7 | 47,156 |
| 2500 | 0.418 | 4.261 | 20.69 | 2.48 | 92.5 | 49,364 |
| 2650 | 0.427 | 4.357 | 21.15 | 2.54 | 97.4 | 51,572 |
| 2800 | 0.437 | 4.453 | 21.62 | 2.59 | 102.6 | 53,781 |
| 3000 | 0.449 | 4.581 | 22.24 | 2.67 | 109.8 | 56,357 |
| 3250 | 0.465 | 4.741 | 23.01 | 2.76 | 119.3 | 59,670 |
| 3500 | 0.481 | 4.901 | 23.79 | 2.85 | 129.4 | 63,350 |

Read the announced row. At 2,650 the share is 0.427, and on a crop of 10.2 million tonnes that delivers 4.357 million tonnes: cover of 21.15 percent, 2.54 months of stock. The bill is 77.0 billion pounds. The gap to the target is 642,721 tonnes, and importing it at the central world price costs 11.1 billion. Carrying costs 9.3 billion. The total is 97.4 billion, and the target is missed. Rows at 2,800 and above stretch the fitted line past the ratios it was fitted on: the line extended, not the line observed.

## The number that surprised me

Look at the last column. Each extra tonne a higher price attracts costs between 47,156 and 63,350 pounds, roughly three times the price itself. The reason is plain arithmetic. The raise is paid on every tonne delivered, not only on the extra tonnes it brings in, and the saving on the smaller import gap pays back only a small part. Moving from 2,650 to 3,000 buys 223,792 extra tonnes for 12.4 billion extra pounds, about 55,254 pounds for each extra tonne. Most of the money goes to farmers who would have delivered anyway. That may still be the right policy. It should be chosen with its price tag showing.

And the top of the demand range does not settle the target question by itself. At 3,500 the central curve delivers 4.901 million tonnes, still 99,226 tonnes short. The high curve, fitted on all eight seasons, delivers 5.159 million tonnes and passes. So the honest question is not whether the target fails. It is which curve the last two seasons support, and those seasons ran above my central line.

## The planting side answers back

Money alone, with no promise and no pattern holding it there, first plants wheat in the model at a state price of about 3,060 pounds per ardeb. Below that point, every hectare of wheat stands on the pattern Egypt plants and on motives outside margin. Above it, the price starts to plant wheat by itself, slowly: even at 3,500 the free plan plants 116,250 hectares against a pattern of about 672,606, because potatoes and berseem take the land and water first. The same raise also makes the old promise cheaper to keep: holding pattern production costs the farm economy 30.2 billion pounds at a price of 2,200 and 13.1 billion at 3,500. A higher price is a dearer purchase and a cheaper guarantee at the same time.

## Wheat against berseem, an honest negative

The public argument says wheat must beat berseem, the clover that feeds Delta livestock, before farmers plant and deliver more. I priced that contest. Wheat would need a state price of 5,412 to 6,261 pounds per ardeb to match berseem on margin. Even if every tonne earned the state price, the break even sits at 4,321 to 5,022. No price under discussion comes close.

One caveat: the berseem price in my model is a built feed value, not a market price, because no office publishes one. Berseem mostly feeds the farmer own animals, so its margin is largely feed cost he avoids, not cash. Wheat straw and flour for the house carry value the model does not price. So the negative does not say the price does not matter. It says deliveries do not answer the price through the berseem margin. They answer through payment speed, through obligation, through access to inputs, and because the state price pulls the trader price up behind it. The fitted line summarises all of that. The margin table cannot see it.

## The tests, and the soft spot inside my own headline

I simulated 2,000 seasons at each price, mixing the three curves, the production history of 2015 to 2024 and the world price scenarios. At 2,650, no draw reaches the target. At 3,000, 6.4 percent of draws reach it. At 3,500, 44.5 percent do. The worst quarter of seasons at the announced price averages 100.5 billion pounds against the central 97.4 billion.

The input that moves my total most is one I had to assume: how long the state holds the stock. Between three and seven months it swings the total at the announced price by 7.5 billion pounds, ahead of the world price at 4.8 billion. The response curve moves deliveries by about 205,000 tonnes between its low and high forms but moves the total by only about 0.5 billion, because an extra local tonne replaces an import tonne at similar money. Anyone quoting my 97.4 billion should quote the holding period beside it. I do.

An independent check, written apart from the build, recomputed the fit by a second method, replayed the two announced price plans under a second solver, and rebuilt the simulation shares from the saved samples. Thirteen of thirteen checks pass. One passes weakly, and I keep the weakness where readers can see it: the check that the plans respect the rice decree, because the optimised plans plant no rice at all, so the decree bound never binds them. It binds the real pattern, not these plans.

## What this proves, and what it does not

Version 6 priced a promise about land. Version 7 prices the announcement that moves the crop. It hands the price meeting one page: what each price buys, what it costs in full, what it costs in a bad year, and where the answer is soft. The label does not change. This is a numerically verified exploratory study, not validated evidence. District water is still split by land share from a built total. The delivery line still rests on six seasons. The numbers are the start of a price talk, not the end of one.
