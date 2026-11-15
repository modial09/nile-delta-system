# Results note: allocating Nile Delta water

Mohamed Diallo. November 2026. This is version three. It replaces version two and keeps its numbers. I rewrote the words only, to say the same things more plainly.

I am Mohamed Diallo. I built a model that allocates Nile Delta water among eight districts and five crops, under three possible inflow years. Then I audited my own work the way an opponent would. The audit found three faults: one in the code, one in the units of my water values, and one in how I framed the headline. This note reports the corrected model. Where a number rests on data I assumed for now, the note says so.

## The one decision this model supports

The model supports one decision today: how much staple food production to guarantee, and what that guarantee costs. The current cropping pattern earns what it earns while delivering about 94.5 percent of its full water staple output in an average year, and it falls short in a dry year. So the honest question is not how to beat the current pattern. It is what level of food protection to buy, and at what price. The rest of this note is that price list.

## The headline, with its limits

At a guarantee of ninety percent of current staple output, the best plan earns an expected margin of EGP 130.44 billion, against EGP 118.11 billion for the current pattern. The gain is EGP 12.33 billion, or 10.44 percent. Per cubic metre of water the gain is 11.52 percent, EGP 12.32 against EGP 11.05.

What is real in that number: the crop yields and harvested areas are FAOSTAT series, Egypt averages over 2014 to 2023, and the wheat price is the published government procurement price for 2025. What is assumed: the other four crop prices, all production costs, all crop water needs, the district land base, the district yield differences, the water budgets for each inflow year, and how likely each year is. Every money figure is therefore provisional. The ratios and the order of things are the results.

I tested the headline hard. I moved the rice and potato prices by twenty percent each way, alone and together: the gain stays between 9.46 and 13.91 percent. I moved all costs by twenty percent: the gain stays between 8.94 and 12.35 percent. I moved all water budgets by five percent: the gain stays between 10.37 and 11.75 percent. Inside this data, the direction of the result is solid and its size is a band of roughly nine to fourteen percent. What the headline cannot survive is a change in the food guarantee itself. That trade is priced below.

One part of the plan needs daylight. The plan plants 317,308 hectares of sugar beet and, in a dry year, gives that beet no water at all. The dry year shortfall is 1.65 billion cubic metres, almost exactly the beet water demand, and the model covers it by writing the crop off, with about EGP 11.42 billion of planting cost already spent. A planner who takes this plan takes that write off. It should be argued about first.

## The staple guarantee, priced

The guarantee is a dial. Here is what each setting does.

At ninety percent of current staple output, the gain is EGP 12.33 billion, 10.44 percent.

At ninety five percent, the gain is EGP 5.36 billion, 4.54 percent.

At one hundred percent in every year, the best plan earns EGP 114.35 billion against the current pattern at EGP 118.11 billion. That is a loss of EGP 3.75 billion. It still earns more per cubic metre, EGP 11.33 against EGP 11.05, because the strict plan uses less water.

Read plainly: moving the guarantee from full to ninety percent creates EGP 16.09 billion of the headline gain. Reallocation alone, at full protection, earns less than the pattern farmers already use. And the full guarantee is a promise the current pattern itself does not keep, because it delivers about 94.5 percent of its full water staple output in an average year. So the middle row, at about four and a half percent, is the honest headline. A careful reader should quote that one.

## What water is worth

One more cubic metre of water in an average year is worth EGP 8.02 to 10.21 across districts, lowest in Kafr El Sheikh and highest in Menoufia. In a dry year the same cubic metre is worth EGP 33.03 to 37.90. That is about four times the normal year value. My first version said about two times, because it quoted probability weighted values as if they were values inside the year. I checked the corrected values by brute force inside the model itself, and the check agrees exactly for Dakahlia.

Two cautions govern this map. The ranking of districts follows the yield differences I assumed, rank for rank, with no exception. Until real district yields arrive, the ranking is my assumption restated. The levels carry the information; the ranking does not yet. And the dry year values are high because planting is fixed before the inflow is known. Water is precious in a dry year precisely because the plan cannot adapt. That is the honest argument for planning under uncertainty. Inside this model, perfect knowledge of the inflow year ahead of time would be worth EGP 10.37 billion.

## The stress tests

I cut the water by ten percent. Expected margin falls by EGP 13.70 billion to EGP 116.74 billion. Staple output does not move, and the guarantee holds in every year. Beheira takes the largest district loss, EGP 2.76 billion. The first cut is paid in money, not in food.

I cut the water by twenty percent. The guarantee cannot be held. Staple output falls to 6.16 million tons, which is 57 percent of the guarantee, and Beheira again takes the largest loss, 957,042 tons of staples. I do not quote a margin for this case, because without the guarantee the solver buys margin back by cutting food. This is also where the audit found the code fault: the first version, with the guarantee dropped, reported negative harvests on eight rice plantings, the largest about 14,586 tons below zero in Beheira. The corrected model fences production at zero. The staple fall barely moves, so the conclusion stands and the arithmetic is now clean.

## What data lands next, and what it could change

Three data pulls come next, in this order. CAPMAS first: the real district land base, the real cropping pattern, and real district yields. That pull could reorder the water value map, and it tests the baseline district by district. The direct FAOSTAT pull second: producer prices for every crop, and cotton, which both versions leave out for want of a series. Real prices could narrow the gain band if beet and potato prices land below my assumed values. The Ministry water quota figures third: they would set the water budgets as fact instead of calibration. Two smaller pulls follow: hydrology, to set how the inflow years scale, and extension data, to replace my midpoint water needs with Egyptian values.

Until those land, this note is a priced argument about a food guarantee, built on real yields and assumed money. Nothing in it should be quoted as a measured saving.
