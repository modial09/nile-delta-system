# What a Wheat Price Buys: A Delivery Response and Financial Extension of a Stochastic Cover Model for the Nile Delta

Mohamed Diallo
November 2026

## Executive summary

Egypt consumes about 20.6 million tonnes of wheat a year and grows roughly half of that at home (U.S. Department of Agriculture, Foreign Agricultural Service [USDA FAS], 2026; Food and Agriculture Organization of the United Nations [FAO], 2026). Each autumn the state announces a procurement price for the coming harvest, and each spring farmers choose how much of their wheat to deliver to state collection points at that price, and how much to sell to traders, keep or feed to animals. The announcement for the coming season is 2,650 pounds per ardeb of 150 kilograms, set against public demands of 3,000 to 3,500 pounds (Newsroom.info, 2026). This paper prices that announcement. It extends the stochastic Nile Delta allocation model of the companion study, which priced a wheat cover guarantee at a ceiling of 27.83 percent of consumption, with a delivery response fitted to the public record and a financial layer that counts the full cost of each price.

The delivery response is a least squares line of the delivered share of production on the ratio of the state price to the farm gate price, fitted on six seasons, 2019 to 2024: share equals 0.2611 plus 0.1682 times the ratio, with an R squared of 0.866. The line underpredicts both seasons outside the fit, 2025 and 2026, so the analysis carries low, central and high curves throughout. At each price on a grid from 2,200 to 3,500 pounds per ardeb, the model reports deliveries on a production basis of 10.2 million tonnes, the cover and months of stock they buy, and a total programme cost built from the procurement bill, the import cost of the shortfall against the announced target of 5.0 million tonnes, and the carrying cost.

Three results stand out. First, the announced price does not reach the announced target: at 2,650 pounds, central deliveries are 4.357 million tonnes, cover of 21.15 percent or 2.54 months of stock, total programme cost of 97.4 billion pounds, and a gap of 642,721 tonnes costing 11.1 billion pounds to import at the central world price of 313 dollars per tonne. In 2,000 Monte Carlo draws at that price, no draw reaches the target. Second, each extra tonne a higher price attracts costs between 47,156 and 63,350 pounds, roughly three times the price itself, because the higher price is paid on every tonne delivered. Third, the margin contest does not explain the response: wheat would need a price of 5,412 to 6,261 pounds per ardeb to beat berseem on margin, far above the demand range, on a berseem price that is itself a stated construction. The response runs through payment speed, obligation and the pull of the state price on the trader price. An independent check passes thirteen of thirteen tests, one weakly; the study remains a numerically verified exploratory study, not validated empirical evidence.

## 1. Introduction

A wheat procurement price looks like a simple number. In Egypt it is set once a year, in pounds per ardeb, and it is argued over in parliament, in the press and in the fields before it is announced. What the argument almost never contains is a priced forecast of its own consequence: how much wheat the number will actually bring to the state, what that wheat costs in full once the remaining gap is imported and the stock is carried, and what the same number costs in a bad year. The price is signed first. The delivery answer arrives the following summer.

The companion study priced a different promise: that the Delta will grow a stated share of national wheat consumption even when water is short (Diallo, 2026). Its instrument was a two stage stochastic programme over eight governorates, and its headline was a price list for the guarantee, with a capped ceiling of 27.83 percent cover. But a growing promise is not a delivered tonne. Between the field and the state silo stands a choice the farmer makes at harvest, and that choice answers to the procurement price. This paper builds the missing layer. It fits how deliveries have answered the price in the public record, runs a grid of candidate prices through the cropping model of the foundation study, and attaches a financial layer that counts the bill, the import gap and the carrying cost of the stock as one programme cost.

The contribution is the joint pricing. A procurement price, a delivery forecast, an import gap and a stock carrying cost are usually four numbers in four rooms. Here they are one table, priced before the announcement rather than reconstructed after it, with the uncertainty of the behavioural layer printed beside every row instead of averaged away. The methods are standard: a least squares response, a stochastic programme, Monte Carlo simulation, break even analysis and sensitivity ranking. The product is the table and the honesty apparatus around it.

## 2. How Egypt sets the price, and how the crop moves

A reader who does not know Egypt needs three facts before the model makes sense. They are stated here once, compactly, and not repeated.

**The announcement.** The procurement price is a cabinet level decision, announced before the winter planting window opens in mid November so that farmers plant knowing it. For the coming season the Prime Minister announced 2,650 pounds per ardeb, up from 2,500 pounds in the 2026 season (Newsroom.info, 2026). Parliament members and farmer representatives demanded 3,000 to 3,500 pounds (Filcatalog, 2026). The argument is conducted in cost figures: a parliament agriculture committee deputy put the cost of one feddan of wheat at about 50,000 pounds for the new season, against revenue of about 47,700 pounds at the announced price and an average yield of 18 ardebs per feddan, and formal briefing requests asked the ministers of supply, agriculture and finance to review the price (Erem Business, 2026).

**The farmer choice.** At harvest the farmer holds wheat the state wants and the market wants. The state buys at more than 400 collection points and has publicised payment within 48 hours. The alternatives are traders and private mills, home use, and animal feed. Parliament members warned in plain terms what a low price does: farmers cut wheat area, move to crops with faster and higher returns, or sell away from state collection points, and the state imports the difference (Safha News, 2026). The choice is not always free: in 2022 a ministerial decree required every wheat producer to sell a minimum of 12 ardebs per feddan to government purveyors (USDA FAS, 2022). The delivered share of production, the fraction of the national crop that reaches the state, is the summary statistic of this choice, and it is the variable this paper models.

**The gap at the port.** What the state does not collect, it imports, through the General Authority for Supply Commodities. The state set a delivery target of 5.0 million tonnes for the 2026 season and reported about 4.9 million tonnes by mid July 2026; in 2022 it took in 4.2 million tonnes against earlier expectations of 5 to 5.5 million tonnes (USDA FAS, 2022). Import buying is reactive and its cost is documented: the tender of August 2024 sought 3.8 million tonnes and bought 280,000 tonnes, with traders citing payment delays of up to 270 days as the reason offer prices rose (Reuters, 2024). Detailed stock figures are not published continuously; the Minister of Supply told the Senate in October 2026 that disclosure would weaken the state negotiating position with suppliers (Al Hayah News, 2026). A tool of the kind built here would therefore live inside the ministry, and its first user is the official who must sign the price with the bad year priced.

## 3. The foundation in brief

The foundation study models cropping in eight Nile Delta governorates across three planting seasons and nine crops, on 1,676,580 hectares of physical land (Ministry of Agriculture and Land Reclamation, 2025). Winter planting is chosen before the year reveals itself; summer and Nili planting adapt once the water state is observed. A scenario is a Lake Nasser storage state crossed with an inflow year type, turned into a water budget by one stated release rule, and crossed with one of three price and yield layers: 27 scenarios in all. Water scales from a built anchor of 11.00 billion cubic metres that no source publishes, split across governorates by land share. Rice is bounded by the state decree area. Berseem, the clover that feeds Delta livestock and the largest winter planting, competes with wheat for winter land. The wheat guarantee is a hard floor on production that must hold in every scenario at once.

Its headline results, stated here because version 7 builds on them: under planting caps that keep plans near the observed pattern, the guarantee ceiling is 27.83 percent cover, 3.34 months of stock; a 25 percent guarantee costs 28.9 billion pounds of expected farm margin, and 31.5 billion priced on the worst quarter of scenarios; the pattern Egypt actually plants holds 20 percent cover in every scenario and fails at 25 percent; and replayed against the prices and yields of 2015 to 2024, the capped 25 percent plan holds its floor in two years of ten. Prices are forecasts from the FAOSTAT farm gate series (FAO, 2025); costs stand on an official wheat budget for 2024/25 and a consumer price bridge for the remaining crops (Agricultural Research Center, 2025; World Bank, 2025). An independent verification of the foundation passed fifteen of sixteen checks; the single failure, a robust ordering check, is recorded in its verification file. Version 7 changes none of this. It asks what the foundation cannot: given that farmers choose where to sell, what does the price announcement itself buy?

## 4. The delivery response

**The record.** Eight seasons of public record, assembled from USDA FAS Cairo reporting, FAO GIEWS briefs, ministry announcements and Reuters, give for each season the announced price, the tonnage the state bought, national production, and the delivered share.

| Season | Price, pounds per ardeb | Bought, million tonnes | Production, million tonnes | Share delivered |
| --- | --- | --- | --- | --- |
| 2019 | 685 | 3.27 | 8.77 | 0.373 |
| 2020 | 700 | 3.50 | 8.90 | 0.393 |
| 2021 | 725 | 3.60 | 9.00 | 0.400 |
| 2022 | 885 | 4.20 | 9.50 | 0.442 |
| 2023 | 1500 | 3.80 | 8.87 | 0.428 |
| 2024 | 2000 | 3.60 | 9.20 | 0.391 |
| 2025 | 2200 | 4.00 | 9.30 | 0.430 |
| 2026 | 2500 | 4.90 | 10.20 | 0.480 |

**The variable.** The price variable is a ratio: the procurement price per tonne divided by the farm gate price of wheat per tonne in the same season, both from the FAOSTAT producer price family (FAO, 2025). The ratio is the right shape for the farmer decision, because the state price competes with the price the trader offers for the same tonne. Two warnings travel with it. In 2022 and 2023 the published farm gate price equals the procurement price exactly, so the ratio reads 1.000 in those years by construction of the sources rather than by market observation: the official series is partly administered. And part of the 2022 share was required by the delivery decree, not chosen at the price. The fit that follows is a summary of how share and ratio moved together in a short, policy heavy record. It is not a clean market experiment, and this paper does not present it as one.

**The fit.** Ordinary least squares of share on ratio, on the six seasons with a published farm gate price, gives share equals 0.2611 plus 0.1682 times ratio. The slope carries a standard error of 0.0331, the residual standard deviation is 0.0105 of share, and the line accounts for 0.866 of the variance of the six shares. In words: when the state price rises from equal to the farm gate price to ten percent above it, the fitted share rises by about 1.7 points. Refitted without 2022, the season with the legal requirement, the slope falls by about a fifth, to 0.1384. The 2022 season stays in the headline fit because the requirement bound only a minimum per feddan and the season still carries price information, but the refit is reported and the difference is part of the uncertainty the curves below carry.

**Validation, and the three curves.** No farm gate price is published for 2025 or 2026, so those seasons cannot be fit points. Used as checks, with the alternative price set to the project forecast of 17,892 pounds per tonne, the line underpredicts both: for 2025 it gives 0.399 against an actual 0.430, and for 2026 it gives 0.418 against an actual 0.480. The misses run in one direction and they are informative. The response of the two recent seasons ran stronger than the earlier record, and the public record says why in part: planted area rose to a record of about 3.7 million feddans in 2026, payment within 48 hours was publicised, and the price was announced before sowing and raised again in April 2026. A fit that holds production fixed cannot see the planting half of the response. Version 7 handles this in three stated ways. The headline grid holds production fixed and says so. Three curves are carried through every result: a low curve, the fit with its slope reduced by one standard error; the central curve above; and a high curve fitted on all eight seasons, resting on a constructed alternative price for the last two seasons and labelled as such. And the Monte Carlo of Section 6 varies production across its historical range on top of the curves.

## 5. The price grid and the financial layer

**The financial layer.** At each candidate price the programme cost has three parts. The bill is the price times the tonnes delivered. The gap is the announced delivery target of 5.0 million tonnes less the tonnes delivered, imported at a world price scenario: 265, 313 or 400 dollars per tonne cost and freight, each anchored on a named dated observation, the central value being the S&P Global price for wheat delivered to Egypt on 8 October 2026 (S&P Global, 2026), converted at 54.47, 55.25 or 57.00 pounds per dollar (Central Bank of Egypt, 2026; Reuters, 2026). Gap orders are priced at the arrival quarter scenario, carrying a stated shipping lag of 75 days. The carrying cost is charged on delivered local tonnes: financing on the bill at treasury bill yields of 0.23956 to 0.2635, central 0.25, over a holding period of three, five or seven months, plus storage at 40, 60 or 90 pounds per tonne per month. The holding period and the storage cost are labelled assumptions; no public source prices either. The total counts these three parts only. It excludes the baseline import programme for the rest of consumption, about 10.4 million tonnes on the basis used here, which does not change across the grid, and the bread subsidy system downstream of the stock.

**The grid.** Central curve, production basis of 10.2 million tonnes, the FAO record 2026 harvest carried as the coming season planning basis because no 2027 forecast exists (FAO, 2026). Cover is delivered tonnes divided by consumption of 20.6 million tonnes. Rows at 2,800 pounds and above carry a price ratio above 1.000 and extend the fitted line beyond its observed range of 0.654 to 1.000; they are extrapolations and are marked as such wherever the grid is quoted in the project record.

| Price per ardeb | Share, central | Delivered, million tonnes | Cover, percent | Months of stock | Total programme cost, billion pounds | Step cost per extra tonne, pounds |
| --- | --- | --- | --- | --- | --- | --- |
| 2200 | 0.399 | 4.070 | 19.76 | 2.37 | 83.2 | first row |
| 2350 | 0.408 | 4.165 | 20.22 | 2.43 | 87.7 | 47,156 |
| 2500 | 0.418 | 4.261 | 20.69 | 2.48 | 92.5 | 49,364 |
| 2650 | 0.427 | 4.357 | 21.15 | 2.54 | 97.4 | 51,572 |
| 2800 | 0.437 | 4.453 | 21.62 | 2.59 | 102.6 | 53,781 |
| 3000 | 0.449 | 4.581 | 22.24 | 2.67 | 109.8 | 56,357 |
| 3250 | 0.465 | 4.741 | 23.01 | 2.76 | 119.3 | 59,670 |
| 3500 | 0.481 | 4.901 | 23.79 | 2.85 | 129.4 | 63,350 |

At the announced price of 2,650 pounds, the bill is 77.0 billion pounds, the gap of 642,721 tonnes costs 11.1 billion to import at the central world price, carrying costs 9.3 billion, and the total is 97.4 billion. The step column carries the grid its sharpest lesson. Each extra tonne a higher price attracts costs 47,156 to 63,350 pounds, roughly three times the procurement price itself, because the higher price is paid on every tonne delivered, not only on the extra tonnes, and the import saving on the shrinking gap offsets only a small part. Moving from 2,650 to the bottom of the demand range at 3,000 buys 223,792 extra tonnes for 12.4 billion extra pounds, an average of 55,254 pounds per extra tonne. And the top of the demand range still does not close the target on the central curve: at 3,500 the state buys 4.901 million tonnes, 99,226 tonnes short, at a total of 129.4 billion. On the high curve the same price delivers 5.159 million tonnes and passes the target. The target question is therefore a question about which response curve the recent record supports, and the recent record runs above the central line.

**The planting side.** The grid also re reads the cropping model at each price. Wheat in the model earns a blended price: the delivered share at the state price, the rest at the farm gate price. Asked when margin alone would plant wheat in the Delta, with no floor and no pattern imposed, the model answers at a state price of about 3,060 pounds per ardeb, inside the demand range. Below that point every hectare of wheat in the model stands on the observed pattern and on motives outside margin. Above it the price begins to plant wheat by itself, slowly: even at 3,500 the free plan plants 116,250 hectares against the pattern area of about 672,606 hectares, because potatoes and berseem still take the land and water first. The cost of holding pattern production falls as the price rises, from 30.2 billion pounds at 2,200 to 13.1 billion at 3,500. A higher state price is therefore also a cheaper guarantee: the same production promise costs the farm economy less to keep when wheat is worth more at the collection point.

## 6. Robustness

**Monte Carlo.** Two thousand draws per price combine the three response curves at weights of 0.25, 0.50 and 0.25, a production multiplier drawn from whole years of the 2015 to 2024 record, an alternative price drawn from the three foundation price layers, and a world price scenario drawn from the three scenarios.

| Price per ardeb | Mean delivered, million tonnes | Draws reaching the target, percent | Mean total cost, billion pounds | Worst quarter mean total, billion pounds |
| --- | --- | --- | --- | --- |
| 2200 | 4.089 | 0.0 | 83.7 | 87.5 |
| 2350 | 4.182 | 0.0 | 88.3 | 91.8 |
| 2500 | 4.276 | 0.0 | 92.9 | 96.0 |
| 2650 | 4.372 | 0.0 | 97.9 | 100.5 |
| 2800 | 4.463 | 0.6 | 102.9 | 105.2 |
| 3000 | 4.583 | 6.4 | 110.1 | 112.3 |
| 3250 | 4.753 | 19.6 | 120.1 | 124.0 |
| 3500 | 4.910 | 44.5 | 131.1 | 138.1 |

The target reading is the hard one. At the announced price, no draw in 2,000 reaches 5.0 million tonnes. Only at 3,500 does reaching the target become a realistic prospect, at 44.5 percent of draws, and the worst quarter mean cost there is 138.1 billion pounds against a central case total of 129.4 billion. A second reading, the share of draws reaching the promised cover at each price, sits near one half at every price by construction, because the promise is the central case and the draws are centred near it; it is reported in the project record for completeness and is not a confidence level.

**Break even against berseem.** The public argument assumes farmers deliver more when wheat beats berseem, its winter rival, on margin. On the model basis berseem earns a margin of 129,327 pounds per hectare, so wheat must earn revenue of 211,394 pounds per hectare to match it. The break even state price, at the blended value where only the delivered share earns the state price, runs from 5,412 pounds per ardeb in Sharkia to 6,261 in Kafr El Sheikh. At full delivery, the most favourable case for wheat, it runs from 4,321 to 5,022. No price in the grid and no price in the demand range makes wheat beat berseem on margin in any governorate. The caveats are part of the result: the berseem price is a constructed feed value of 0.125 times the maize price, not a market price; berseem in the Delta feeds the farmer own animals, so its margin is largely avoided feed cost rather than cash; wheat straw and household flour carry value the model does not price; and berseem area cannot grow past livestock demand, which the model cap reflects. The honest reading is that the delivery response is not a berseem margin story. Farmers deliver more at a higher price through payment speed, obligation, input access and the state price anchoring the trader price, channels the fitted share summarises and the margin comparison cannot see. That is why this paper fits the response to the record instead of deriving it from margins.

**Sensitivity.** Each new input moved between its low and high values at the announced price, all else central, ranked by the swing in total programme cost: the holding period, a labelled assumption, swings the total by 7.5 billion pounds; the world price by 4.8 billion; the production basis by 1.8 billion, with deliveries swinging by 712,817 tonnes; storage cost by 1.1 billion; the financing rate by 0.8 billion; the response curve by 0.5 billion, with deliveries swinging by 204,831 tonnes; and the exchange rate by 0.5 billion. The ranking carries a warning. At the announced price the total is more sensitive to an assumption with no public source than to any measured input, and more sensitive to the world price than to the delivery response itself, because extra local tonnes replace import tonnes at similar money. Anyone quoting the total at 2,650 should quote the holding period assumption beside it. This paper does.

## 7. Verification

An independent check routine, written separately from the build, recomputed the headline numbers by paths the build did not use. The response fit was recomputed by a second method and matches to the printed digits, as does its R squared. Grid arithmetic at three prices recomputes from the saved inputs. The two announced price cropping plans were rebuilt and replayed under HiGHS, a different solver from the CBC used in the build: the free plan margin agrees to within about 600 pounds on 221.7 billion, and the floor plan to within about 800 pounds on 197.0 billion. The Monte Carlo shares at the announced price recompute from the saved samples, including the worst quarter mean total of 100.5 billion pounds exactly. One break even price was recomputed directly from the parameters. Thirteen of thirteen checks pass. One passes weakly and is recorded as such: the check that the saved floor plan respects the rice decree passes with the whole bound to spare, because the optimised plans plant no rice at all. At the model prices rice earns the least per unit of water among the summer crops, so margin seeking plans drop it; the decree binds the observed pattern, which plants 447,153 hectares against a bound of 451,164 hectares, and does not bind these plans. The check is therefore a weak test for version 7, and the verification file says so in those words. The check verifies arithmetic, solver agreement and internal consistency. It does not verify the delivery response against the world, and it does not price the labelled assumptions.

## 8. Limitations

Five limits govern every figure in this paper. First, the behavioural layer rests on six fit seasons from a policy heavy record, in a market where the state is both price setter and largest buyer, one season carried a legal delivery requirement, and the alternative price series is partly administered. The fitted slope is a planning input with wide honest uncertainty, not a measured elasticity of a free market. Second, the headline grid holds production fixed at 10.2 million tonnes, while the two validation seasons suggest production itself answers the price through planted area; the grid is therefore conservative on deliveries in a way the paper can state but cannot yet correct. Third, every grid row at 2,800 pounds and above extrapolates the response beyond its observed ratio range. The demand range lives in the extrapolated region, which is uncomfortable and is stated rather than smoothed over. Fourth, two financial inputs, the holding period and the storage cost, are labelled assumptions with no public source, and the first of them is the largest single sensitivity of the headline total. Fifth, version 7 inherits the limits of its foundation: district water split by land share from a built anchor, price and yield layers with weak measured coverage, recourse that sees the full scenario so that plan margins are lower bound readings, and a berseem price that is a constructed feed value with no market or foreign cross check. What would move this study from exploratory toward empirical is named plainly: delivery records by governorate and week, which the state payment system plausibly holds; measured district water by source; a market observed alternative price series; and specialist review of the agronomy. The paper is offered for that review.

## References

Agricultural Research Center. (2025). *Wheat cost of production budget, 2024/25* [As held in the project workbook Egypt_Pakistan_Farm_Costs.xlsx].

Al Hayah News. (2026, October 27). [Minister of Supply remarks to the Senate on stock disclosure and silo capacity].

Central Bank of Egypt. (2026). *Treasury bill auction results and official exchange rates, August to November 2026*.

Diallo, M. (2026). *Pricing the wheat guarantee in the Nile Delta: A stochastic allocation study in wheat cover units* [Companion study, version 6].

Erem Business. (2026, October 31). [Parliament cost estimate for the wheat season and briefing requests on the procurement price].

Filcatalog. (2026). *Egypt wheat price tracker* [Updated 17 November 2026].

Food and Agriculture Organization of the United Nations. (2025). *FAOSTAT: Crops and livestock products; producer prices* [December 2025 vintage].

Food and Agriculture Organization of the United Nations. (2026). *GIEWS country brief: Egypt* [Briefs to June 2026].

Gohar, A. A., Cashman, A., & El bardisy, A. (2021). [Egypt water allocation model; as reviewed in the project prior work file].

Ministry of Agriculture and Land Reclamation, Economic Affairs Sector. (2022). *Bulletin of cost statistics and net return*.

Ministry of Agriculture and Land Reclamation, Economic Affairs Sector. (2025). *Agricultural statistics bulletin, Part 1: Winter crops 2024 to 2025*.

Newsroom.info. (2026, October 25). [Prime Minister announcement of the 2,650 pound procurement price].

Organisation for Economic Co operation and Development. (2026). *Agricultural policy monitoring and evaluation 2026*.

Reuters. (2024, August 19). [Report on the August 2024 GASC tender and trader comment on payment terms].

Reuters. (2026, June 11; October 24). [Reports on the 5.0 million tonne delivery target and on the price announcement at 55.25 pounds per dollar].

S&P Global. (2026, October 8). [Wheat price delivered to Egypt, as reported in the Black Sea ports report of 15 October 2026].

Safha News. (2026, October 26). [Parliament warnings on wheat area, trader sales and imports at the announced price].

U.S. Department of Agriculture, Foreign Agricultural Service. (2020). *Grain and feed annual: Egypt* (Report EG2020-0005).

U.S. Department of Agriculture, Foreign Agricultural Service. (2021). *Grain and feed update: Egypt* (Report EG2021-0020).

U.S. Department of Agriculture, Foreign Agricultural Service. (2022). *Grain and feed annual: Egypt* (Report EG2022-0009); *Grain and feed update: Egypt* (4 October 2022).

U.S. Department of Agriculture, Foreign Agricultural Service. (2023). *Grain and feed update: Egypt* (Report EG2023-0025).

U.S. Department of Agriculture, Foreign Agricultural Service. (2025). *Grain and feed annual: Egypt* (Report EG2025-0009).

U.S. Department of Agriculture, Foreign Agricultural Service. (2026). *Grain and feed update: Egypt* (Report EG2026-0013).

World Bank. (2025). *World development indicators: Consumer price index, Egypt* [As held in the project workbook Egypt_Pakistan_Farm_Costs.xlsx].
