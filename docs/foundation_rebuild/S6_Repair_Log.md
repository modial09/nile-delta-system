# S6 Repair Log: Version 6 of the Nile Delta Model

Date: 16 November 2026
Code: src/allocation_model_v6.py, src/methods_v6.py, src/user_template_v6.py, src/check_v6.py
Run records: data/processed/run_v6_main.txt, run_v6_caps.txt, run_v6_scaled.txt, run_v6_dro.txt, run_v6_reservealt.txt, run_v6_usersupply.txt, run_v6_mc.txt, run_v6_backtest.txt, run_v6_breakeven.txt
Results: data/processed/results_v6_main.json, results_v6_caps.json, results_v6_scaled.json, results_v6_dro.json, results_v6_reservealt.json, results_v6_usersupply.json, results_v6_methods.json
Version 5 files were not modified. This log is the exact figure record. The memo and the paper round money to billions with one decimal; this log does not round.

## 1. What changed, repair by repair

**Repair 1. The floor is restated in wheat cover.** The version 5 floor bound the mixed tonnage of wheat, unmilled paddy rice and summer maize against a reference of 12,254,401 tonnes. Version 6 retires that unit as the headline. The floor now binds on wheat tonnage alone. Each level is a share of national wheat consumption of 20,600,000 tonnes (USDA Foreign Agricultural Service, Grain and Feed Update EG2026-0013, 28 September 2026, marketing year 2025/26). Months of stock is the same quantity in a second unit: wheat tonnage divided by one twelfth of consumption, so 25 percent cover is 3.00 months. The mixed tonnage is still tracked in the run output and is no longer the promise.

**Repair 2. Water keeps the built anchor, and district supply becomes a user input.** The total stays at the calibration anchor of 11.00 billion cubic metres, which no source publishes, split across the eight governorates by physical land share. Every document narrates it as a built anchor. The ladders are also solved at anchor scales of 0.90 and 0.80. District supply is now also a working input, not only a design note: see Repair 8.

**Repair 3. Scenarios are rebuilt on how the river is run now.** A water state is a starting Lake Nasser storage state (low, normal, high) crossed with an inflow year type (dry, normal, high), giving nine water states and, with the three price and yield layers, 27 scenarios. The budget follows one stated release rule: the release factor equals the inflow ratio of the year type plus a storage adjustment (low storage minus 0.04, normal plus 0.02, high plus 0.10), bounded between 0.70 and 1.05 of the anchor. Inflow ratios are dry 0.7807, normal 0.9547 and high 1.2213, taken from the gauged Aswan record of 1871 to 1970. That record now supplies only the definitions of the year types. Its frequencies are retired as probability weights. Scenario weights are stated planning weights: storage in equal thirds, inflow dry 0.30, normal 0.45, high 0.25, layers 0.25, 0.50, 0.25. Multi year dry sequences are priced as named stresses in the scaled run: a second dry year at the budget of the low storage and dry inflow state, and a third dry year at the release rule floor of 0.70 of the anchor.

**Repair 4. Rice is bounded by the state decree.** Total planted rice area in every water state is bounded by 451,164 hectares: Ministerial Resolution No. 543 of the Ministry of Water Resources and Irrigation, designating 1,074,200 feddans across nine governorates, as reported in USDA Grain and Feed Annual EG2024-0010 (23 April 2024) and confirmed unchanged for 2025/26 by the OECD Agricultural Policy Monitoring and Evaluation 2026. The decree covers nine governorates and the model covers eight of them; the bound is applied to the study area as published, and that difference is named here rather than adjusted silently. The observed baseline rice area of the study area is 447,153 hectares, inside the bound.

**Repair 5. Berseem is a real winter crop.** Berseem now competes with wheat inside the winter pool. National area 1,253,666 feddans for 2024 to 2025, fresh yield 28.637 tonnes per feddan, cost 9,792 pounds per feddan including rent for 2021 to 2022 (Ministry of Agriculture and Land Reclamation, Economic Affairs Sector bulletins, as assembled in docs/foundation_rebuild/Pakistan_Comparison_Expanded.md and filed in data/external/v6_berseem_parameters.csv). The study area total is a stated construction: the national area times the Delta share of 0.6824 from CAPMAS figures for 2021, giving 359,311 hectares, split across governorates by physical land share. Its yield is 68.183 tonnes per hectare fresh in every district and layer. Its water duty is 6,971 cubic metres per hectare. Its price is a stated feed value construction, 0.125 times the maize price of the same layer, from standard feed table values for total digestible nutrients. It is not a measured market price, because no official berseem price series could be found; see the unverified list.

**Repair 6. Costs stand on one year, 2025, on a sourced bridge.** Wheat carries the Agricultural Research Center budget for 2024/25: 34,468 pounds per feddan including rent, which is 82,066.67 pounds per hectare (workbook Egypt_Pakistan_Farm_Costs.xlsx, user supplied 16 November 2026; the 2023/24 figure of 29,834 pounds per feddan is filed in data/external/v6_facts.csv). Every other crop carries its official 2022 cost moved to 2025 by the Egypt consumer price path in the same workbook: index 119.834237 in 2022 to 234.759958 in 2025, a factor of 1.959093. The guessed multipliers of version 5 (1.50 and 2.00) are retired as the primary bridge. A single labelled sensitivity at all costs times 1.25 is run in their place, as a bracket for farm costs outrunning consumer prices.

**Repair 7. Four methods are added.** Distributionally robust optimisation over an ambiguity set of twelve weight vectors (the nominal weights plus stated tilts of 1.5, renormalised). Conditional value at risk of the margin at the worst 25 percent tail, printed beside every frontier rung. Monte Carlo testing of the capped plan at the headline rung on 200 whole year draws from 2015 to 2024, seed 20261116, plus a backtest of the same plan and of the historical pattern on the ten actual years in order. Break even sensitivity at the headline rung, perturbing eight inputs one at a time, with a break even search on the strongest input. Method designs are stated in the docstring of src/methods_v6.py.

**Repair 8. Decision maker data input is a working feature.** A blank template ships at data/external/decision_maker_input_template.csv: 42 rows covering district water supply by source (canal, drainage reuse, groundwater, in billion cubic metres for the reference water state), crop costs in pounds per hectare, and crop expected prices in pounds per tonne, each row labelled in plain English with its unit and its public default. The reader sits in src/user_template_v6.py at the data loading edge only. It is called from one place inside load_all in src/allocation_model_v6.py. No solver code and no model structure were changed for this feature. Rules: a missing file changes nothing; a blank cell keeps its public default; a filled cell replaces only its named input; a filled crop price replaces the expected price and moves the low and high bands by the same ratio; for water, if one or two source cells of a district are filled, the blank sources are covered by one public default balance that is not assigned to a source, because no public source split is held. Every run log prints the provenance of every template cell, user or default, in the header block. Two proofs are in the verification record: with the blank template present, budgets, costs and prices are identical to a run with no template at all; with one filled cell (wheat cost set to 99,999 pounds per hectare), only the wheat cost changed. The older water only demonstration mode (usersupply) still runs: moving Damietta 20 percent up and Kafr El Sheikh 20 percent down leaves the capped ceiling unchanged, raises the unconstrained capped margin by 231,243,887 pounds, and lowers the margin at 20 percent cover by 120,956,256 pounds.

**Pakistan enters in two places only.** A short mirror section in the memo, and an assumptions cross check table in the memo that uses matched Pakistan values to bound Egypt assumptions where Egypt data is missing. Pakistan numbers never replace Egypt data anywhere in the model. The source note is docs/foundation_rebuild/Pakistan_Comparison_Expanded.md.

**One reporting repair found during the build.** In the first version 6 main run, the wheat procurement variant and the cost sensitivity printed margins valued at the default prices and costs, because the reporting routine read the default parameter set while the solver used the overrides. The plans were correct; the printed margins were valued on the wrong basis. The frontier routine now folds any price or cost override into the parameter copy used for both the solve and the report. The primary ladders carry no overrides and are unchanged by this repair: the relaxed unconstrained margin is 397,309,284,899 pounds in both runs. The variant figures below are from the corrected run.

## 2. The new ladders in wheat cover units

### 2.1 Capped ladder, the headline list. Anchor 11.00 billion cubic metres.

Unconstrained expected margin under caps: 221,699,177,650 pounds.

| Cover | Months of stock | Floor in wheat tonnes | Expected margin, pounds | Cost against the capped optimum, pounds | Step cost from the rung below, pounds | CVaR margin, pounds | CVaR cost, pounds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 percent | 0.00 | 0 | 221,699,177,650 | 0 | 0 | 195,645,625,198 | 0 |
| 15 percent | 1.80 | 3,090,000 | 210,189,613,497 | 11,509,564,153 | 11,509,564,153 | 182,176,392,550 | 13,469,232,648 |
| 20 percent | 2.40 | 4,120,000 | 202,170,306,859 | 19,528,870,791 | 8,019,306,638 | 173,561,296,458 | 22,084,328,740 |
| 25 percent | 3.00 | 5,150,000 | 192,795,390,204 | 28,903,787,446 | 9,374,916,655 | 164,187,153,199 | 31,458,471,998 |
| 30 percent | 3.60 | 6,180,000 | infeasible | | | | |
| 35 percent | 4.20 | 7,210,000 | infeasible | | | | |

Capped ceiling: 5,733,795 tonnes of wheat held in every scenario, a cover of 27.83 percent, 3.34 months of stock. The top feasible rung is 25 percent.

### 2.2 Relaxed ladder, the benchmark list. Anchor 11.00 billion cubic metres.

Unconstrained expected margin without caps: 397,309,284,899 pounds.

| Cover | Months of stock | Expected margin, pounds | Cost against the relaxed optimum, pounds | Step cost from the rung below, pounds | CVaR cost, pounds |
| --- | --- | --- | --- | --- | --- |
| 0 percent | 0.00 | 397,309,284,899 | 0 | 0 | 0 |
| 15 percent | 1.80 | 362,740,984,449 | 34,568,300,450 | 34,568,300,450 | 34,658,967,234 |
| 20 percent | 2.40 | 341,376,481,677 | 55,932,803,222 | 21,364,502,772 | 57,863,164,882 |
| 25 percent | 3.00 | 314,180,390,805 | 83,128,894,093 | 27,196,090,871 | 84,583,315,339 |
| 30 percent | 3.60 | 280,920,067,074 | 116,389,217,825 | 33,260,323,732 | 117,330,430,316 |
| 35 percent | 4.20 | 247,611,924,044 | 149,697,360,855 | 33,308,143,030 | 150,116,071,402 |

Relaxed ceiling: 8,674,565 tonnes, a cover of 42.11 percent, 5.05 months. The relaxed optima plant potatoes at up to 22 times their observed areas at fixed prices; the market absorption warnings are printed in the run log and travel with this list wherever it is quoted.

### 2.3 Both ladders at the scaled anchors

Capped, anchor scale 0.90 (9.90 billion cubic metres): unconstrained margin 208,108,355,810 pounds; cost at 15 percent 13,410,394,838; at 20 percent 21,688,618,172; at 25 percent 31,059,363,057. Capped ceiling unchanged at 27.83 percent.
Capped, anchor scale 0.80 (8.80 billion cubic metres): unconstrained margin 194,262,422,974 pounds; cost at 15 percent 16,792,697,723; at 20 percent 25,277,509,862; at 25 percent 34,495,649,196. Capped ceiling unchanged at 27.83 percent.
Relaxed, anchor scale 0.90: unconstrained margin 364,825,162,924 pounds; cost at 15 percent 36,020,681,659; at 20 percent 59,310,805,949; at 25 percent 86,820,058,567. Relaxed ceiling 41.60 percent.
Relaxed, anchor scale 0.80: unconstrained margin 332,341,036,279 pounds; cost at 15 percent 38,137,056,723; at 20 percent 62,688,809,691; at 25 percent 91,363,282,801. Relaxed ceiling 40.15 percent.

The capped ceiling does not move when the anchor is scaled, and the dry sequence stresses barely move the relaxed capacity either: a second dry year at the low storage and dry inflow budget leaves maximum wheat capacity at 8,674,565 tonnes (42.11 percent), and a third dry year at the release rule floor of 0.70 gives 8,630,852 tonnes (41.90 percent). The reason is structural and is stated wherever the ceiling is quoted: at the ceiling the binding limits are land and the planting caps, because a kept crop may run at 0.30 of its full water duty with a linear yield penalty. Water binds on the price of each rung, not on the ceiling.

### 2.4 The historical pattern on the new basis

Pattern wheat on the published basis: 4,617,795 tonnes, a cover of 22.42 percent, 2.69 months of stock. Imposed on the fixed pattern, worst scenario wheat capacity is 4,610,705 tonnes, a cover of 22.38 percent. The pattern therefore holds the 15 percent and the 20 percent cover levels in every scenario and fails at 25 percent. Under margin seeking recourse the pattern delivers an expected margin of 75,285,656,060 pounds, expected wheat of 4,295,095 tonnes, and minimum scenario wheat of 3,584,687 tonnes, a cover of 17.40 percent. The gap between capacity and delivery is the same distinction version 5 established: the pattern can hold 20 percent, and left to profit it delivers less.

### 2.5 Variants on the relaxed ladder

Wheat at the documented procurement price of 14,666.67 pounds per tonne in every layer (2025 harvest): the planting plan at each tested level is unchanged, and the guarantee cost rises because the wheat the floor forces is worth less. Cost at 20 percent cover: 70,143,699,400 pounds. Cost at 25 percent: 100,892,514,192 pounds.
All costs at 1.25 times the consumer price bridge: unconstrained margin 318,071,419,263 pounds; margin at 20 percent cover 269,067,420,756 pounds; cost at 20 percent cover 49,003,998,507 pounds.

## 3. Method results

**Distributionally robust optimisation.** Ambiguity set of twelve weight vectors, capped world. At 15 percent cover the robust plan buys a worst case gain of 25,786,944 pounds for an expected cost of 29,237,248 pounds. At 20 and 25 percent cover the robust plan replays to a worst case marginally below the nominal plan (by 20,451,044 and by 22,570,889 pounds), at an expected cost of 37,213,024 and 38,316,508 pounds. One line: because the floor is hard in every scenario, scenario weights move the price very little, and weight robustness on this set costs almost nothing and buys almost nothing. The verification check on the robust ordering failed; see section 5.

**Conditional value at risk.** At the capped headline rung of 25 percent cover, the expected cost of the guarantee is 28,903,787,446 pounds and the cost measured on the worst 25 percent tail of scenarios is 31,458,471,998 pounds. Pricing the promise on the bad tail instead of on the average year adds 2,554,684,552 pounds at this rung. CVaR figures for every rung are in the tables of section 2.

**Monte Carlo.** The capped plan at 25 percent cover, replayed on 200 whole years drawn with replacement from 2015 to 2024 with water at the reference state, holds its floor of 5,150,000 tonnes in 18.5 percent of draws. Median wheat capacity across draws is 4,992,727 tonnes, a cover of 24.24 percent; the 10th percentile is 4,739,066 tonnes and the 90th percentile is 5,157,919 tonnes. Delivered margin across draws: 10th percentile 131,385,791,816 pounds, median 190,805,012,412 pounds, 90th percentile 325,144,891,771 pounds. The delivery reading matched the capacity reading in every drawn year.

**Backtest.** On the ten actual years in order, the same plan holds the 25 percent floor in two years, 2017 and 2021. Its capacity by year runs from 4,739,066 tonnes in 2018 to 5,164,846 tonnes in 2017. The historical pattern holds the 25 percent level in none of the ten years; its capacity runs from 4,242,804 tonnes in 2018 to 4,623,997 tonnes in 2017. The guarantee the model prices is therefore a promise about the constructed scenario set, and history is less kind to it than the scenario set is. This is stated in the memo and in the paper, not only here.

**Break even sensitivity.** At the capped headline rung of 25 percent cover, base guarantee cost 28,903,787,446 pounds, one input at a time, minus and plus 10 percent: wheat yield moves the cost to 44,986,210,453 and to 16,408,491,496, a largest swing of 16,082,423,008 pounds, 55.6 percent of the base cost. Wheat price: 38,299,382,022 and 19,940,133,657, swing 9,395,594,576. Wheat cost: 22,779,172,576 and 35,066,049,187, swing 6,162,261,741. Maize price swing 4,488,364,498. Berseem price swing 4,038,708,039. Potato prices swing 3,328,417,410. Water anchor: 31,059,363,057 and 27,781,064,710, swing 2,155,575,611. Rice price swing 0: the capped headline plan plants no rice, so a 10 percent rice price move does not touch the guarantee cost at this rung. Break even search on wheat yield: a yield multiplier of about 1.114, that is yields about 11.4 percent above the published basis, halves the guarantee cost; at a multiplier of 2.0 the cost is zero because the free plan then plants enough wheat by itself.

**Reserve split.** Printed in full, as the clarity assessment required. Capped ceiling under the primary proportional reserve split: 27.83 percent. Under the winter first split: 27.83 percent. At 20 percent cover, margin under the primary split is 202,170,306,859 pounds and under the winter first split 201,989,069,680 pounds, a difference of 181,237,179 pounds. The reserve construction choice moves the price at this rung by about 0.2 billion pounds and does not move the ceiling.

## 4. Every place a needed datum could not be verified

1. District water supply by source. No public source gives canal, reuse and groundwater supply by Delta governorate. The model therefore keeps the built split by land share as its default and accepts district supply from the user through the template. This is the largest open gap in the project and it is structural, not a search failure.
2. The exact current rice decree. The most recent verified figure is Ministerial Resolution No. 543 as reported on 23 April 2024 and confirmed for 2025/26 by the OECD in 2026. No newer decree text was verified. If a newer decree exists, the bound should be replaced.
3. A measured berseem price. No official berseem price series was found in the searches of 16 November 2026. The model uses a stated feed value construction at 0.125 times the maize price. The break even run bounds the risk: a 10 percent move in the berseem price moves the headline guarantee cost by about 4.0 billion pounds.
4. Berseem yield response to water. No sourced response factor is held. The model sets the factor to 1.00 as a stated assumption, equal to the sugar beet value carried from version 5.
5. District berseem areas. No district level berseem area is published in the sources held. The study area total is built from the national area and the 2021 Delta share, and the district split follows land share. Both steps are constructions.
6. Winter potato cost. No winter potato cost table exists in the ministry bulletin. Winter potatoes carry the summer potato cost, as in version 5, now bridged to 2025. This remains a named gap with a large cost attached (169,764.73 pounds per hectare), and potatoes dominate the relaxed optima, which is one more reason the relaxed list is a benchmark and not a headline.
7. Punjab comparison gaps, carried from the Pakistan note: no verifiable Punjab maize cost of production; no Punjab berseem figures at all, because Pakistan publishes fodder only as one combined category; Punjab cotton cost exists with no paired yield, so no cost per tonne; Egypt cost bulletins end at the 2022 editions, which is why the bridge of Repair 6 exists.
8. Scenario weights. The storage, inflow and layer weights are stated planning weights. No measurement can verify them, because the release rule makes future budgets a policy outcome rather than a frequency. The distributionally robust runs exist for this reason.
9. The price and yield layers. The layer bands are inherited from the version 5 forecasting run, whose measured band coverage was weak (0.0 to 22.2 percent against a 50 percent construction value). Version 6 does not rebuild the layers; it inherits the weakness and the memo states it.
10. Recourse information. Inside the model, water allocation and abandonment respond with the full scenario in view, including its yield layer. No real season sees that much. Printed guarantee costs are therefore lower bounds, and every document in this build says so.

## 5. Verification status

The independent check routine src/check_v6.py ran on 16 November 2026. Fifteen of sixteen checks pass, including HiGHS replays of the headline capped rung (192,795,391,421 pounds against the CBC figure of 192,795,390,204) and of the capped ceiling (27.83 percent under both solvers), the workbook bridges recomputed from the workbook itself, the release rule recomputed from the series, and the two template isolation checks. One check fails: the distributionally robust ordering check, because under a common replay the robust plan holds a marginally lower worst case than the nominal plan at cover of 20 and 25 percent. The failure is recorded in full in docs/foundation_rebuild/CheckV6_Independent_Verification.md. It is not softened there and it is not softened here: no dominance claim for the robust plan is made anywhere in this build.

## 6. The label

Version 6 remains a numerically verified exploratory model study on a stated basis. It is not validated empirical evidence about the Delta. The repairs close the four foundation points of the persona review in design and in computation: the promise is now denominated in wheat cover and months of stock; the water anchor is narrated as built and district supply is a working user input; the scenarios describe a managed river with storage, inflow year types and a stated release rule, with dry sequences priced as stresses; rice is bounded by the decree and berseem stands inside the model as a winter crop. What still blocks the empirical label is the unverified list of section 4, above all the absence of measured district water.
