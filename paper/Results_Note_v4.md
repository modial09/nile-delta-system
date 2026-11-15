# Results note, version 4

I rebuilt the allocation model to Sections 5 and 6 of the combined foundation and ran it in full. The one line a reader should take away is this: in this model a staple guarantee can be held up to about three quarters of the reference tonnage, each step up the ladder has a price in farm margin that I can now state level by level, and the profit objective on its own chooses no staples at all under stress. Every margin in this note is on one basis: forecast prices at the 2024 level with official 2022 costs, in pounds, and the same basis applies to both sides of every comparison.

## 1. What I changed in the model

* Land now binds by season. Winter crops (wheat, sugar beet, winter potatoes) compete for one pool per governorate and summer crops (rice, summer maize, Nili maize, summer potatoes, Nili potatoes) compete for a second pool. Each pool limit is the physical cultivated area of the governorate minus a reserve for unmodeled crops. The eight governorates hold 1,676,580 hectares of physical cultivated area. The annual cropped area of 3,176,474 hectares is a descriptor only and never enters a constraint.
* The reserve is a stated construction, and I state it exactly. No file in this project gives a seasonal total for all crops, so I computed the annual unmodeled crop area of each governorate as its annual cropped area minus the total observed modeled area in the baseline pattern, and I split that annual figure between the winter and summer pools in proportion to the observed modeled area in each pool. The full reserve table is printed in the main run log. This is a construction, not an observed seasonal figure, and I name it as the weakest part of the land layer.
* Planting has two decision points. Winter planted area is one value across all scenarios. Summer planted area is decided per inflow state, four values per governorate and crop, because the inflow is known by summer planting. Summer planting does not vary by the price layer.
* Abandonment is real. In each of the 12 combined scenarios, each planted crop in each governorate carries a binary keep or abandon decision, 768 binaries in all. An abandoned crop gets zero water and zero output and its planting cost is sunk. A kept crop gets a water share between a stated minimum viable share of 0.30 and one, and the yield response relation applies only to kept area. The mixed integer form carried in every run, with frontier solves finishing in at most 21 seconds, so the linear fallback named in the foundation was not used and no renaming was needed.
* District yields are the published district yields, scaled proportionally per crop so the area weighted district mean equals the forecast national yield in the expected state. The low and high yield states use the forecast band ratios in the same way. No rescaling to national means is used in the primary run.
* Scenarios have two layers. The inflow layer has four states from the Aswan record of 1871 to 1970: dry, normal and high from the Derivation A bands as in version 3, plus a multi year drought state whose ratio of 0.8709 is the lowest ten year window mean ratio in the record, across 91 windows. Its probability is a stated construction: the share of ten year windows at or below that ratio, 1 of 91, with the three single year probabilities scaled by one minus that share so the four probabilities sum to one. The price and yield layer has three states from the forecast bands with probabilities 0.25, 0.50 and 0.25, reading the band as quartiles. Independence between the layers is a named assumption. The budget anchor stays the version 3 calibration of 11.00 billion cubic metres for the model area.

## 2. The reference quantity and the floor

The floor is exactly this: every represented scenario delivers at least the stated share of the modeled reference quantity of aggregate wheat, paddy rice and summer maize tonnage. The reference quantity is built from observed areas times published district yields and comes to 12,254,407 tonnes: wheat 4,617,795 tonnes, paddy rice 4,086,080 tonnes and summer maize 3,550,533 tonnes. The floor says nothing about each crop on its own, about calories, or about milled rice.

## 3. The guarantee frontier, primary run, no crop caps

* Floor 0 percent (unconstrained): expected margin 429,588,780,373 pounds.
* Floor 50 percent: expected margin 290,166,264,371 pounds. Cost against the unconstrained optimum 139,422,516,002 pounds. Cost against the next lower level 139,422,516,002 pounds.
* Floor 60 percent: expected margin 243,671,396,588 pounds. Cost against the unconstrained optimum 185,917,383,785 pounds. Cost against the next lower level 46,494,867,783 pounds.
* Floor 70 percent: expected margin 194,764,695,263 pounds. Cost against the unconstrained optimum 234,824,085,110 pounds. Cost against the next lower level 48,906,701,325 pounds.
* Floors of 80, 85, 90, 93, 95 and 100 percent: infeasible, each one proven by solver status at that level, not inferred.

A separate capacity run that maximises the tonnage held in every scenario puts the exact ceiling at 9,246,265 tonnes, which is 75.45 percent of the reference quantity. The ceiling is a result about this stated model, with its budgets, duties, yields and land formulation, and I do not claim that the Delta itself cannot protect more.

With the named constraints added (rotation and market sanity limits, a modelling device: wheat 0.50, rice 0.35, maize 0.40, sugar beet 0.30 and potatoes 0.15 of district physical land), the ceiling falls to 8,842,924 tonnes, which is 72.16 percent of the reference quantity. The capped ladder gives margins of 219,526,150,834 pounds unconstrained, 210,943,640,528 at 50 percent, 195,689,544,155 at 60 percent and 169,267,303,193 at 70 percent, with 80 percent and above infeasible. Feasibility is therefore reported with and without the named constraints, as the foundation requires.

Two controlled sensitivities did not move the ceiling at all: the sugar beet duty across its arbitrated range of 5,600 to 6,600 cubic metres per hectare (the primary run uses the midpoint 6,100), and the rice yield response factor across 1.00 to 1.40 (the primary run carries 1.20, labelled unverified). The labelled rescaling sensitivity, which puts district yields back on the version 3 rescaled basis, lowers the ceiling to 69.62 percent. I report it as a sensitivity only.

## 4. Market absorption warning

The unconstrained optimum rests on potatoes at a scale where the fixed price stops being credible. Against observed areas it plants winter potatoes at 16.72 times, summer potatoes at 9.79 times and Nili potatoes at 953.82 times. At the 70 percent floor the multiples are still 4.18 times for winter potatoes, 5.45 times for summer potatoes and 109.04 times for Nili potatoes. I read every margin in this note with that warning attached: the model prices potatoes as if any area could sell at the forecast price, and no reader should believe that at these multiples.

## 5. Water values

Water values are marginal duals from the linear relaxation of the same formulation at a floor of 75 percent, the ceiling basis, because the 90 percent floor is infeasible in this model. I label them LP relaxation duals and nothing else. Inside a scenario, one more cubic metre is worth, for example, about 44 to 57 pounds in the dry inflow state at expected prices, about 38 to 54 pounds in the normal inflow state at expected prices in the six governorates where water binds hardest, and about 10 to 11 pounds in the high inflow state at expected prices where it binds at all. In the dry inflow state at low prices the relaxation duals spike to about 778 to 920 pounds per cubic metre in every governorate. That spike is a property of the relaxation at a near ceiling floor in the hardest scenario, and I print it because it is in the log, not because I read it as a price anyone would pay. The full table of 96 governorate and scenario cells is in the main run log. No average return is called a price anywhere in this note.

## 6. Information values against true means

The true mean budget, probability weighted across the four inflow states, is 10.9844 billion cubic metres. I computed it from the state budgets and their probabilities; it is not the middle scenario. At the stated floor of 70 percent (the highest feasible ladder level, used because 90 percent is infeasible) the recourse problem value is 194,764,695,263 pounds and the wait and see value is 215,387,623,690 pounds, so the expected value of perfect information is 20,622,928,427 pounds.

The expected value problem, planned at the true means of budget, prices and yields, gives a finding I report plainly: that plan cannot hold the 70 percent floor in 10 of the 12 combined scenarios. It holds only in the normal inflow state at high prices and in the high inflow state at high prices. A standard value of the stochastic solution therefore does not exist for this benchmark, and I do not report one. Evaluated with no floor, the true mean plan reaches 209,970,047,975 pounds, which is an upper bound that flatters it and not an expected result under the guarantee. Under a named penalised variant, with a penalty of 25,000 pounds per tonne of staple shortfall, its penalised expected result is 187,415,904,232 pounds and the penalised value of the stochastic solution is 7,348,791,030 pounds. Both figures carry the word penalised wherever they travel.

## 7. Stress runs, capacity beside choice

* Budgets scaled to 0.90, no floor: maximum staple capacity is 8,560,095 tonnes held in every scenario, 69.85 percent of the reference quantity. The profit objective chooses zero staple tonnes, with an expected margin of 412,488,222,263 pounds.
* Budgets scaled to 0.80, no floor: maximum staple capacity is 7,873,926 tonnes, 64.25 percent of the reference quantity. The profit objective chooses zero staple tonnes, with an expected margin of 386,352,573,081 pounds.

The first number in each pair is physics. The second is a choice of the profit objective, and I keep the two apart in every sentence that uses them.

## 8. Sampled robustness

I fixed the plan at the 70 percent floor, the highest feasible ladder level, since the ceiling of 75.45 percent rules out the 85 percent level. I then drew 100 samples from the inflow record, alternating random single years and random ten year window means with a fixed seed, set each sample budget to 11.00 times its ratio to the record mean, and re solved the recourse for that fixed plan under expected prices and yields, maximising staple tonnage. The maximum feasible floor for the fixed plan across samples has a minimum of 49.21 percent, a 10th percentile of 68.11 percent, a median of 72.04 percent, a mean of 70.85 percent and a maximum of 72.41 percent of the reference quantity. The fixed plan still holds its 70 percent floor in 82 percent of samples. In the worst decile of samples, the expected staple shortfall against the floor reference of 8,578,085 tonnes is 663,137 tonnes. The mean shortfall across all samples is 75,371 tonnes.

## 9. The historical pattern, accounting only

On the same price and cost basis, the historical planting pattern earns an expected margin of 79,671,400,397 pounds, delivers expected staple tonnage of 8,225,526 tonnes, and delivers 6,774,438 tonnes in its worst scenario, about 55 percent of the reference quantity, so the historical pattern holds no guarantee in this model. The unconstrained optimised margin is 429,588,780,373 pounds. The accounting difference between the two margins is 349,917,379,976 pounds, 439.20 percent of the baseline margin. This decomposition is accounting only: it has two components, the baseline margin and the optimised margin, and I attach no causal verb to any input. I also attach the absorption warning of Section 4 to the optimised side, because most of that margin sits on potato area the market would not absorb at a fixed price.

## 10. The sugar beet variant

One variant repeats the frontier at the unconstrained, 70, 80 and 90 percent levels with sugar beet at the documented factory procurement price of 2,400 pounds per tonne, all else equal. The margins come out identical to the primary run at every level tried, because the model plants no sugar beet at either price: potatoes rule beet on both land and water in this parameter set. The two runs differ in price concept, year and marketing basis together, and I attribute nothing about their comparison to the price concept alone. In the primary run beet sits at its forecast farm gate level of 820.52 pounds per tonne, with a backtest root mean squared error of 92.26 pounds and a mean absolute percentage error of 10.21 percent.

## 11. WaPOR calibration verdict

I computed the modeled baseline consumption of the eight governorates as the baseline pattern at full applied duties, which comes to 16.398 billion cubic metres in all, and compared it with the WaPOR totals, which average 24.416 billion cubic metres over 2018 to 2025. The modeled figure sits below the WaPOR total in every governorate, which is the order the two definitions require. I derived no efficiency or requirement scalar from this comparison, because the two sides measure different things: the modeled side covers the modeled crops only on the applied basis, while WaPOR measures total consumption over all surfaces in each governorate, with no cropland mask. WaPOR totals are never cropland consumption in this note. My verdict is that direct calibration is not defensible here and WaPOR serves as validation only.

## 12. Forecasts I consumed, with their errors

Prices for 2024, drift model for every crop: wheat 10,296.94 pounds per tonne (root mean squared error 1,485.60, mean absolute percentage error 14.61 percent); paddy rice 19,394.14 (error 3,735.60, 14.47 percent); maize 14,836.22 (error 1,998.12, 15.64 percent); sugar beet 820.52 (error 92.26, 10.21 percent); potatoes 8,405.44 (error 1,396.76, 19.52 percent). Yields for 2025: wheat 6.6789 tonnes per hectare (error 0.3250, 4.05 percent); paddy rice 9.1315 (error 0.2696, 2.12 percent); maize 7.6834 (error 0.6912, 6.16 percent); sugar beet 56.0570 (error 5.8925, 6.39 percent); potatoes 31.5165 (error 1.4879, 3.10 percent). Costs are the official 2022 bulletin figures with rent included. The winter potato cost is a named gap: I used the summer potato cost of 86,657.14 pounds per hectare for winter potatoes as a stated assumption, and as a sensitivity I reran the unconstrained level at the Nili potato cost of 54,176.19, which raises the unconstrained expected margin to 462,413,066,422 pounds, while the 90 percent floor stays infeasible on either cost.

## 13. Standing assumptions and gaps

* The minimum viable water share for a kept crop is 0.30, stated here and in the code.
* The Nili maize duty of 7,433 cubic metres per hectare is printed in the source note of the water file, so I used it rather than the summer duty. No Nili potato duty exists, so Nili potatoes carry the summer potato duty of 6,145, stated as an assumption.
* Nili potato yields are published for Beheira only, at 18.12 tonnes per hectare, and that published value fills the other governorates after scaling. The Menoufia rice yield cell and four Nili maize yield cells are filled with the area weighted published mean of their crop, and every fill is printed in the main run log.
* The contribution I claim is the one the prior work review supports: I implement an exploratory governorate scale stochastic allocation model for eight Nile Delta governorates, compare outcomes against historical crop areas, and report staple floor feasibility, conditional expected margins, and scenario specific water duals. I claim nothing beyond that combination.

## 14. Files

The model is src/allocation_model_v4.py, run with the project venv python in four modes. The logs are data/processed/run_v4_main.txt, data/processed/run_v4_caps.txt, data/processed/run_v4_beet2400.txt and data/processed/run_v4_robust.txt, and every number in this note traces to a line in one of them. The fixed robustness plan is saved at data/processed/plan_v4_robust_plan.csv.
