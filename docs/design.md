# Design

## Architecture at a glance

Forecasting module produces scenario parameters. Problem One consumes them and produces a planting pattern and water values. Problem Two consumes the planting pattern and produces delivery routes and costs. Validation runs against every layer.

## Problem One: allocation under uncertainty

Sets: districts D, crops C, inflow scenarios S with probabilities p.

Parameters: land available per district; water requirement per crop per hectare; expected yield per crop and district; expected producer price per crop; production cost per hectare; the seasonal water budget per scenario; minimum required production for staple crops.

Decision variables, stage one: hectares planted to each crop in each district, chosen before the inflow is known. Decision variables, stage two: water allocated to each planting under the scenario that occurs, and any shortfall against the ideal water requirement.

Objective: maximise expected total farm margin across scenarios, where margin is revenue less production cost, with a penalty on water shortfall that reflects yield loss.

Constraints: total planted area per district at or below available land; total water allocated per scenario at or below that scenario budget; staple crop production at or above the food security floor; water per planting at or below its agronomic requirement.

Dual reading: the shadow price on each district water constraint is the money value of one more cubic metre of water in that district. The shadow prices are a primary output, reported as the water value map.

Solution method: the deterministic core is a linear program solved with an open solver through PuLP or scipy. The stochastic version is the extensive form across three scenarios. I report the expected value of perfect information and the value of the stochastic solution, because both numbers state, in money, why modelling uncertainty beats planning on the average year.

## The forecasting module

Targets: next season producer price and yield for each modelled crop, at national level first, by district where the series supports it.

Features: lagged values of the target, trend, lagged fertilizer price, and lagged planted area. No feature may use information from the season being forecast.

Models: a ridge regression baseline, a random forest, and a gradient boosting model. The baseline exists so the flexible models must earn their place.

Evaluation: rolling origin backtesting. Train on earlier years, forecast the next, roll forward. Report mean absolute error and mean absolute percentage error per crop and per model, in full, including where the simple baseline wins.

Output into Problem One: forecast means set the expected prices and yields; forecast spread across backtest errors widens or narrows the scenario band. Forecast uncertainty therefore enters the optimization as data, not as a footnote.

## Problem Two: fertilizer distribution

Inputs: planted hectares by crop and district from Problem One; published fertilizer application rates per crop, giving demand in tons by district and nutrient; depot locations; district collection points.

Distances: pairwise road distances between depots and collection points computed with SCGraph on its world highways geograph, which is built on OpenStreetMap. Sample distances are validated against known road distances before any route result is reported.

Model: assign each district to a depot and sequence deliveries as a capacitated routing problem on a reduced instance, one governorate group first. A nearest neighbour plus local improvement heuristic gives the working solution; an exact solve on the smallest instance checks the heuristic gap.

Outputs: routes, total kilometres, cost per ton delivered, and the comparison against the naive rule in which every district is served by its nearest depot with no route planning.

## Data

The full source list with pull status lives in `data/SOURCES.md`. Rules: every file in `data/raw/` is untouched source data; every transformation happens in code; every number in the paper traces to a file and a transformation.

## Testing plan

1. Baseline test: the model allocation against the actual cropping pattern, same prices, same water. The headline comparison of the paper.
2. Backtest: earlier years only, judged on data the model did not fit.
3. Stress test: water budgets reduced by 10 percent and by 20 percent.
4. Sensitivity: prices and costs moved across plausible bands; shadow price stability reported.
5. Routing check: SCGraph sample distances against known distances; heuristic gap on the small exact instance.

## Stakeholder plan

Stage one, design and build: no stakeholder contact. The first job is technical validity on public data.

Stage two, after the core model stands, planned for December: three to five structured conversations, one cooperative manager, one fertilizer distributor, one or two farmers. Their job is assumption auditing: collection point realism, application rate realism, and whether any operator would act on an allocation recommendation. We ask about their current practice, never whether they like the model, to avoid politeness bias.

Stage three, the paper: their answers are reported as a reality check section. The paper does not depend on their approval, and no claim rests on a conversation.

## Timeline

Weeks 1 to 2: data pull, source notes, data cleaning, first descriptive notebook.
Weeks 3 to 4: deterministic allocation model, baseline comparison, shadow price extraction.
Week 5: forecasting module and backtests; scenario parameters generated.
Week 6: stochastic allocation, stress tests, value of information measures.
Weeks 7 to 8: routing layer on the reduced instance; stakeholder conversations in parallel.
Week 9: paper completion, release with DOI, one page brief.

Scope rule: the core allocation work and its writing ship first. The routing layer ships only if the core is finished and written. If time tightens, routing is cut and the contribution to SCGraph stands on its own track.

## Outputs and artifacts

The working paper, submitted to SSRN. The public code release with a Zenodo DOI. The one page plain English brief. The SCGraph contribution runs as a parallel track under its own checkpoints and is not part of this repository.

## Risks I am managing openly

Public district level series may be thinner than national series; the fallback is a national model with district land shares. Scenario probabilities are judgment, declared as such and sensitivity tested. Fertilizer rates vary by soil and practice; the stakeholder audit exists to catch a rate that no operator recognizes.
