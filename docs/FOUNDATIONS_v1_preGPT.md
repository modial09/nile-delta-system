# Foundations of the Nile Delta project

Version 1, written 14 November 2026. This document is the base the whole project is built on. It states the problem, the value for each stakeholder, the data the model stands on, how the parts connect, the computations and the method. It is built from the data foundation, the second mining sweep, and the reassessment and upgrade design. One step remains open by design: the external review from GPT will be read against this document, and the combined version will replace this one before the build starts.

## 1. The problem and the end goal

Egypt grows most of its food in the Nile Delta with a fixed share of Nile water. Each season, someone decides, in practice if not on paper, which districts and which crops get that water. Today that decision has no published price for a guarantee: nobody can say what it costs, in farm income, to promise that staple food output will hold in a dry year, or what one more cubic metre of water is worth in one district against another.

The end goal of this project is to make that decision priced and visible. The model must answer three questions with numbers a decision maker can use. What cropping plan holds staple output at a stated floor across dry and normal years. What that promise costs, stated honestly. And what water is worth, district by district and year type by year type, at the margin. Every computation in this project exists to serve those three answers. A result that does not serve one of them does not ship.

## 2. The value, by stakeholder

For farmers, the value is a plan that protects income in the bad year, not only in the average year. The model reports what a cropping plan earns in expectation and what it loses in the worst years, so a farmer facing it can see the trade in his own terms: margin kept in a normal year against margin protected in a dry one. The guarantee floor is stated as a share of the staple output farmers produce today, never as an abstract target.

For government agencies, in the Ministry of Water Resources and Irrigation and the Ministry of Agriculture, the value is a priced guarantee and a district water value table. A planner who must defend an allocation can point to the cost of each level of food security, to the districts where water earns most at the margin, and to the years where the promise breaks. The project also returns something the agencies do not publish today: measured water consumption by governorate from satellite data, computed in this project from public rasters.

For my professors and the academic team who will read this work, the value is method they can examine. Every forecast carries its own backtest error. Every stale series is either forecast under a stated rule or carried as a named gap with its cost stated. The model is a known structure used without decoration, the claims are limited to what the prior work review proved, and the data appendix lets any reader rebuild every input. The project proves readiness by the standard of its evidence, not by the size of its headline.

## 3. How the parts connect

The project has four layers, and each layer passes a defined product to the next.

The data layer holds every input with its source, its year and its unit. It produces one clean parameter set and one gap register. Nothing enters the model from outside this layer.

The forecasting layer reads the long price and yield series from the data layer. It produces, for each crop, a forecast for the next planting season and a band around that forecast taken from measured backtest error. Those two products, the expected value and the band, are what the allocation layer consumes. No hand set price or yield enters the model again.

The satellite layer reads public WaPOR rasters and produces measured actual water consumption by governorate and season for 2018 to 2025. That product calibrates the water side of the allocation model and replaces the conversion from net to applied water that the old versions rested on.

The allocation layer is the model itself. It reads the parameter set, the forecasts and their bands, the measured consumption, and the inflow record. It produces the plan, the priced guarantee at each floor level, the water value for each district in each year type, and the shortfall in the bad tail. The paper is written from these outputs and from nothing else.

## 4. The data the model stands on

Land, cropping pattern and yields by governorate come from the Ministry of Agriculture Agricultural Statistics Bulletins, read first hand. The eight governorate panel for 2020 to 2021 is complete for the five crops, and two further seasons were added in the second sweep.

Costs stand on two official bulletin families. The CAPMAS income bulletin gives 2015 to 2017. The Ministry cost bulletin, the Bulletin of Cost Statistics and Net Return (نشرة إحصاءات التكاليف وصافى العائد), published by the Economic Affairs Sector (قطاع الشئون الاقتصادية), gives full component costs by crop and governorate from 2019 to 2022. No official cost table exists after 2022. The years after 2022 are forecast territory under the rule in Section 6, carried from the 2022 base with the wheat anchor for 2022 to 2023 as a check, and every such figure is labelled an estimate.

Prices come from the FAOSTAT prices domain. Wheat, maize and potatoes now run to 2024 in the December 2025 vintage. Rice and sugar beet farm gate prices stop at 2023 and are carried as named gaps. The sugar beet factory procurement price is documented separately, to an announced 2,300 pounds per tonne for 2026 to 2027, because the farmer sells to the factory and the two prices answer different questions. The model runs the beet price as a stated choice between the two concepts, never as a silent default.

Water stands on three legs. Field measured applied water and consumptive use, read in the original Egyptian journals, now exist for wheat, rice, maize and sugar beet under Delta conditions, with sugar beet arbitrated at about 5,600 to 6,600 cubic metres per hectare. Satellite measured consumption from WaPOR covers the whole Delta for 2018 to 2025. And the inflow record is the gauged Aswan series, 1871 to 1970, labelled as gauged flow and never as natural flow. The national frame is the National Water Balance for 2025, 65.35 billion cubic metres of fresh water, which supersedes the older conflicting totals.

The gaps that remain are named here so the build never trips over them silently: no year by year flow record after 1970; the 1978 to 1987 drought known only as a period mean; the rice price after 2023; the rice yield response factor unverified in its original source; no published release series for the Delta, so the model area water budget stays a calibration on the release side while becoming measured on the consumption side; and the Menoufia rice cell for 2020 to 2021, which its own source leaves blank.

## 5. The Arabic research layer

Part of this research must be in Arabic, because the primary record of Egyptian agriculture is in Arabic. This is a structural part of the foundation, not a translation task at the end. The rule is: for any Egyptian primary source, search in Arabic first, read the table in the original, and record the Arabic title beside the English one in the data appendix. The largest find of the project, the Ministry cost bulletin, sat in a public catalogue under its Arabic title and was missed for weeks because the first pass searched for the English republication. The field trial literature that arbitrated sugar beet water lives in Egyptian university journals, most of them Arabic first. The mining method from the second sweep stands as the project standard: follow the institutions own platforms, the ministry uploads index, the FAO catalogue and the Egyptian Knowledge Bank journals, before general web search.

## 6. The method

The forecasting module is built first, before any new allocation run. For each crop it forecasts next season price and next season yield. The candidates are a ridge regression, a random forest and a gradient boosting model, and two naive lines that any real model must beat: last value carried forward, and a drift line from the recent trend. Features use only information available before the season being forecast: lagged values, a time trend, lagged fertilizer price and lagged planted area. Selection is per crop, by backtest score, and the full score table ships, including the crops where nothing beats the naive line. The backtest is rolling origin over at least ten test seasons for prices and over twenty for yields, and it reports root mean squared error, mean absolute error, mean absolute percentage error and skill against the naive line. The band that enters the model is the empirical spread of the one step backtest errors. A forecast is never printed, in the paper or in a run log, without its error beside it.

Costs after 2022 follow the gap rule, because no honest training series exists for them: forecast from the official base where a defensible method exists, print the error beside the figure, or carry the year as a named gap. One rule governs every stale or missing input in the project: find it recent, or forecast it from history with the forecast tested on at least ten years and its error printed beside every use, or carry it as a named gap with the cost of the gap stated. No silent carries.

The allocation model is a two stage stochastic linear program over eight governorates and five crops. The first stage fixes planted area before the year type is known. The second stage allocates water inside each year type, with yield loss under deficit irrigation set by the crop response factors. The objective is expected farm margin at forecast prices and the stated cost basis, reported as an index against the current pattern wherever the cost years force it, so that no margin ever again mixes two economies and calls the result a level. The staple guarantee enters as a floor on wheat, rice and maize output at stated levels of current production, and the model reports the cost of each level. The scenario set has two layers: inflow states from the Aswan record, and price and yield states set by the forecast bands, with the independence between the layers stated as a named assumption. Two additions repair the known blind spots of the earlier versions. A multi year drought state enters the scenario set, because storage makes the multi year run the real risk. And a sampled robustness run over the inflow record reports the guarantee ceiling as a distribution, with the expected staple shortfall in the worst decile of scenarios printed as a headline measure, because a food guarantee is a promise about the tail.

The outputs are read under three disciplines. Water values are dual values and are reported as marginal values only; an average return per cubic metre is never called a price. Every gain figure travels with its decomposition, so the reader can see how much comes from the plan improving and how much from the baseline being graded harder. And every claim in the paper is limited to the combination the prior work review proved, with the word first used only where that review earned it.

Layer two of the original design, the fertilizer routing model, is outside this foundation. The reassessment proposes the cut and this foundation is written for the core alone: forecasting, satellite calibration and the allocation model, with the paper as the final product. The routing layer returns only if the core is finished and written early enough that it cannot endanger the paper.

## 7. The build order

First, the remaining data jobs: the direct FAOSTAT crops pull, the extractions from located bulletins, and the WaPOR zonal statistics that produce measured consumption by governorate. Second, the forecasting module, with its full backtest tables. Third, the allocation model rebuilt on forecast inputs, measured consumption and the enlarged scenario set. Fourth, the audit of the new run, by the same standard as before: independent replay of the baseline, an independent solver on any infeasibility claim, and errors reported first. Fifth, the paper, written last, from the audited run only.

## 8. The combination step

This foundation was written from our own materials, as instructed. When the GPT review of the audit package arrives, it will be read against this document claim by claim. What it proves against us, we adopt and record. What it asserts without evidence, we test before adopting. The combined foundation that results is the version the build starts from, and this version is kept so the change is visible.
