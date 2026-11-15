# Results note, Problem One, version two

I am Mohamed Diallo. This note replaces version one. I audited my own model the way an opponent would, and the audit found one fault in the code, one fault in the units of my water values, and one fault in how the headline was framed. Version two fixes all three. The numbers below come from the run saved in data/processed/run_v2_output.txt, produced by src/allocation_model_v2.py.

## The decision this model supports

A Delta planner can use this model today for one decision: how much staple production to guarantee, and what that guarantee costs. The model says the current crop mix earns what it earns while delivering about 94.5 percent of its full water staple output in expectation, and it falls short of full staple output in a dry year. An optimised plan held to a full guarantee in every year must keep a promise the current pattern itself does not keep. If the planner guarantees staple production at ninety percent of current output instead, a replanting toward sugar beet and potatoes in the strong yield districts raises expected margin by about a tenth. If the planner must guarantee the full current staple output in every year, the model finds no gain at all. Choosing the guarantee is the decision. The model prices it, and the price list is the most useful output in this note.

## The headline, graded honestly

At the ninety percent guarantee, the optimised plan earns an expected margin of EGP 130.44 billion against EGP 118.11 billion for the current pattern. The gain is EGP 12.33 billion, or 10.44 percent. Per cubic metre the gain is 11.52 percent, EGP 12.32 against EGP 11.05.

What is real in that number: the yields and harvested areas are FAOSTAT series, Egypt means over 2014 to 2023, pulled through the Our World in Data mirror after the FAOSTAT site failed, and the wheat price is the published government procurement price for 2025. What is illustrative: the other four crop prices, all production costs, all crop water requirements, the district land base, the district yield multipliers, the scenario budgets and the scenario probabilities. Every pound figure is therefore provisional. Ratios and orders are the results.

I attacked the headline with the sensitivity runs my design promised and version one skipped. I moved the rice price and the potato price by twenty percent in each direction, alone and together. The gain stays between 9.46 and 13.91 percent. I moved all production costs by twenty percent in each direction. The gain stays between 8.94 and 12.35 percent. I moved all water budgets by five percent in each direction. The gain stays between 10.37 and 11.75 percent. So at this guarantee, the direction of the result and its rough size do not rest on any single assumed price. Grade it as follows. Direction: solid inside this data. Size: a band of roughly nine to fourteen percent, not a point. What the headline cannot survive is a change in the food guarantee itself, which the staple section below prices.

One more fact about the plan belongs in the open. The plan plants 317,308 hectares of sugar beet and, in a low inflow year, gives that beet no water at all. Every other planting is fully watered in every year. The dry year shortfall of 1.65 billion cubic metres equals the beet water demand almost exactly, and the model covers it by writing the beet crop off, with about EGP 11.42 billion of planting cost sunk. Version one never said this. A planner who adopts this plan adopts that write off, and should argue about it before arguing about anything else in the plan.

## The water value map, in corrected units

Version one reported water values of about EGP 4 to 5 per cubic metre in an expected year and about EGP 8 to 9 in a low year, and said the dry year value roughly doubles. That was the wrong unit for the claim. Those numbers are probability weighted values from the stochastic model. The value inside the year itself, which is what a planner means by the value of water in a dry year, divides out the probability. In an expected year, one more cubic metre is worth EGP 8.02 to 10.21 across districts, lowest in Kafr El Sheikh and highest in Menoufia. In a low inflow year, one more cubic metre is worth EGP 33.03 to 37.90. The dry year value is about four times the normal year value, not about two times. I verified the reported duals by brute force inside the stochastic model itself this time, and the check agrees exactly for Dakahlia.

Two cautions govern the map. First, the order of districts follows the yield multipliers I assumed, rank for rank, with no exception. Until the CAPMAS pull brings real district yields, read the order as my assumption restated. The levels carry the information; the ranking does not yet. Second, the high dry year values are high because the planting is fixed before the inflow is known. Water is precious in a dry year precisely because the plan cannot adapt. That is the honest argument for planning under uncertainty, and the value of perfect inflow information inside this model is EGP 10.37 billion.

## The stress answers

A ten percent water cut: expected margin falls by EGP 13.70 billion to EGP 116.74 billion. Staple output does not move and the food guarantee holds in every year. Beheira absorbs the largest district loss, EGP 2.76 billion. The first cut is paid in money, not in food.

A twenty percent water cut: the food guarantee cannot be held. Staple output falls to 6.16 million tons, which is 57 percent of the guarantee, and Beheira again absorbs the largest loss, 957,042 tons of staples. I do not quote a comparable margin for this run, because without the guarantee the solver buys margin back by cutting food. The audit also found a quiet fault in the version one run of this case: with the guarantee dropped, its solver reported negative harvests on eight rice plantings, the largest about 14,586 tons below zero in Beheira. Version two fences production at zero. The staple fall barely moves, so the conclusion stands and the arithmetic is now clean.

## The staple trade, priced

The guarantee is a dial, and here is what each setting does to the gain over the current pattern.

1. Guarantee at ninety percent of current staple output: gain EGP 12.33 billion, 10.44 percent.
2. Guarantee at ninety five percent: gain EGP 5.36 billion, 4.54 percent.
3. Guarantee at one hundred percent in every year: total margin EGP 114.35 billion against the current pattern at EGP 118.11 billion, a loss of EGP 3.75 billion. Margin per cubic metre still leads, EGP 11.33 against EGP 11.05, a gain of 2.55 percent, because the strict plan uses less water.

The arithmetic is blunt. Moving the guarantee from full to ninety percent creates EGP 16.09 billion of the headline. Reallocation alone, at full protection, earns less than the current pattern on total margin. One caution cuts the other way, and fairness requires it: the full guarantee in every year is a promise the current pattern itself does not keep, because in a dry year the current pattern also falls short of its full water staple output. The current pattern delivers about 94.5 percent of its full water staple output in expectation. A planner who wants protection at the level the current pattern actually delivers sits near the middle row of the table, where the gain is about four and a half percent. That middle row is my honest headline for a careful reader.

## What data lands next and what it could change

CAPMAS comes first. It carries the real district land base, the real district cropping pattern and real district yields. It could reorder the water value map, and it makes the baseline test bind district by district instead of only at crop mix level. The direct FAOSTAT pull comes second, for producer prices on every crop and for cotton, which version one and two both omit for want of a series. Real prices could narrow the gain band from below if beet and potato prices land under my assumed values in the same season. The Ministry water quota figures come third: they would fix the scenario budgets as fact rather than as a calibration set just under the current pattern demand. The hydrology pull sets the scenario scaling, and the extension pull replaces my midpoint water requirements with Egyptian values. Until those land, this note stands as a priced argument about a guarantee, built on real yields and assumed money, and nothing in it should be quoted as a measured saving.
