# S1 Decision Definition: what decision this model serves

One page. Written 15 November 2026 under Stage S1, from the paper (paper/Nile_Delta_Paper.md), its methods appendix and docs/FOUNDATIONS.md. Where the record leaves a point open, this page says so rather than filling it.

## The decision maker and the decision

The reader the work serves is a planning authority for the Nile Delta: a ministry level planner who sets seasonal planting guidance for districts and divides irrigation water among them, and who may be asked to promise that staple output will hold in a dry year. The decision the model prices is this: choose a cropping plan for the coming agricultural year, and choose one guarantee level from a ladder, knowing in advance what each level costs in expected farm margin and where the ladder ends. The model does not choose the level. It publishes the price list the choice needs: the margin at each level, the cost of each level against the free optimum and against the level below it, the highest level that can be held at all, and the marginal value of water in each district under each year type.

## Geography, activities and horizon

Geography: eight Nile Delta governorates (Beheira, Kafr El Sheikh, Dakahlia, Gharbia, Menoufia, Sharkia, Qalyubia, Damietta), with physical cultivated area of 1,676,580 hectares as the land that binds, season by season. Annual cropped area of 3,176,474 hectares describes the year and constrains nothing.

Activities: eight crop and season activities built from five crops: wheat, sugar beet and winter potatoes in the winter season; rice, summer maize and summer potatoes in the summer season; Nili maize and Nili potatoes in the Nili season. Land not given to these activities is held in a reserve that stands for all unmodeled crops, built from their observed areas.

Horizon: one agricultural year, planned once, with three seasons inside it. The year is a constructed reference year, not a calendar year: prices sit at a forecast 2024 level, costs at the official 2022 bulletin level, and the planting pattern panel is 2020 to 2021 with potato areas from 2021 to 2022. That mixed basis is stated in the paper wherever the margins travel.

## The water accounting boundary

Water is counted as applied water at district level: each hectare planted is charged a fixed applied duty in cubic metres per hectare, and the sum charged in a governorate may not exceed that governorate budget for the scenario. Governorate budgets are shares of one model area total, split by physical cultivated area. The model area total in a scenario is a calibration anchor of 11.00 billion cubic metres times the inflow state ratio for that scenario. The boundary is therefore the field gate at district scale, on a calibrated total. The model does not simulate canal releases, reservoir operation, conveyance loss, drainage or return flows, and it claims no system level saving. Satellite measured consumption (WaPOR) is used as a validation comparison only, never as the budget.

## Information at each decision date

Winter planting is decided before the year type is known: one winter plan serves all twelve scenarios. Summer and Nili planting are decided after the inflow state is observed, so the plan carries one late planting variant per inflow state, four in all. The price and yield layer is never known at planting time; no decision in the model conditions on it, which is why the guarantee is written as a hard floor in every scenario rather than in expectation. Inside a scenario, a planted crop may be abandoned: it then takes no water, yields nothing, and keeps its sunk planting cost. A kept crop must receive at least 0.30 of its full water duty, a stated assumption.

The scenario set has twelve members: four inflow states (dry, normal, high, and a multi year drought state) built from the Aswan gauged record of 1871 to 1970, crossed with three price and yield layers whose spread is set by the forecast backtest errors. Layers are treated as independent of the inflow state; that independence is a named assumption of the design.

## Exactly what the guarantee protects, and what it does not

The guarantee protects one quantity: the aggregate tonnage of wheat, paddy rice and summer maize together, at or above the chosen share of a reference quantity of 12,254,407 tonnes (observed areas times published district yields), in every one of the twelve scenarios at once. A plan that misses the share in any single scenario is not accepted as holding that level.

The guarantee does not protect any single crop on its own; the mix inside the aggregate is free. It does not protect calories, nutrition or milled rice supply; the rice in the aggregate is paddy. It does not protect household access, food prices or farm income. It does not protect any single governorate; production may move between districts. And it does not protect performance outside the twelve constructed scenarios: when the 80 percent plan is tested against 100 sampled years from the historical record, it holds its floor in 65 of them.

## Primary case and feature classification

Primary case, recommended: keep the current configuration as the primary case, and name it honestly as a constructed reference case on a stated mixed basis (forecast 2024 prices, official 2022 costs, 2020 to 2021 pattern panel with the 2021 to 2022 potato split). Reason: no single calendar year in the current sources carries observed prices, observed costs and a full district pattern at once, because official costs stop at 2022, the full pattern panel is 2020 to 2021, and observed farm gate prices run to 2023 with forecasts for 2024. A nominally current case would hide the same mixing under a single year label. A genuine single year reconstruction becomes possible only if S2 finds the missing tables, and it should then be run as a comparison case, not swapped in silently.

Required core: the two stage allocation model with seasonal land pools and the reserve; the hard floor ladder and its ceiling; the historical pattern benchmark; the information values at the top feasible level; the sampled robustness test of the chosen plan.

Diagnostic sensitivity, kept and labelled: the ceiling band under reserve and yield variants; the named rotation and market caps mode; the budget stress pairs at 0.90 and 0.80; the sugar beet price concept variant; the winter potato cost variant; the relaxation dual tables, labelled as values from one optimal dual solution of the relaxation.

Deferred extensions: the SCGraph supply routing layer; any added crop without district data; any nutritional or household access extension of the guarantee; any live interface over the results. Each waits until the core passes Gate A.
