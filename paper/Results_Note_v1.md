# Results note, Problem One, version one

I am Mohamed Diallo. This note reports the first working run of my water allocation model for the Nile Delta. I wrote the numbers exactly as the run printed them. Where a number rests on a declared assumption instead of pulled data, I say so in the same breath.

## What I built and ran

I built the two stage stochastic linear program from my design. Stage one plants hectares by crop and district before the inflow is known. Stage two delivers water under the scenario that occurs. A water shortfall cuts yield through a yield response factor. The objective is expected farm margin. The constraints are district land, crop share caps, a water budget per district and scenario, and a food floor on staple production in every scenario. I solve it with PuLP and the CBC solver. The code is in src/allocation_model.py and the full printed run is saved in data/processed/run_v1_output.txt.

The model covers eight Delta governorates and five crops. The crops are wheat, rice, maize, sugar beet and potatoes. The scenarios are low, expected and high inflow, with probabilities of one quarter, one half and one quarter. I declare those probabilities as judgment.

## What data is real and what is not

Real pulled data: yields and harvested areas for Egypt from FAOSTAT, taken as means over 2014 to 2023. I pulled them on 12 November 2026 through the Our World in Data mirror, because the FAOSTAT site itself failed that day. The API returned a server error and the bulk download host refused the request. The mirror is a workaround, not the source of record, and a direct FAOSTAT pull is still owed. Mean yields are 6.57 tons per hectare for wheat, 9.15 for rice, 7.37 for maize, 52.19 for sugar beet and 28.09 for potatoes. The real harvested areas give the current crop mix: wheat 40.9 percent, maize 30.6 percent, rice 15.5 percent, sugar beet 6.9 percent and potatoes 6.1 percent.

One price is real: wheat at 14,667 Egyptian pounds per ton, the published government procurement price for the 2025 season. Everything else money shaped is a declared illustrative value inside a reported range. That covers the other four crop prices, all production costs, all crop water requirements, the district land base and the district yield multipliers. Every money figure below is therefore illustrative. The orders and the comparisons are the results. The exact pound values will move when the real price pull lands.

## The headline comparison

The falsification rule from my problem statement is fixed in advance. If the optimised allocation cannot beat the real current pattern in margin per unit of water by a meaningful margin, the thesis fails and I report that.

On this data the optimised plan beats the baseline. Expected margin is EGP 130.4 billion for the optimised plan against EGP 118.1 billion for the current pattern. The gain is EGP 12.3 billion, or 10.4 percent. Margin per cubic metre is EGP 12.32 against EGP 11.05, a gain of 11.5 percent. Expected water use is 10.59 billion cubic metres for the optimised plan against 10.69 for the baseline. The baseline at full watering would demand 11.41 billion cubic metres against an expected budget of 11.00, which is the scarcity the model is built for.

One trade sits inside that headline and I state it plainly. The optimised plan produces 10.90 million tons of staples, which is the food floor I set at 90 percent of the current pattern. The current pattern produces 11.44 million tons. Part of the margin gain is bought by letting staple output fall to the floor. A planner who wants the full current staple output can raise the floor, and the margin gain will shrink. The model makes that trade visible. It does not hide it.

The baseline also has a limit I state plainly. It is the real national crop mix placed on an illustrative district land base. It is not yet the real cropping pattern district by district, because the CAPMAS district pull is still owed. The falsification test therefore binds at the level of the crop mix today. It will bind at district level when CAPMAS lands.

## The optimised plan in words

The plan holds wheat at its cap of half the land in every district. It concentrates potatoes in Gharbia, Menoufia and Qalyubia, the districts with the strongest yields, and plants none in the other five. It cuts maize hard in the south and keeps rice spread across all districts at a lower share than today. In the low scenario the margin falls to EGP 99.4 billion while the food floor still holds. In the expected and high scenarios the margin is EGP 140.8 billion, because the fixed planting cannot use more water than its crops require, so extra budget in a wet year adds nothing.

## The water value map

The shadow price of water, in Egyptian pounds per cubic metre, by district and scenario. Expected scenario first, then low, then high.

1. Menoufia: 5.11, then 9.48, then 0.
2. Gharbia: 5.03, then 9.39, then 0.
3. Dakahlia: 4.96, then 9.31, then 0.
4. Qalyubia: 4.96, then 9.31, then 0.
5. Sharkia: 4.89, then 9.23, then 0.
6. Beheira: 4.74, then 9.07, then 0.
7. Damietta: 4.16, then 8.42, then 0.
8. Kafr El Sheikh: 4.01, then 8.26, then 0.

Water is worth most in the southern Delta and least in the northern Delta, where soil salinity drags yields down. In a low inflow year the value of one more cubic metre roughly doubles in every district. The zero in the high scenario needs one honest sentence. It means the fixed planting cannot absorb more water, so one more cubic metre adds nothing at the margin. It does not mean water has no worth in a wet year.

I verified the dual values by brute force. I raised one district water budget by one percent in a separate solve and divided the objective change by the added water. For Dakahlia in the expected scenario the solver dual and the brute force value agree at 13.68 pounds per cubic metre in the deterministic model. That check is why I trust the dual extraction code.

## The stress answers

A 10 percent water cut: expected margin falls by EGP 13.7 billion to EGP 116.7 billion. Staple output does not move. The food floor still holds in every scenario. Beheira absorbs the largest district loss, EGP 2.76 billion in the expected scenario. The first cut is paid in money, not in food.

A 20 percent water cut: the food floor cannot be held. Staple output falls to 6.17 million tons, which is 57 percent of the floor. Beheira again absorbs the largest loss, 957,042 tons of staples in the expected scenario. I do not quote a comparable margin for this run. Without the floor the solver buys margin back by cutting food, and that number would flatter the cut. The honest answer at 20 percent is the size of the food breach and where it lands.

## What planning on the average year costs

The expected value of perfect information is EGP 10.4 billion. That is the most that better inflow knowledge could be worth inside this model. The sharper finding runs the other way. A plan built for the expected year alone cannot keep the food floor in a low inflow year. Scored without the floor, that plan reaches EGP 137.2 billion, but the score is an upper bound that flatters it, because it is achieved by breaking the food rule in the dry year. For that reason the value of the stochastic solution has no single honest number in version one. The stochastic plan keeps a promise that the average year plan breaks. That sentence is the result.

## What failed and what is still owed

1. The direct FAOSTAT pull failed on 12 November 2026, so yields came through a mirror and the FAOSTAT producer prices pull is still owed for every crop.
2. Cotton is out of version one because the mirror carries no cotton series for Egypt. A Delta model without cotton is incomplete and I know it.
3. The CAPMAS district pull is still owed. It carries the real district land base, the real district cropping pattern and real district yields. Three illustrative parts of version one exist only because that pull is missing.
4. The water quota figures from the Ministry of Water Resources and Irrigation are still owed. Version one calibrates its expected budget just under the water demand of the current pattern and declares that choice in the code.
5. The hydrology literature pull is still owed, so the scenario scaling and probabilities are declared judgment, sensitivity testing still to come.
6. The extension guidance pull is still owed, so crop water requirements are midpoints of published ranges, not Egyptian extension values.
7. The yield response to water shortfall is linear in my model. Real yield response curves bend. The paper will state this as a limit.

## My verdict on version one

The model runs end to end and passes its own falsification test at crop mix level, on real yields and a real crop mix, with illustrative money. The stress result is the finding I would lead with: the system absorbs a 10 percent water cut in money and breaks on food at 20 percent, and the break lands first in Beheira. The next work is data, not code. CAPMAS first, then FAOSTAT prices direct, then the quota and hydrology pulls. When those land, every illustrative label in this note either comes off or the number changes in public.
