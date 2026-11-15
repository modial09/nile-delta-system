# Pricing the Food Guarantee: A Stochastic Water Allocation Model for the Nile Delta

Mohamed Diallo
November 2026

## Abstract

Egypt grows most of its food in the Nile Delta with a fixed share of Nile water, and every season that water is divided among districts and crops. What nobody publishes is the price of the food promise: what it costs, in farm income, to guarantee that staple output holds in a dry year, and what one more cubic metre of water is worth in one district against another. I built a two stage stochastic allocation model for eight Nile Delta governorates and five crops, on published district data, official cost bulletins read in Arabic, satellite measured water consumption, and price and yield forecasts that carry their own backtest errors. The model prices a staple guarantee as a ladder. A guarantee of 80 percent of a reference tonnage built from observed areas and published yields is the highest ladder level the model can hold in every scenario, the exact ceiling is 80.25 percent, and holding the 80 percent level costs 227,935,234,023 pounds of expected margin against the same model left free, on a basis of forecast 2024 prices and official 2022 costs. The historical planting pattern holds no guarantee inside this model. Left to profit alone under a water cut, the model plants no staples at all, while its physical capacity to produce them stays high. Water values, reported as marginal duals by governorate and scenario, complete the price list a decision maker needs.

## 1. The problem

Egypt's share of Nile water is fixed by agreement at 55.5 billion cubic metres a year. Most of the country's food grows in the Nile Delta, on about 1.68 million hectares of physical land across the eight governorates I study: Beheira, Kafr El Sheikh, Dakahlia, Gharbia, Menoufia, Sharkia, Qalyubia and Damietta. Each year the same hard question returns. Which districts and which crops get the water, and what does that choice promise the people who eat?

In practice the allocation is made, season by season, through canal schedules, area controls on thirsty crops such as rice, and long habit inside the ministries. Analytical tools exist at ministry level, and published optimisation models of Egyptian agriculture exist too. What does not exist in the open is a price list for the promise itself. A planner who wants to promise that wheat, rice and maize output will hold in a dry year cannot read anywhere what that promise costs the farmers who must keep it, level by level. A planner who must move water between districts cannot read what the last cubic metre earns in each district in a dry year against a normal one.

I set out to build that price list, and to build it in a way a reader can check. The model in this paper answers three questions. What cropping plan holds staple output at a stated floor across dry and normal years? What does that promise cost, measured against the same model free to maximise income, and between one floor level and the next? And what is water worth, district by district and year type by year type, at the margin?

## 2. What was already built, and what was left open

I am not the first to model Egyptian water, and this paper claims no such thing. Egypt has a sector model tradition of three decades: Lofgren (1996) modelled the cost of managing with less water, He and co authors (2006) derived shadow prices for irrigation water at national scale by solving their model at different water quantities, and McCarl and co authors (2015) carried the same lineage into climate scenarios. Gohar and Ward (2010) optimised water and land jointly along the Nile with food security constraints held, and Gohar, Cashman and El bardisy (2021) built the fullest Egypt allocation model I found, with 22 crops, three seasons and welfare tracked. Stochastic programming reached Egyptian cropping early: Rosa and Yates (1994) brought it to the sector model, and El Shazly and co authors (2009) ran a named two stage stochastic model on the Egyptian cropping pattern with food security among its purposes. The two stage structure itself is textbook material since Huang and Loucks (2000). On the food floor, Adly and co authors (2018) computed the income cost of one fixed wheat self sufficiency floor at national scale, a fall of 13.3 percent in total net revenue. Abdelkader and Elshorbagy (2021) set out the national trade off between margin, water demand and food self sufficiency as a set of patterns for policy makers to choose among. Water values for Egypt exist at national scale (Yates and Strzepek, 1998; Fuglie and co authors, 2021) and by farm survey inside one Delta district (Saleh, 2018).

What that record leaves open is the combination a Delta planner actually faces in one place: a model restricted to the Delta at governorate level, with the planting decision taken before the inflow is known, a staple floor swept level by level with the margin cost of each level reported, and a water value for each governorate under each inflow scenario, all benchmarked against the observed current cropping pattern rather than a planned one. That combination is the contribution of this work, stated in the form my prior work review supports: I implement an exploratory governorate scale stochastic allocation model for eight Nile Delta governorates, compare outcomes against historical crop areas, and report staple floor feasibility, conditional expected margins, and scenario specific water duals. It is not a new method, and nothing in this paper claims otherwise.

Two lessons from the field literature discipline the reading of every result below. Ghazouani and co authors (2014) show that Delta farmers plant thirsty crops at canal tail ends for household food security, know how and neighbour practice, not for profit alone; farmers already run an informal food floor of their own, and an optimised pattern is a direction and a price signal, not an instruction anyone will simply follow. El Agha, Molden and Ghanem (2011) measured about half of main canal supply returning to drains and groundwater in a Delta command, so field level water savings are not system level savings; my model works on applied duties at district level and claims no saving of that kind.

## 3. The data, including the parts that had to be found in Arabic

Every number in the model comes from a named source, listed with its years and units in Appendix A. Land, cropping pattern and district yields come from the Agricultural Statistics Bulletins of the Ministry of Agriculture, read first hand: the eight governorate panel for 2020 to 2021, with the potato season split from 2021 to 2022 and one Menoufia rice cell from 2019 to 2020, because its own source leaves the 2020 to 2021 cell blank. The model keeps two land quantities apart at all times: physical cultivated area, 1,676,580 hectares, which limits each season, and annual cropped area, 3,176,474 hectares, which describes the year and limits nothing, because a field carrying two crops is still one field.

Costs taught me the largest lesson of the project. My first pass, in English, found only the CAPMAS income bulletin and stopped at 2017. The fuller official series, the Bulletin of Cost Statistics and Net Return of the Economic Affairs Sector, sits in the ministry catalogue under its Arabic title, and it gives component costs by crop and governorate through 2022. The model stands on those 2022 costs, rent included. No official cost table exists after 2022, and I carry that as a stated limit rather than a silent one: every margin in this paper is on one basis, forecast prices at the 2024 level with official 2022 costs, and the same basis applies to both sides of every comparison.

Prices come from the FAOSTAT prices domain, and yields and areas from a direct pull of the FAOSTAT crops domain. Water duties are applied water figures under Delta conditions: the CAPMAS duty table carried by Abdelwahab and co authors (2024) for most crops, field trial evidence from Egyptian journals for sugar beet, arbitrated at 5,600 to 6,600 cubic metres per hectare with the midpoint 6,100 in the primary run. Satellite data plays a validation role only: WaPOR measures total water consumption over all surfaces in each governorate at a mean of 24.416 billion cubic metres a year over 2018 to 2025, and my modeled baseline demand of the modeled crops at full applied duties, 16.398 billion cubic metres, sits below that total in every governorate, which is the order the two definitions require. The two measures cover different things, so I derived no calibration scalar from the comparison.

The inflow record is the gauged flow at Aswan from 1871 to 1970: one hundred years, a mean of 91.94 billion cubic metres and a standard deviation of 16.92. From that record I built four inflow states for the Delta, dry, normal, high and a multi year drought state, with budgets of 8.588, 10.502, 13.434 and 9.580 billion cubic metres for the model area and probabilities of 0.2275, 0.4451, 0.3165 and 0.0110 taken from the record itself. The model area budget is a calibration, because no published release series for the Delta exists; it is labelled as such wherever it matters.

## 4. Forecasts, with their errors, and one honest verdict

The model does not eat hand set prices or yields. I built a forecasting module first. For each crop it forecasts the next season price and the next season yield, with five candidates: a ridge regression, a random forest, a gradient boosting model, and two simple lines any serious model must beat, last value carried forward and a drift line. Backtests are rolling origin, with thirteen test seasons for wheat, maize and potato prices, ten test seasons for paddy rice and sugar beet prices, and twenty four test seasons for yields for every crop, and selection is per crop by backtest error.

The verdict on prices is plain, and I print it because hiding it would poison everything downstream: no learning model beat the simple lines on any of the five price series. The drift line won for every crop. The 2024 price forecasts the model consumes are wheat 10,296.94 pounds per tonne with a backtest root mean squared error of 1,485.60 and a mean absolute percentage error of 14.61 percent; paddy rice 19,394.14, error 3,735.60, 14.47 percent; maize 14,836.22, error 1,998.12, 15.64 percent; sugar beet 820.52, error 92.26, 10.21 percent; and potatoes 8,405.44, error 1,396.76, 19.52 percent. On yields the learners did win in places: a random forest carries wheat, maize and sugar beet, a ridge regression carries potatoes, and the naive line carries rice, because every learner lost to it. The full score tables, including every losing model, are part of the project record, and no forecast appears anywhere in this paper without its error beside it. The low and high price and yield states in the model are set by the spread of those backtest errors, so the uncertainty the plan must survive is measured, not chosen.

## 5. The model in brief

The model is a two stage stochastic program over the eight governorates and five crops, with potatoes carried as three seasonal crops, winter, summer and Nili, because their areas, costs and water figures differ by season. Planting is decided at the two moments a farmer actually faces. Winter planting is fixed before the year type is known. Summer and Nili planting are decided with the year type observed, because by then the inflow is known. Water is allocated inside each season and each scenario. Appendix C gives the structure in full, in enough detail to rebuild it.

Three design choices carry the honesty of the results. First, land binds by season: in each governorate and season, the modeled crops may use at most the physical cultivated area minus a reserve for the crops I do not model, built from their observed areas, so no plan can plant land that does not exist in that season. Second, crop failure is a real decision: in any scenario the model may abandon a planted crop, taking no water and yielding nothing, with the planting cost already sunk, exactly as a written off field behaves. A kept crop must receive at least a minimum viable share of its water requirement, set at 0.30 and stated as an assumption. Third, the guarantee is a hard floor in every scenario, stated in the exact words the model uses: every represented scenario delivers at least the stated share of a modeled reference quantity of aggregate wheat, paddy rice and summer maize tonnage. The reference quantity is 12,254,407 tonnes, built from observed areas times published district yields: wheat 4,617,795 tonnes, paddy rice 4,086,080 tonnes and summer maize 3,550,533 tonnes. The floor protects that aggregate tonnage. It says nothing about each crop on its own, about calories, or about milled rice, and I do not read it as saying more.

The scenario set has twelve members: the four inflow states crossed with three price and yield layers, expected, low and high, the layers set by the forecast error bands. Prices and yields in a layer move together, and the layers are treated as independent of the inflow state; that independence is a named assumption of the design.

## 6. Findings

### 6.1 The price of the guarantee

The guarantee is a ladder, and each rung has a price. The table gives expected farm margin at each floor level, on the common basis of forecast 2024 prices and official 2022 costs, with the cost of each level measured two ways: against the unconstrained optimum of the same model, and against the next lower level.

| Floor, share of the reference tonnage | Expected margin, pounds | Cost against the unconstrained optimum, pounds | Cost against the next lower level, pounds |
| --- | --- | --- | --- |
| 0 percent, unconstrained | 403,078,762,407 | 0 | 0 |
| 50 percent | 297,739,198,932 | 105,339,563,475 | 105,339,563,475 |
| 60 percent | 262,520,406,731 | 140,558,355,676 | 35,218,792,201 |
| 70 percent | 223,222,240,454 | 179,856,521,953 | 39,298,166,277 |
| 75 percent | 202,983,384,826 | 200,095,377,581 | 20,238,855,628 |
| 80 percent | 175,143,528,384 | 227,935,234,023 | 27,839,856,442 |
| 85 percent and above | infeasible | | |

Read as a decision maker reads it: the first half of the reference tonnage is the most expensive promise on the ladder, at about 105 billion pounds of expected margin, because the free model would rather grow potatoes than staples at these prices. Each further step costs between about 20 and 39 billion. And the ladder ends. A capacity run that maximises the tonnage held in every scenario puts the ceiling at 9,833,867 tonnes, 80.25 percent of the reference quantity. Floors of 85 percent and above cannot be held in this model at all.

The ceiling is a result about this stated model, and I print it with its band, because my audits showed it moves when its conditions move. Under the reserve construction of the primary run, on published district yields, it is 80.25 percent. Under the uncapped proportional split of the reserve it is 80.12 percent. With no reserve held at all, pool limits at physical area, it is 90.94 percent. On the sensitivity that scales district yields to the forecast national level, it is 75.62 percent. With named rotation and market sanity caps added, it is 77.44 percent. I do not claim the Delta itself cannot protect more than 80.25 percent; I claim that this model, on this data, with land and water as stated, cannot promise more, and that the honest answer to a minister is a band with its conditions, not a point.

One more property of the ladder matters as much as its prices. At every floor level, the margin optimal plan is exactly tight in its hardest scenarios: the smallest headroom above the floor is zero tonnes, and it is a four way tie, tight throughout the low price and yield layer in all four inflow states at once. A promise bought at the margin carries no slack. Whatever breaks first, a slightly worse year, a slightly lower yield, takes the plan below its floor, and Section 6.7 measures how often that happens under sampled hydrology.

### 6.2 The pattern Egypt actually plants holds no guarantee

The benchmark matters, because a price list means little without the present beside it. Evaluated inside the same model on the same basis, the historical planting pattern earns an expected margin of 86,006,146,997 pounds, delivers expected staple tonnage of 8,908,274 tonnes, about 72.69 percent of the reference quantity, and delivers 7,367,358 tonnes in its worst scenario, about 60.12 percent. Inside this model, the pattern Egypt actually plants holds no guarantee at any level on the ladder. That is a result of this model on this data, and I state it in exactly those terms.

The accounting difference between the unconstrained optimised margin and the historical margin is 317,072,615,410 pounds, 368.66 percent of the baseline margin. I call it accounting and attach no cause to any input, and the next paragraph is the reason no reader should take that number at face value.

### 6.3 The warning that travels with every margin

The free model loves potatoes beyond anything a market would absorb. Against observed areas, the unconstrained optimum plants winter potatoes at 16.91 times the observed area, summer potatoes at 22.69 times and Nili potatoes at 366.22 times; at the 80 percent floor the multiples are still 9.32 for summer potatoes and 97.76 for Nili potatoes. The model prices potatoes as if any area could sell at the forecast price. At these multiples it could not. Every margin in this paper should be read with that warning attached: the levels and the differences between levels carry the information; the absolute pound figures rest on fixed prices that the plan itself would move. This is also why the guarantee is so expensive at the first rung. The opportunity cost of staples is priced against a potato margin that a real market would not pay at that scale.

### 6.4 Stress: capacity is physics, the empty plan is a choice

Two stress runs cut every district budget, to 0.90 and to 0.80 of its stated value, with no floor imposed. Each run reports two numbers, and I keep them apart in every sentence. At the 0.90 scale, the maximum staple tonnage the land and water can still hold in every scenario is 9,049,077 tonnes, 73.84 percent of the reference quantity. The profit objective, left to itself at the same budgets, chooses zero staple tonnes, with an expected margin of 375,091,832,795 pounds. At the 0.80 scale the pair is 8,264,287 tonnes of capacity, 67.44 percent, and again zero staples chosen, with a margin of 343,134,636,238 pounds. The first number in each pair is physics. The second is a choice of the objective. A reader who reports only the second number would say food production collapses under a water cut; a reader who reports only the first would say nothing is wrong. Both halves are the finding: under stress, the capacity to feed people survives far better than the incentive to do it at these prices, and that gap is exactly what a guarantee exists to close.

### 6.5 What water is worth at the margin

Water values are the marginal duals of the district water constraints, taken from the linear relaxation of the same formulation at a floor of 80.15 percent, and converted to conditional values per scenario. They answer one question only: what one more cubic metre would earn, in that district, in that scenario, at the margin of the current plan. No average return per cubic metre is reported as a price anywhere in this paper.

In the dry inflow state at expected prices and yields, one more cubic metre is worth between 47.39 and 64.32 pounds across the eight governorates, and water binds in all eight. In the normal inflow state the range is 19.17 to 53.54 pounds, Damietta the lowest and Sharkia the highest. In the high inflow state it is 11.81 to 14.64 pounds. In the dry state at low prices the relaxation duals spike to between 1,073.50 and 1,240.34 pounds; that spike is a property of the relaxation at a near ceiling floor in the hardest scenario, and I print it because it is in the results, not because anyone would pay it.

One caution belongs to these ranges, and the independent reaudit earned it. The ranges above are the ranges of one optimal dual solution, the one my solver returned. Dual solutions are not unique in this relaxation, and another optimal solution moves some governorate values: the reaudit, solving the same relaxation to the same optimal objective, found Damietta in the normal inflow state at expected prices at 16.68 pounds per cubic metre, below the quoted minimum of 19.17. The levels and the ordering, dry years dearer than wet ones, Damietta low and Sharkia high in the normal state, are the robust content. Any single district value should be read as the value in one optimal solution, not as a constant of nature.

### 6.6 The value of knowing, and the plan built on averages

At the 80 percent floor, the wait and see value, the margin available to a planner who knew each scenario before planting, is 198,927,633,193 pounds, against a recourse value of 175,143,528,384, so the expected value of perfect information is 23,784,104,809 pounds. That is the most that better forecasts, better inflow prediction and better price information together could be worth inside this model at that floor, which makes it a budget line for information, not a compliment to it.

The plan built on averages fails, and the failure is a finding. Planned at the true probability weighted means of budget, prices and yields, the true mean budget being 10.9844 billion cubic metres, the resulting plan cannot hold the 80 percent floor in 10 of the 12 scenarios; it holds only in the normal inflow state at high prices and in the high inflow state at high prices. A standard value of the stochastic solution therefore does not exist for this benchmark, and I do not report one. Under a named penalised variant, with a penalty of 25,000 pounds per tonne of staple shortfall, the penalised value of the stochastic solution is 7,607,863,594 pounds, and it carries the word penalised wherever it travels. The practical reading is short: a plan built on average water is not a guarantee strategy, and the difference between the two is worth billions.

### 6.7 How the promise behaves across sampled years

A floor held in twelve constructed scenarios is one thing; a promise kept across the run of real years is another. I fixed the plan at the 80 percent floor and drew 100 samples from the inflow record, alternating single years and ten year window means, evaluating each with late season planting frozen at the normal inflow variant of the fixed plan, because a sampled budget carries no state label of its own. Every sample result is saved in the project files, and the figures here recompute from that file. The plan holds its 80 percent floor in 65.0 percent of samples. The maximum share it could hold runs from 55.28 percent in the worst sample through a median of 82.03 percent to 82.67 percent at best. In the worst decile of samples, the expected staple shortfall against the floor is 1,103,686 tonnes; across all samples the mean shortfall is 156,385 tonnes. A food guarantee is a promise about the tail, and the tail here says: at 80 percent, the promise breaks about one year in three under historical hydrology, by about 1.1 million tonnes when it breaks badly. Anyone who sets the level should set it with that sentence in the room.

### 6.8 The sugar beet test

One variant repeats the frontier with sugar beet at the documented factory procurement price of 2,400 pounds per tonne instead of its forecast farm gate level of 820.52 pounds per tonne (backtest root mean squared error 92.26 pounds, mean absolute percentage error 10.21 percent). The margins come out identical at every level tried, because the model plants no sugar beet at either price: potatoes rule beet on both land and water in this parameter set. The two runs differ in price concept, year and marketing basis together, and I attribute nothing about their comparison to the price concept alone. The result still earns its place: a policy debate about the beet price is, inside this model, a debate about a crop the optimiser would not plant at either price, which redirects the debate to the constraints and prices that actually bind.

## 7. What a decision maker should do with this

First, choose the guarantee level as a budget decision, from the price list, not as a slogan. Each level now has a stated price against the free optimum and against the level below it, and the choice between 70, 75 and 80 percent is a choice between about 20 and 39 billion pounds a step. A level chosen without its price is a promise made blind.

Second, when weighing one more point of guarantee, compare its price with the cost of the alternative way of covering the same tonnage: importing it. The ladder gives the domestic margin cost of one more guaranteed tonne at each level; set beside the import cost of that tonne, it tells the planner which instrument is cheaper at which level, and the answer will not be the same at 60 percent as at 80.

Third, use the water values as marginal signals, district by district and year type by year type, and never as tariffs or averages. They say where one more cubic metre earns most in a dry year, which is where protection, maintenance and delivery discipline buy the most food. They do not say what water should cost a farmer, and this paper does not pretend otherwise.

Fourth, do not read the optimised pattern as a planting instruction. Its potato areas are beyond any market, and farmers plant for household security and know how as much as for margin, as the field evidence shows. The pattern is a direction and a price signal. The instruments that move real planting, area rules, procurement prices, extension and credit, sit outside this model.

Fifth, plan the failure of the promise, not only the promise. A margin optimal plan at any floor is exactly tight in its hardest scenarios, and the sampled record says the 80 percent plan breaks in about one year in three. A guarantee at that level needs its partner instruments ready in advance: import cover, stocks, or a stated lower promise for dry sequences. The drought state and the worst decile shortfall, about 1.1 million tonnes, are the quantities to plan against.

Sixth, spend on information where the model prices it. The expected value of perfect information at the 80 percent floor is about 23.8 billion pounds. Real forecasting buys only a part of that, but the number sets the scale of what inflow prediction, price information and district data are worth chasing, and it argues for the unglamorous work first: published release data for the Delta, and cost and price series that do not stop in 2022 and 2023.

## 8. Limits, stated where they belong

The margins rest on fixed prices, and the potato warning of Section 6.3 is the largest single limit: at the areas the free model chooses, prices would fall, so absolute pound figures are conditional in a way the ladder differences only partly escape. The inflow record ends in 1970, because no year by year record after 1970 was obtainable for this project; the state probabilities rest on that record, and the drought state is built from the lowest ten year window mean inside that record itself; the 1978 to 1987 drought falls after the record ends, is known only as a published period mean, and does not enter the model at all. The model area water budget is a calibration, since no published Delta release series exists. Costs stop at the official 2022 bulletin while prices sit at a forecast 2024 level, a mixed basis I state rather than hide, adopted because it is the most recent official cost data that exists. The winter potato cost is a named gap: winter potatoes carry the summer potato cost as a stated assumption, and a sensitivity at the Nili potato cost raises the unconstrained margin to 436,283,724,443 pounds while the 90 percent floor stays infeasible on that cost as well. The rice yield response factor of 1.20 is unverified in its original source and is carried with a tested range of 1.00 to 1.40, across which the ceiling does not move. The water values are duals of one optimal solution among several, as Section 6.5 states. And every feasibility statement in this paper is a statement about this model on this data, never a claim about what the Delta itself can or cannot do.

## References

Abdelkader, A. and Elshorbagy, A. (2021). ACPAR: A framework for linking national water and food security management with global conditions. Advances in Water Resources, 147, 103809.

Abdelwahab, H. F., Negm, A. M., Ramadan, E. M., Kuriqi, A. and Abd Elaty, I. (2024). Mitigating water shortages and enhancing food security through crop optimization: Insights from the Eastern Nile Delta. Acta Scientiarum Polonorum, Formatio Circumiectus, 23 (4), pages 61 to 76.

Adly, N., Nosier, S., Kassem, N., Mahrous, M. and Salah, R. (2018). Modelling the optimal cropping pattern to 2030 under different climate change scenarios: A study on Egypt. African Journal of Agricultural and Resource Economics, 13 (3), pages 224 to 239.

Basheer, M., Nechifor, V., Calzadilla, A., Siddig, K., Etichia, M., Whittington, D., Hulme, M. and Harou, J. J. (2021). Collaborative management of the Grand Ethiopian Renaissance Dam increases economic benefits and resilience. Nature Communications, 12, 5622.

CAPMAS. Annual Bulletin of Estimates of Income from the Agricultural Sector, editions for 2015 to 2016 and 2016 to 2017; and the CAPMAS irrigation water duty table of 2017, as carried in Abdelwahab and co authors (2024).

Cobb, G. W. (1978). The problem of the Nile: conditional solution to a change point problem. Biometrika, 65, pages 243 to 251, Table 1.

Doorenbos, J. and Kassam, A. H. (1979). Yield response to water. FAO Irrigation and Drainage Paper 33, Food and Agriculture Organization of the United Nations, Rome. Yield response factors as carried in FAO Papers 56 and 66.

El Agha, D. E., Molden, D. J. and Ghanem, A. M. (2011). Performance assessment of irrigation water management in old lands of the Nile Delta of Egypt. Irrigation and Drainage Systems, 25 (4), pages 215 to 236.

El Shazly, F. A., Mansour, M. E. E., Ahmed, M. A. and Shehata, E. A. (2009). Egyptian cropping pattern under risk and varying domestic and international circumstances. Conference Towards Development of New Policies to Promote the Agricultural Sector in Egypt, Cairo University, with FAO and partner institutes. MPRA Paper 42634.

FAO. FAOSTAT, Prices domain and Crops and livestock products domain, Egypt. Bulk downloads accessed November 2026.

FAO. WaPOR, the FAO portal to monitor Water Productivity through Open access of Remotely sensed derived data, version 3, Level 2 actual evapotranspiration and interception at 100 metres. Accessed November 2026 through the FAO GISMGR catalogue.

Fuglie, K., Dhehibi, B., El Shahat, A. A. I. and Aw Hassan, A. (2021). Water, policy, and productivity in Egyptian agriculture. American Journal of Agricultural Economics, 103 (4), pages 1378 to 1397.

Ghazouani, W., Molle, F., Swelam, A., Rap, E. and Abdo, G. (2014). Understanding farmers adaptation to water scarcity: a case study from the western Nile Delta, Egypt. IWMI Research Report 160.

Gohar, A. A. and Ward, F. A. (2010). Gains from expanded irrigation water trading in Egypt: An integrated basin approach. Ecological Economics, 69, pages 2535 to 2548.

Gohar, A. A., Cashman, A. and El bardisy, H. A. E. H. (2021). Modeling the impacts of water land allocation alternatives on food security and agricultural livelihoods in Egypt: Welfare analysis approach. Environmental Development, 39, 100650.

He, L., Tyner, W. E., Doukkali, R. and Siam, G. (2006). Policy options to improve water allocation efficiency: Analysis on Egypt and Morocco. Water International, 31 (3), pages 320 to 337.

Huang, G. H. and Loucks, D. P. (2000). An inexact two stage stochastic programming model for water resources management under uncertainty. Civil Engineering and Environmental Systems, 17 (2), pages 95 to 118.

Lofgren, H. (1996). Cost of managing with less: cutting water subsidies and supplies in Egypt's agriculture. IFPRI TMD Discussion Paper 7.

McCarl, B. A. and co authors (2015). Climate change vulnerability and adaptation strategies in Egypt's agricultural sector. Mitigation and Adaptation Strategies for Global Change, 20, pages 1097 to 1109.

Ministry of Agriculture and Land Reclamation, Economic Affairs Sector. Agricultural Statistics Bulletins, editions for 2019 to 2020, 2020 to 2021 and 2021 to 2022, governorate tables of area, production and yield.

Ministry of Agriculture and Land Reclamation, Economic Affairs Sector. Bulletin of Cost Statistics and Net Return (نشرة إحصاءات التكاليف وصافى العائد), editions covering 2019 to 2022.

Ministry of Water Resources and Irrigation (2016). Water Strategy to 2050, December 2016. Egypt Nile share of 55.5 billion cubic metres a year.

Ministry of Water Resources and Irrigation (2026). National Framework for Water Resources Allocation, August 2026, printing the approved National Water Balance for 2025, fresh water total of 65.35 billion cubic metres.

Nile gauged flow series at Aswan, 1871 to 1970, from Cobb (1978), Table 1, as distributed in the R datasets package as the Nile series.

Rosa, C. H. and Yates, D. (1994). Addressing the issue of uncertainty within the Egyptian Agricultural Sector. IIASA Working Paper WP 94 097.

Saleh, E. M. (2018). The economic value and cost recovery of water in the Egyptian irrigated agriculture. Egyptian Journal of Agricultural Research, 96 (2), pages 787 to 813.

World Bank (2022). Egypt Country Climate and Development Report.

Yates, D. N. and Strzepek, K. M. (1998). An assessment of integrated climate change impacts on the agricultural economy of Egypt. Climatic Change, 38, pages 261 to 287.

## Appendix A. Data

Every parameter the model consumes, with its value, its source, its years and its unit. Areas, pattern and district yields are from the Agricultural Statistics Bulletins of the Ministry of Agriculture and Land Reclamation, Economic Affairs Sector, Part 2, Tables 17 and 19 for land and the governorate area, production and yield tables for the pattern. The baseline mixes two cropping years, as Section 1 of the results note states in plain words: areas for wheat, sugar beet, rice, summer maize and Nili maize from the 2020 to 2021 panel, potato areas in all three seasons from the 2021 to 2022 season split, and one Menoufia rice cell from 2019 to 2020 because its own source leaves the 2020 to 2021 cell blank. Two rounding facts belong here. The unrounded reference tonnage sum is 12,254,407.16 tonnes and prints as 12,254,407, while the three rounded components below sum to 12,254,408; the one tonne difference is component rounding only. And the reference tonnage is observed areas times published district yields by construction, so it differs slightly from the sums of the bulletin production column, by 399 tonnes for wheat, 68 for rice and 83 for maize, because the published yields are themselves rounded conversions.

| Parameter | Value | Source | Years | Unit |
| --- | --- | --- | --- | --- |
| Physical cultivated area, Beheira | 387,540.72 | Ministry Agricultural Statistics Bulletin, Table 17, via capmas_governorate_total_cropped_area.csv | 2020 to 2021 | hectares |
| Physical cultivated area, Sharkia | 375,274.20 | Same table | 2020 to 2021 | hectares |
| Physical cultivated area, Dakahlia | 271,077.24 | Same table | 2020 to 2021 | hectares |
| Physical cultivated area, Kafr El Sheikh | 228,117.96 | Same table | 2020 to 2021 | hectares |
| Physical cultivated area, Gharbia | 159,438.72 | Same table | 2020 to 2021 | hectares |
| Physical cultivated area, Menoufia | 141,087.24 | Same table | 2020 to 2021 | hectares |
| Physical cultivated area, Qalyubia | 66,784.20 | Same table | 2020 to 2021 | hectares |
| Physical cultivated area, Damietta | 47,260.08 | Same table | 2020 to 2021 | hectares |
| Physical cultivated area, total | 1,676,580.36, printed 1,676,580 | Sum of the eight rows above | 2020 to 2021 | hectares |
| Annual cropped area, Beheira | 720,838.86 | Ministry Agricultural Statistics Bulletin, Table 19, via the same file | 2020 to 2021 | hectares |
| Annual cropped area, Sharkia | 679,537.74 | Same table | 2020 to 2021 | hectares |
| Annual cropped area, Dakahlia | 533,501.22 | Same table | 2020 to 2021 | hectares |
| Annual cropped area, Kafr El Sheikh | 450,194.64 | Same table | 2020 to 2021 | hectares |
| Annual cropped area, Gharbia | 308,141.82 | Same table | 2020 to 2021 | hectares |
| Annual cropped area, Menoufia | 269,171.70 | Same table | 2020 to 2021 | hectares |
| Annual cropped area, Qalyubia | 119,479.92 | Same table | 2020 to 2021 | hectares |
| Annual cropped area, Damietta | 95,607.96 | Same table | 2020 to 2021 | hectares |
| Annual cropped area, total | 3,176,473.86, printed 3,176,474 | Sum of the eight rows above | 2020 to 2021 | hectares |
| Reference tonnage, wheat | 4,617,795 | Observed areas times published district yields, run log run_v4_1_main.txt | 2020 to 2021 | tonnes |
| Reference tonnage, paddy rice | 4,086,080 | Same construction, with the Menoufia fill noted below | 2020 to 2021 | tonnes |
| Reference tonnage, summer maize | 3,550,533 | Same construction | 2020 to 2021 | tonnes |
| Reference tonnage, total | 12,254,407 | Sum of the unrounded components | 2020 to 2021 | tonnes |
| District yield basis, wheat, area weighted aggregate | 6.87 | Published district yields, 2020 to 2021 panel, DATA_FOUNDATION.md Section 7 | 2020 to 2021 | tonnes per hectare |
| District yield basis, paddy rice, area weighted aggregate | 9.14 | Same, seven reporting governorates, Menoufia not reported that year | 2020 to 2021 | tonnes per hectare |
| District yield basis, summer maize, area weighted aggregate | 8.79 | Same | 2020 to 2021 | tonnes per hectare |
| District yield basis, sugar beet, area weighted aggregate | 49.37 | Same | 2020 to 2021 | tonnes per hectare |
| District yield basis, potatoes all seasons, area weighted aggregate | 28.39 | Same | 2020 to 2021 | tonnes per hectare |
| Applied water duty, wheat | 5,126 | CAPMAS 2017 duty table via Abdelwahab et al. (2024), Table 3; crop_water_requirements_egypt.csv | CAPMAS 2017 | cubic metres per hectare |
| Applied water duty, paddy rice | 16,600 | Same | CAPMAS 2017 | cubic metres per hectare |
| Applied water duty, summer maize | 9,305 | Same | CAPMAS 2017 | cubic metres per hectare |
| Applied water duty, Nili maize | 7,433 | Same table, Nili value printed in the source note of the water file | CAPMAS 2017 | cubic metres per hectare |
| Applied water duty, sugar beet | 6,100, midpoint of the arbitrated range 5,600 to 6,600 | Sakha field trials arbitration, MINING_SWEEP_2.md Target 2, replacing the CAPMAS printed 9,426 and the Gabr net 3,927 | Trials to 2019 | cubic metres per hectare |
| Applied water duty, winter potatoes | 4,079 | CAPMAS 2017 via Abdelwahab et al. (2024); potato_season_split.csv | CAPMAS 2017 | cubic metres per hectare |
| Applied water duty, summer potatoes | 6,145 | Same | CAPMAS 2017 | cubic metres per hectare |
| Applied water duty, Nili potatoes | 6,145, carries the summer duty, stated assumption, no Nili duty exists in the sources | Model code comment; EXTRACTIONS_1B.md Gap 1b B | Assumption | cubic metres per hectare |
| Yield response factor Ky, wheat | 1.05 | FAO Paper 33 via FAO Paper 56, Table 24, and FAO Paper 66, Table 1; fao33_ky_values.csv | Papers of 1998 and 2012 summarising 1979 | dimensionless |
| Yield response factor Ky, paddy rice | 1.20, unverified, tested range 1.00 to 1.40 | No seasonal rice value found in either FAO secondary table; carried in the model with the tested range | Checked November 2026 | dimensionless |
| Yield response factor Ky, maize, summer and Nili | 1.25 | FAO Paper 33 via Papers 56 and 66 | As above | dimensionless |
| Yield response factor Ky, sugar beet | 1.00 | FAO Paper 33 via Papers 56 and 66 | As above | dimensionless |
| Yield response factor Ky, potatoes, all seasons | 1.10 | FAO Paper 33 via Papers 56 and 66 | As above | dimensionless |
| Production cost, wheat, rent included | 37,742.86 | Ministry Bulletin of Cost Statistics and Net Return, Part 1, Table 2; ministry_cost_bulletin_2019_2022.csv | Season 2021 to 2022, the 2022 base | pounds per hectare |
| Production cost, sugar beet, rent included | 39,454.76 | Same bulletin, Part 1, Table 9 | Season 2021 to 2022 | pounds per hectare |
| Production cost, paddy rice, rent included | 41,850.00 | Same bulletin, Part 2, Table 2 | Season 2022 | pounds per hectare |
| Production cost, summer maize, rent included | 37,671.43 | Same bulletin, Part 2, Table 3 | Season 2022 | pounds per hectare |
| Production cost, Nili maize, rent included | 37,888.10 | Same bulletin, Part 2, Table 4 | Season 2022 | pounds per hectare |
| Production cost, summer potatoes, rent included | 86,657.14 | Same bulletin, Part 2, Table 18 | Season 2022 | pounds per hectare |
| Production cost, Nili potatoes, rent included | 54,176.19 | Same bulletin, Part 2, Table 19 | Season 2022 | pounds per hectare |
| Production cost, winter potatoes, rent included | 86,657.14, the summer cost, stated assumption, no winter table exists in the bulletin | Model code comment; FORECASTING_RESULTS.md Section 8.1 | Assumed from season 2022 | pounds per hectare |
| Farm gate price, wheat | 10,000 | FAOSTAT Prices domain; faostat_producer_prices_egypt.csv | 2023 | pounds per tonne |
| Farm gate price, paddy rice | 18,761 | Same | 2023 | pounds per tonne |
| Farm gate price, maize | 14,400 | Same | 2023 | pounds per tonne |
| Farm gate price, sugar beet | 795 | Same | 2023 | pounds per tonne |
| Farm gate price, potatoes | 8,160 | Same | 2023 | pounds per tonne |
| Forecast price for 2024, wheat, drift model | 10,296.94, backtest RMSE 1,485.60, MAPE 14.61 percent | forecast_prices_yields_v4.csv; FORECASTING_RESULTS.md Sections 3 and 5 | Forecast 2024, backtest 2011 to 2023 | pounds per tonne |
| Forecast price for 2024, paddy rice, drift model | 19,394.14, RMSE 3,735.60, MAPE 14.47 percent | Same | Forecast 2024, backtest observed seasons 2011 to 2018 and 2022 to 2023 | pounds per tonne |
| Forecast price for 2024, maize, drift model | 14,836.22, RMSE 1,998.12, MAPE 15.64 percent | Same | Forecast 2024, backtest 2011 to 2023 | pounds per tonne |
| Forecast price for 2024, sugar beet, drift model | 820.52, RMSE 92.26, MAPE 10.21 percent | Same | Forecast 2024, backtest as rice | pounds per tonne |
| Forecast price for 2024, potatoes, drift model | 8,405.44, RMSE 1,396.76, MAPE 19.52 percent | Same | Forecast 2024, backtest 2011 to 2023 | pounds per tonne |
| Procurement price context, sugar beet factory price at 16 percent sugar | 2,400 | procurement_prices_egypt.csv; Sugar and Integrated Industries Company announcement | Season 2024 to 2025 | pounds per tonne |
| Procurement price context, wheat, top grade | 14,667, file value 14,666.67 from 2,200 pounds per ardab of 150 kilograms | procurement_prices_egypt.csv; Ministerial Decree 46 of 2025 | Harvest season 2025 | pounds per tonne |
| Forecast yield for 2025, wheat, random forest | 6.6789, backtest RMSE 0.3250, MAPE 4.05 percent | forecast_prices_yields_v4.csv; FORECASTING_RESULTS.md Sections 4 and 5 | Forecast 2025, backtest 2001 to 2024 | tonnes per hectare |
| Forecast yield for 2025, paddy rice, naive last value | 9.1315, RMSE 0.2696, MAPE 2.12 percent | Same; the forecast equals the last observed value by construction of the selected model | Forecast 2025, backtest 2001 to 2024 | tonnes per hectare |
| Forecast yield for 2025, maize, random forest | 7.6834, RMSE 0.6912, MAPE 6.16 percent | Same | Forecast 2025, backtest 2001 to 2024 | tonnes per hectare |
| Forecast yield for 2025, sugar beet, random forest | 56.0570, RMSE 5.8925, MAPE 6.39 percent | Same | Forecast 2025, backtest 2001 to 2024 | tonnes per hectare |
| Forecast yield for 2025, potatoes, ridge regression | 31.5165, RMSE 1.4879, MAPE 3.10 percent | Same | Forecast 2025, backtest 2001 to 2024 | tonnes per hectare |
| Aswan gauged flow, mean | 91.94, recomputed 91.935 | nile_inflow_aswan_series.csv; Cobb (1978), Table 1, via the R datasets Nile series | 1871 to 1970 | billion cubic metres a year |
| Aswan gauged flow, sample standard deviation | 16.92, recomputed 16.9228 | Same series, recomputed | 1871 to 1970 | billion cubic metres |
| Inflow state, dry | Budget 8.588, ratio 0.7807, probability 0.2275, 23 years below 0.85 times the mean | Model inflow construction, Derivation A bands; run_v4_1_main.txt | Record 1871 to 1970 | billion cubic metres; probability |
| Inflow state, normal | Budget 10.502, ratio 0.9547, probability 0.4451, 45 years | Same | Record 1871 to 1970 | billion cubic metres; probability |
| Inflow state, high | Budget 13.434, ratio 1.2213, probability 0.3165, 32 years above 1.08 times the mean | Same | Record 1871 to 1970 | billion cubic metres; probability |
| Inflow state, drought | Budget 9.580, ratio 0.8709, the lowest ten year window mean ratio, probability 0.0110, one window in 91 | Same, ten year rolling windows | Windows inside 1871 to 1970 | billion cubic metres; probability |
| Model area budget anchor | 11.00, a calibration; no official figure exists for the eight governorate model area | Model code, ANCHOR_BCM, with its calibration comment; DATA_FOUNDATION.md Sections 10 and 11 | Calibration | billion cubic metres |
| Governorate budget rule | Each governorate budget in a state equals the state total times its physical cultivated area divided by the total physical area of 1,676,580.36 hectares | Model code, budget construction | Every inflow state | share |
| National frame, Nile share of Egypt | 55.5 | MWRI Strategy for the Development and Management of Water Resources until 2050, December 2016; egypt_water_budget_anchors.csv | Agreement share | billion cubic metres a year |
| National frame, National Water Balance fresh total | 65.35, components Nile 55.50, non renewable groundwater 7.90, rainfall and floods 1.30, desalination 0.65 | MWRI National Framework for Water Resources Allocation, August 2026, printing the approved National Water Balance for 2025; MINING_SWEEP_2.md Target 4 | Balance for 2025 | billion cubic metres a year |
| WaPOR measured total consumption, eight governorates, mean | 24.416 | wapor_aeti_governorate_2018_2025.csv; WAPOR_METHODS.md Section 4; total consumption over all surfaces in each governorate polygon, no cropland mask | 2018 to 2025 | billion cubic metres a year |
| WaPOR measured total consumption, single year | 24.378 | Same file, Delta total row | 2023 | billion cubic metres |
| Modeled baseline demand at full applied duties | 16.398 | Run log WaPOR comparison; baseline areas times applied duties, modeled crops only | Baseline pattern | billion cubic metres |
| Model constant, minimum viable water share | 0.30 | Model code, MIN_VIABLE_SHARE | Constant | share of the full duty |
| Model constant, shortfall penalty in the penalised variant | 25,000 | Model code, penalised variant; run log | Variant | pounds per tonne |
| Menoufia rice fill | Area 7.98 hectares from the 2019 to 2020 panel; yield filled with the area weighted mean of the seven published district yields, 9.138; the fill contributes 72.92 tonnes to the rice reference | Run log fill print; the 2020 to 2021 source cell is blank and is never treated as zero | 2019 to 2020 area; 2020 to 2021 yield fill | hectares; tonnes per hectare; tonnes |

## Appendix B. Glossary

Stochastic program: an optimisation model that plans under uncertainty. Some decisions are taken before the uncertain outcome is known, and the rest adjust after it is known, and the plan is judged on its expected result across the possible outcomes.

Two stage: the timing shape of such a model. First stage decisions are fixed before the outcome is known; second stage decisions, called recourse decisions, respond to the outcome once it arrives.

Scenario: one complete possible future inside the model. In this paper a scenario is one inflow state combined with one price and yield layer, and the model carries twelve of them, each with a probability.

Guarantee, or staple floor: a hard minimum the plan must meet in every scenario. Here it is a stated share of a reference quantity of aggregate wheat, paddy rice and summer maize tonnage. A plan that misses the floor in even one scenario is not accepted.

Reference quantity: the tonnage the floor shares refer to, built from observed crop areas multiplied by published district yields. It is a yardstick built from the observed pattern, not a forecast and not a measure of what Egypt eats.

Dual variable: a number the solver attaches to a constraint, equal to the change in the best achievable objective if that constraint is relaxed by one unit. The dual on a district water constraint is the marginal value of water in that district and scenario.

Shadow price: another name for a dual variable when the constraint is a resource, such as water or land. It is a marginal value at the current plan, not a market price and not an average return.

Marginal value: the value of one more unit, holding the rest of the plan at its margin. One more cubic metre, one more hectare. Marginal values change as the plan changes; average values do not answer the same question.

Expected margin: the probability weighted average of farm margin across the twelve scenarios, where margin is crop revenue minus the full production cost including rent, on the paper stated basis of forecast 2024 prices and official 2022 costs.

Expected value of perfect information: the difference between what a planner could earn if each scenario were known before planting, and what the best plan earns without that knowledge. It prices information itself.

Value of the stochastic solution: the gain from planning with the scenario structure instead of planning at the average values of the uncertain inputs. In this paper the average value plan cannot hold the floor, so no standard value exists, and only a penalised variant is reported.

Abandonment: the model decision to write off a planted crop in a scenario. The crop takes no water and yields nothing, and its planting cost is already paid. It is the model form of a field a farmer gives up on in a bad year.

Yield response factor, Ky: a number that says how strongly a crop yield falls when its water falls short of the full requirement. A Ky of 1.25 means a ten percent water shortfall costs about twelve and a half percent of yield, in the linear relation the model uses.

Applied water duty: the volume of water a crop is charged per hectare in this model, in cubic metres per hectare, measured on the applied basis, the water delivered to the field, as distinct from the smaller net requirement the crop itself consumes.

Backtest: a test of a forecasting method against history, run as if the forecaster stood in each past season and could use only what was known then. The errors of those rehearsals are the backtest errors printed beside every forecast in this paper.

Reserve: the land in each governorate and season held back from the modeled crops, standing for the crops this model does not carry. The plan may not plant into the reserve.

Feddan: the Egyptian land unit used in the source bulletins. One feddan is 4,200 square metres, about 0.42 hectares. All areas in this paper are stated in hectares.

## Appendix C. Methods

This appendix states the model exactly as built in src/allocation_model_v4_1.py, in enough detail for another analyst to rebuild it. The solver is CBC, called through PuLP, with primal and dual feasibility tolerances at the CBC default of 0.0000001 and a relative gap of zero. Water is carried inside the solver in thousands of cubic metres for numerical scaling, and every printed figure is converted back to cubic metres.

Sets. Governorates d: Beheira, Sharkia, Dakahlia, Kafr El Sheikh, Gharbia, Menoufia, Qalyubia and Damietta, with total physical cultivated area 1,676,580 hectares and total annual cropped area 3,176,474 hectares, the second figure a descriptor only, never a constraint. Activities c, eight: wheat, sugar beet and winter potatoes in the winter pool; rice, summer maize and summer potatoes in the summer pool; Nili maize and Nili potatoes in the Nili pool. Inflow states s: dry, normal, high and drought. Price and yield layers l: low, expected and high, with probabilities 0.25, 0.50 and 0.25, the forecast band read as quartiles. Scenarios are the twelve pairs of one inflow state and one layer, with probability equal to the product of the two state probabilities, the layers treated as independent of the inflow state.

Inflow states. The record is the gauged Aswan flow series, 1871 to 1970, mean 91.935 billion cubic metres. Band edges are 0.85 and 1.08 times the record mean. Dry holds the 23 years below the lower edge, normal the 45 years between the edges, high the 32 years above the upper edge; each state ratio is the mean flow in its band divided by the record mean, giving ratios of 0.7807, 0.9547 and 1.2213. The drought state uses the 91 ten year rolling window means of the same record: its ratio is the minimum window ratio, 0.8709, and its raw probability is the share of windows at or below that ratio, one window in 91. The three single year probabilities are scaled by one minus the raw drought probability, giving final probabilities of 0.2275, 0.4451, 0.3165 and 0.0110. The budget of a state is 11.00 billion cubic metres times its ratio: 8.588, 10.502, 13.434 and 9.580 billion cubic metres. The 11.00 figure is the calibration anchor for the model area. The governorate budget in a state is the state total split by physical cultivated area share.

Prices and yields by layer. The price of a crop in the expected layer is its forecast value; in the low and high layers, its forecast band low and band high. Forecast, low and high prices in pounds per tonne: wheat 10,296.94, 9,500.80, 12,951.11; paddy rice 19,394.14, 19,324.81, 23,480.32; maize 14,836.22, 14,561.64, 19,061.05; sugar beet 820.52, 793.52, 972.06; potatoes 8,405.44, 8,143.20, 9,609.40. The expected yield of a crop in a governorate is its published district yield. The low and high layer yields are the published district yield multiplied by the group ratio of band low to forecast, and band high to forecast, from the forecast yield bands: wheat 6.6789, 6.4854, 7.1477 tonnes per hectare; paddy rice 9.1315, 8.8217, 9.3594; maize 7.6834, 7.3823, 8.2055; sugar beet 56.0570, 51.1310, 59.5386; potatoes 31.5165, 30.3124, 32.4186. The backtest errors of these forecasts, root mean squared error and mean absolute percentage error, are: prices, wheat 1,485.60 and 14.61 percent, paddy rice 3,735.60 and 14.47 percent, maize 1,998.12 and 15.64 percent, sugar beet 92.26 and 10.21 percent, potatoes 1,396.76 and 19.52 percent; yields, wheat 0.3250 and 4.05 percent, paddy rice 0.2696 and 2.12 percent, maize 0.6912 and 6.16 percent, sugar beet 5.8925 and 6.39 percent, potatoes 1.4879 and 3.10 percent.

Decision variables. Winter planting xw, by governorate and winter activity, 24 continuous variables, one value common to all scenarios. Late planting xs, by governorate, late activity and inflow state, 160 continuous variables. Served area a, water w and a keep binary k, each by governorate, activity and scenario, 768 of each. Production q is not a variable but a linear expression in a and w.

Objective. Maximise expected margin: the probability weighted sum over scenarios, governorates and activities of price times production, minus planting cost charged once on planted area. Winter planting cost enters with weight one. Late planting cost for each inflow variant enters weighted by that inflow state probability. There is no water cost term anywhere in the objective. Costs, pounds per hectare, rent included, official 2022: wheat 37,742.86; sugar beet 39,454.76; rice 41,850.00; summer maize 37,671.43; Nili maize 37,888.10; summer potatoes 86,657.14; Nili potatoes 54,176.19; winter potatoes 86,657.14, the summer cost carried as a stated assumption because no winter potato cost exists in the bulletin.

Land constraints and the reserve. For each governorate, winter planting sums to at most the winter pool limit; for each governorate and inflow state, summer planting sums to at most the summer pool limit and Nili planting to at most the Nili pool limit, each variant fitting its pool on its own. A pool limit is the physical cultivated area minus its reserve. The reserve is built in two steps. First, the annual unmodeled area of the governorate, its annual cropped area minus the total observed modeled area, is split across the three pools in proportion to the observed modeled area of each pool. Second, each pool reserve is capped at the free land of that pool, the physical area minus the observed modeled area of the pool, and floored at zero. By construction no pool limit can fall below the observed modeled area of its pool, and the observed historical pattern is feasible in all 24 pools. The reaudit records the cost of the cap on the books: the capped reserves sum to 30,136 hectares less than the annual unmodeled area, and that area receives no seasonal home in any pool.

Water constraints. For each governorate and scenario, total water over the eight activities is at most the governorate budget of that scenario. Applied water duties, cubic metres per hectare: wheat 5,126; rice 16,600; summer maize 9,305; Nili maize 7,433; sugar beet 6,100, the midpoint of the arbitrated range of 5,600 to 6,600; winter potatoes 4,079; summer potatoes 6,145; Nili potatoes 6,145, the summer duty carried as a stated assumption.

Production and abandonment. Yield response factors Ky: wheat 1.05, rice 1.20 labelled unverified, summer and Nili maize 1.25, sugar beet 1.00, potatoes 1.10 in all three seasons. For a served cell, production q equals the layer yield times served area times one minus Ky, plus the layer yield times Ky divided by the water requirement times water applied; in words, the yield on the served area falls by Ky times the share by which water falls short of the full requirement. Coverage, water applied divided by the full requirement on the served area, is forced between 0.30 and 1.00 for a kept crop by two constraints: water at most the requirement times served area, and water at least 0.30 times the requirement times served area. The binary linkage makes served area equal planted area when k is 1, and equal zero when k is 0: served area is at most planted area, at most a big bound times k, and at least planted area minus the big bound times one minus k. The big bound is the pool limit when a plan is being optimised, and the planted area of the cell itself when a plan is fixed for evaluation, because a solver produced plan can sit a fraction of a hectare above a pool limit inside solver tolerance and a pool limit bound would then make its own recourse infeasible. With k at 0, served area and water are zero, production is zero, and the planting cost stands: abandonment is a real write off, not a refund.

The floor. Staple activities are wheat, rice and summer maize. The reference tonnage is the sum over governorates and staple activities of baseline area times published district yield: 12,254,407 tonnes. For a floor share f above zero, one constraint per scenario requires that scenario staple production to be at least f times the reference tonnage. The floor binds scenario by scenario, never in expectation and never crop by crop.

Named caps, in the capped mode only. Planting of each activity in a governorate, and each late variant separately, is at most a share of district physical land: wheat 0.50, rice 0.35, summer maize 0.40, Nili maize 0.40, sugar beet 0.30, and each potato activity 0.15.

Derived computations. The ceiling replaces the objective with a single variable t, constrained to sit at or below the staple production of every scenario, and maximises t; the ceiling share is t divided by the reference tonnage. Clearance fixes a saved plan and, scenario by scenario in single scenario builds with the planted cell bound, maximises staple tonnage; clearance is that maximum minus the floor tonnage, and the plan clearance reported is the smallest across the twelve scenarios. The expected value problem plans at the true means: budget 10.9844 billion cubic metres, prices and yields each the layer probability weighted mean with weights 0.25, 0.50 and 0.25, solved as one deterministic problem, its late planting for every inflow state set to the normal variant of that solve, and the extracted plan then evaluated over all twelve scenarios. The wait and see value runs twelve deterministic solves, one per scenario at that scenario prices, yields and budgets, with each scenario margin recomputed as revenue minus the full planting cost of the plan for that inflow state, and takes the probability weighted sum; the expected value of perfect information is the wait and see value minus the recourse value. The penalised variant replaces the hard floor in a scenario with a shortfall variable charged at 25,000 pounds per tonne in the objective. The stress runs set the floor to zero and scale all governorate budgets by 0.90 or 0.80, solving once for maximum held staple tonnage and once for maximum margin. The robustness run fixes the 80 percent floor plan, draws 100 samples with a seeded generator of seed 20261114, alternating a single year and a ten year window mean from the Aswan record, sets each sample budget to 11.00 times the draw ratio to the record mean, freezes late planting at the normal inflow variant, and maximises staple tonnage at expected prices and yields; every sample result is saved to data/processed/robustness_samples_v4_1.csv. The dual table comes from the linear relaxation, identical except that the keep binaries are continuous between 0 and 1, at a floor of the ceiling share minus a tenth of a percentage point, 80.1476 percent. A conditional dual is the absolute CBC dual of a water constraint divided by 1000, to return from solver units to pounds per cubic metre, and then divided by the scenario probability.

## Appendix D. Sensitivity: what moves the results and what does not

The guarantee ceiling is the headline most exposed to its conditions, so it is tested first. Under the primary reserve construction on published district yields the ceiling is 80.25 percent of the reference quantity. Under the uncapped proportional split of the reserve it is 80.12 percent, so the reserve cap does the consistency work and almost none of the ceiling work. With no reserve held at all, the ceiling is 90.94 percent. On scaled district yields it is 75.62 percent. With the named rotation and market caps added, it is 77.44 percent. The honest statement is the band: on the published yield basis the ceiling sits at about 80 percent under any reserve construction that admits the observed pattern, and the choice to hold no reserve at all is what would move it toward 91 percent, at the cost of letting the plan plant land that other crops demonstrably use.

Family by family relaxations of the ceiling problem, computed in the independent reaudit, locate what binds. Winter land binds in all eight governorates at the ceiling solution, and water binds in 47 of the 96 governorate and scenario cells. Tripling the dry inflow state water raises the ceiling to 87.65 percent. Holding the floor only in the expected price and yield layer, rather than in every layer, raises it to 82.91 percent, which shows the low yield layer binds: it is low yields, more than low water alone, that cap the promise. Removing the minimum viable water share of 0.30 changes the ceiling not at all. Dropping the drought state changes it not at all, because the dry state binds harder.

Two parameter ranges were swept directly and moved nothing. The sugar beet duty across its arbitrated range of 5,600 to 6,600 cubic metres per hectare leaves the ceiling unchanged, because the ceiling solution plants no sugar beet. The rice yield response factor across 1.00 to 1.40 leaves it unchanged, because the ceiling solution plants no rice in any inflow state. A parameter that moves nothing because the crop is absent is a different kind of robustness from a parameter that is well measured, and the paper reports the reason beside the result so the two are not confused.

The winter potato cost gap is the sensitivity with the largest money effect. Winter potatoes carry the summer potato cost of 86,657.14 pounds per hectare as a stated assumption, the winter cost being absent from the located bulletins. At the Nili potato cost of 54,176.19 pounds per hectare instead, the unconstrained expected margin rises from 403,078,762,407 to 436,283,724,443 pounds, while the 90 percent floor stays infeasible on either cost. The cost assumption moves the money; it does not move the feasibility story.

Budget stress moves capacity and choice in opposite readings, as Section 6.4 reports: scaling all district budgets to 0.90 leaves a staple capacity of 73.84 percent of the reference quantity while the profit objective chooses zero staples; at 0.80 the capacity is 67.44 percent and the choice is again zero. The sugar beet price concept moves nothing: at the factory procurement price of 2,400 pounds per tonne the frontier margins are identical to the primary run at every level tried.

The water values carry their own sensitivity, of a mathematical kind. Because the dual solution is not unique, individual governorate values move between optimal dual solutions: the reaudit alternative solution spans 48.63 to 64.32 pounds in the dry state at expected prices against the printed 47.39 to 64.32, 12.00 to 14.64 in the high state against the printed 11.81 to 14.64, and puts Damietta at 16.68 in the normal state against the printed minimum of 19.17. The orderings and the dry to wet gradient survive every solution found; the second decimal of any single district value should not be quoted as a finding.
