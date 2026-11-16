# My Nile Delta Project: A Walk Through

Mohamed Diallo, November 2026

## The one question

Egypt eats about 20.6 million tonnes of wheat each year. Egypt grows part of that wheat in the Nile Delta. The rest comes from ships.

My project asks one question. What does it cost to promise that the Delta will grow a set share of the wheat Egypt eats, even in a dry year?

The promise has a price. The price is farm profit given up. If farmers must plant more wheat, they plant less of other crops. Some of those crops pay more. The profit they lose is the price of the promise.

I state the promise in two units. The first is wheat cover: the share of the wheat Egypt eats that Egypt grows at home. The second is months of stock: the same amount, counted in months of eating. A promise of 25 percent cover is a promise of 5.15 million tonnes of wheat. That is 3.0 months of stock.

## The land and the crops

The model covers eight governorates in the Delta. It works with the real land: 1,676,580 hectares of farm land.

There are three planting seasons in a year. Winter is the main season. Summer comes next. Nili is a short third season in late summer. A field can grow two or three crops in one year, so the model counts land season by season.

The model plants nine crops. Wheat is the crop of the promise. Rice is bounded by law: the state sets the rice area each year by decree, and the model obeys the decree. Berseem is a green feed crop for animals. It is the largest winter planting in the Delta, and it fights wheat for the same winter land. Sugar beet, maize and potatoes fill the other seasons.

## The main variables, in plain words

| Thing | What it means | Where it comes from |
| --- | --- | --- |
| Land | The farm land of each governorate, by season | Ministry farm statistics |
| Water | The water each governorate may use in a season | A built total, split by land share; a user can replace it |
| Yield | The tonnes one hectare grows | Published district yields |
| Price | What one tonne sells for at the farm gate | A forecast from past prices, with a low and a high band |
| Cost | What one hectare costs to grow, rent inside | Official cost books, moved to 2025 prices |
| The floor | The least wheat the plan must grow in every scenario | The promise level I choose to test |
| Margin | The profit of the whole plan | Price times harvest, minus all costs |

## How the parts link

Water is the tight input. My total water is a built number: 11.00 billion cubic metres. No book prints this number. I built it to fit the size of the system, and I say so every time I use it. The model splits the total across the eight governorates by their share of land. That split is a guess, and it is the weakest part of the model. Section three of this walk through says what I do about that.

The river today is a managed river. Lake Nasser stores water behind the High Dam. Each year, the water a farmer gets is a release decision, not raw nature. So my scenarios start from the lake. A scenario has a storage start: low, normal or high. It has an inflow year: dry, normal or high. One stated rule turns the pair into a water budget. A high lake covers part of a dry year. A low lake holds water back so it can refill. On top of the water, each scenario has a price and yield band: low, expected or high. Nine water states times three bands give 27 scenarios.

Planting has two decision moments. Winter planting is fixed before the year shows itself. One winter plan must serve all 27 scenarios. Summer and Nili planting come later, when the water state is known. After a scenario shows itself, the plan can still move water between crops, and it can drop a crop and lose its cost. That late freedom is called recourse. It is strong: the model sees the whole scenario before it moves the water. Real farmers see less. So every price I print is a low estimate of the true price. I say this in every document.

The floor binds in every scenario at once. A promise that holds only on average is not a promise. It fails in the dry year, which is the year the promise was bought for.

## The two price lists and how to read one rung

The model prices the promise in two worlds. In the capped world, no crop may take more than a set share of a governorate. This world stays near the pattern Egypt plants now. In the relaxed world, planting is free. There the best plan plants potatoes on up to 22 times their real area, all sold at one fixed price. No market absorbs that. The relaxed list is a benchmark, not a plan.

Read the capped list first. With no promise, the capped plan earns 221.7 billion pounds. A promise of 15 percent cover earns 210.2 billion. The promise costs 11.5 billion. A promise of 20 percent costs 19.5 billion in total. The step from 15 to 20 costs 8.0 billion. A promise of 25 percent costs 28.9 billion in total, and the step from 20 to 25 costs 9.4 billion. A promise of 30 percent cannot be kept at all. The most wheat the capped world can hold in every scenario is 27.8 percent cover. That top point is called the ceiling.

The pattern Egypt plants today already holds 20 percent cover in every scenario. So the real policy question is small and sharp: is the step from 20 to 25 percent worth 9.4 billion pounds?

I also price each promise on the bad tail: the average of the worst quarter of scenarios. The 25 percent promise costs 31.5 billion on the tail, against 28.9 billion on the average. A careful planner budgets from the tail.

## The tests I ran on my own work

I cut the water by a tenth, then by a fifth. The ceiling did not move. Every rung just cost more. Land and the caps bind before water does, because a kept crop may live on 30 percent of its full water and yield less. Water sets the price of the promise, not its top.

I changed the weights on the scenarios, to test if my stated weights drive the answer. They do not. The floor holds in every scenario, so weights move the price only a little. One check on this test failed, and I kept the failure in the record: under one replay, the safe plan held a slightly worse worst case than the plain plan. The gap is 0.02 billion pounds. I claim nothing from that test except that weights matter little here.

I replayed my best plan against real history, the prices and yields of 2015 to 2024. The plan kept its 25 percent promise in only two years of ten. Its middle year reached 24.2 percent cover. This is the hardest fact in the project. The promise is a promise about my scenario set. History is less kind. I print this fact in the paper itself, not in a footnote.

I moved one input at a time to find what moves the price most. The answer is wheat yield. If yields rise by about 11.4 percent, the price of the promise falls by half. If yields fall by a tenth, the price jumps to 45.0 billion pounds. The wheat price is second. The water total is near the last. The cheapest promise policy in this model is better wheat harvests, not more water.

## Bring your own numbers

The weakest input is district water. The ministry holds the real release records. I do not. So the model ships with a blank form. A decision maker can fill in water by district and by source: canals, drainage reuse and groundwater. They can fill in their own crop costs and prices too. A blank cell keeps the public default. A filled cell replaces only that cell. The run log prints which values came from the user and which are defaults. I tested this: with the blank form, the model gives the same numbers as with no form at all. With one cell filled, only that cell changes.

## The weak points, and what I say about them

The water split is built, not measured. I say: the total is a calibration, the split follows land, and I price the error at three water levels. The form lets the holder of the real records replace my split in one step.

The berseem price is built, not measured. No office prints a berseem price. I price berseem by its feed value next to maize, and I test it: a tenth more or less in that price moves the headline price by about 4.0 billion pounds.

The layers are thin. My price and yield bands miss more often than they should. I say: the floors, the ceilings and the steps do not depend on the band weights. Only the average money figures do, and I print the weakness beside them.

The model sees too much. Its late choices use the full scenario. I say: so my prices are low estimates. A promise costed here will cost more in life, never less, on this count.

## What this project proves

The model prices a food promise for the Nile Delta in the units the decision uses: wheat cover and months of stock. It prices each step, not just each level. It tests its own price list against less water, other weights, the bad tail and real history, and it prints the results it does not like. That is the work. The numbers are the start of a budget talk, not the end of one.
