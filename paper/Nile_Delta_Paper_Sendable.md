# Allocating Nile Delta water: the price of a food guarantee

Mohamed Diallo
November 2026

## Why I built this

I am a business analytics graduate living in Cairo. I built this model to answer a question that Egyptian water planning answers today by habit: given the water the Delta has, which districts and which crops should get it, and what does that choice cost? The model allocates land and water across eight Delta districts and five crops, under three possible Nile inflow years, and it prices the water in each district. This note reports what it found, what rests on real data, and what does not.

## The model in brief

Planting is decided before the inflow year is known, so the model decides in two stages. First it chooses how much land to plant to each crop in each district. Then, once the inflow year is known, it allocates the available water to those plantings. It maximises total farm margin, subject to the water budget, the land in each district, and a floor under staple food production that I set. I call that floor the guarantee, and the model prices each level of it. The guarantee is the heart of this note.

## The main finding: the guarantee is the decision

Today, the Delta cropping pattern delivers about 94.5 percent of its full water staple output in an average year, and it falls short in a dry year. The guarantee is therefore a real choice, not a technical one. At a guarantee of ninety percent of current staple output, the best plan earns an expected margin of EGP 130.44 billion, against EGP 118.11 billion for the current pattern. The gain is EGP 12.33 billion, or 10.44 percent. Per cubic metre of water, the gain is 11.52 percent, EGP 12.32 against EGP 11.05. At ninety five percent, the gain falls to EGP 5.36 billion, 4.54 percent. At one hundred percent in every year, the best plan earns EGP 114.35 billion and loses EGP 3.75 billion against the current pattern, though it earns more per cubic metre, EGP 11.33 against EGP 11.05, because it uses less water.

Read plainly: moving the guarantee from full to ninety percent creates EGP 16.09 billion of the apparent gain. Reallocation by itself, at full protection, earns less than the pattern farmers already use. The honest headline of this work is the middle setting: about four and a half percent, at the level of food protection the Delta actually delivers today.

I stress tested the ninety percent result. Moving the rice and potato prices by twenty percent each way moves the gain between 9.46 and 13.91 percent. Moving all costs by twenty percent moves it between 8.94 and 12.35 percent. Moving all water budgets by five percent moves it between 10.37 and 11.75 percent. The direction holds. The size is a band, not a point.

One part of the best plan deserves daylight. The plan plants 317,308 hectares of sugar beet and, in a dry year, gives that beet no water at all. The dry year shortfall, 1.65 billion cubic metres, is almost exactly the beet water demand, so the model covers it by writing the crop off, with about EGP 11.42 billion of planting cost already spent. Any planner who adopts this plan adopts that write off, and it should be argued about before anything else in the plan.

## What water is worth

One more cubic metre of water in an average year is worth EGP 8.02 to 10.21 across districts, lowest in Kafr El Sheikh and highest in Menoufia. In a dry year, the same cubic metre is worth EGP 33.03 to 37.90, about four times the normal year value. The values are high in a dry year because the planting is fixed before the inflow is known: water is precious exactly when the plan cannot adapt. For the same reason, perfect knowledge of the inflow year, known in advance, would be worth EGP 10.37 billion inside this model. I checked these values by brute force inside the model itself, and the check agrees exactly for Dakahlia.

## The stress tests

I cut total water by ten percent. Expected margin falls by EGP 13.70 billion to EGP 116.74 billion. Food output does not move, the guarantee holds in every year, and Beheira takes the largest district loss, EGP 2.76 billion. The first cut is paid in money, not in food.

I cut total water by twenty percent. Now the guarantee cannot be held. Staple output falls to 6.16 million tons, 57 percent of the guarantee, and Beheira again takes the largest loss, 957,042 tons of staples. I do not quote a margin for this case, because without the guarantee the solver wins margin back by cutting food, and such a number would mislead.

## What is real, and what is assumed

The crop yields and harvested areas are real: FAOSTAT series, Egypt averages over 2014 to 2023. The wheat price is real: the published government procurement price for 2025. The rest of the money side is assumed for now: the other four crop prices, all production costs, all crop water needs, the district land base, the district yield differences, the water budget of each inflow year, and the chance of each year. Every money figure in this note is therefore provisional. The ratios, and the order of the findings, are the results.

Two cautions follow. The ranking of districts by water value follows my assumed yield differences rank for rank, so until real district yields arrive, the levels inform and the ranking does not. And a first run of this model contained three errors: one in the code, which had reported negative harvests on eight rice plantings; one in the units of the water values; and one in the framing of the headline. This note reports the corrected run, and those corrections are the reason the headline reads four and a half percent and not ten.

## What comes next

Three data pulls come next, in this order. CAPMAS, for the real district land base, the real cropping pattern, and real district yields. A direct FAOSTAT pull, for producer prices on every crop and for cotton, which this model leaves out for want of a series. And the Ministry water quota figures, which would set the water budgets as fact instead of calibration. Until those land, this note is a priced argument about a food guarantee, built on real yields and assumed money. Nothing in it should be quoted as a measured saving. The code and the data tables are available on request.
