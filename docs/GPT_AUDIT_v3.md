# Independent academic audit: Nile Delta water allocation project, version 3

14 November 2026 · Audit only; project files unchanged

**1. Verdict**

This is a master's-level optimization prototype with substantial work on data documentation, scenario analysis, and dual interpretation. It is not yet a defensible empirical working paper or journal-grade study. The reported gains mostly reproduce, but the high-beet plan exceeds physical winter land, the reported VSS uses the wrong average-water benchmark, and the feasibility conclusion is conditional on consequential modeling choices. Major revision is required before presenting the results as validated evidence for Delta allocation policy.

**2. Errors found, largest first**

**A. The annual land pool permits a physically impossible winter planting plan.**

The code lets wheat, sugar beet, rice, maize, and potatoes compete for each governorate's total annual cropped area. Annual cropped area counts the same physical field again when it carries a second crop. It therefore cannot, by itself, constrain land occupied in a particular season.

This is a demonstrated defect, not merely a theoretical objection. The beet2400 plan plants approximately **1.575 million hectares of wheat plus 0.321 million hectares of sugar beet: 1.896 million hectares of winter crops**. The package's cultivated-area series gives only **1.677 million physical hectares** across the eight governorates. Wheat and beet alone exceed that total by approximately **219,665 hectares, or 13.1%**, before any winter potatoes are counted. The plan exceeds physical cultivated area in seven governorates; unused land in Qalyubia cannot remedy another governorate's excess. Summing the positive district excesses gives approximately 220,737 hectares.

The beet795 plan has a smaller but still real violation: its approximately 47,804 hectares of wheat in Damietta exceed that governorate's 47,260 physical hectares before potatoes are considered.

Consequently, **EGP 147.994 billion and the associated 52.92% gain are results of an allocation that is not physically implementable under the package's own land figures**. The economic comparison cannot be defended as an implementable plan merely by labeling the annual land pool a modeling choice.

There is also an omitted opportunity cost. The five modeled crops occupy **1,793,438.64 crop-hectares** in the baseline, only **56.46%** of the **3,176,473.86 annual crop-hectares** made available to optimization. The optimized plans expand their combined area to approximately 2.072 million and 2.376 million crop-hectares. The model charges no loss of output or margin from the unmodeled crops that such expansion might replace. It therefore estimates returns to the five modeled activities, not a complete change in governorate farm income.

Evidence: `04_RERUN_CHOICES.md`, land and baseline sections; `05_MODEL_CODE_v3.py`, `build_problem`; planting tables in logs 06 and 07; `capmas_governorate_total_cropped_area.csv` and `capmas_governorate_area.csv`. Area totals above were independently calculated.

**B. The reported VSS figures do not use the expected-value problem.**

The probability-weighted water budget is:

`0.23 × 8.591 + 0.45 × 10.505 + 0.32 × 13.431 = 11.0011 BCM`.

The code instead calls `build_deterministic_model(par, "expected")`, using **10.505 BCM**, the middle scenario. That budget is approximately **4.51% below the actual mean**. A scenario named “expected” does not become the mathematical expectation because of its name.

Thus **EGP 613,178,863 and EGP 8,025,667,499** measure the advantage over the particular middle-scenario planning rule used in the code. They are not standard values of the stochastic solution relative to planning at the expected uncertain inputs.

This is consequential. In my independent reconstruction, planning at the actual 11.0011 BCM mean yields fixed planting plans whose maximum low-scenario staple outputs are approximately:

| Variant | Maximum low-scenario staples with the mean-water planting fixed | Required floor | Shortfall |
|---|---:|---:|---:|
| beet795 | 10,025,041 t | 10,344,276 t | 319,234 t |
| beet2400 | 10,064,474 t | 10,344,276 t | 279,802 t |

These shortfalls persist when low-scenario water is allocated specifically to maximize staples. They are not a consequence of choosing a profit-seeking recourse allocation. The actual expected-value plans are infeasible under the hard guarantee. A finite conventional VSS cannot simply be reported for them without specifying a penalty or other treatment of infeasibility.

I also checked whether a different, equally optimal mean-water plan could avoid this result. Requiring low-scenario feasibility reduces the best mean-scenario objective by approximately EGP 1.977 billion and EGP 0.934 billion, respectively. Thus this is not merely an unfortunate choice among tied mean-water optima in the reconstruction.

The EVPI computation is a different comparison and does not contain this particular error.

Evidence: code file 05, `information_values`, `build_deterministic_model`, and `build_problem`; scenario probabilities and budgets in logs 06 and 07. The new calculations reconstruct the supplied model independently; they do not repair its physical land problem.

**C. The internal audit confuses reproduction with validation of the formulation.**

The internal audit says the 95% infeasibility result is “not a formulation artefact” because a separate optimizer using the same constraints reproduces it. That reasoning is invalid. A second optimizer can reproduce a restrictive assumption perfectly.

I independently reconstructed the stated LP and checked its solutions against both primal constraints and dual optimality conditions. My maximum low-scenario staple production is approximately **10,763,190 tonnes**, or **93.64475%** of the modeled full-water baseline. This is about **141 tonnes below** the internal audit's **10,763,331 tonnes**. My value rounds to **93.64%**, rather than 93.65%. The small numerical disagreement does not affect either the 95% or 100% infeasibility verdict.

The crucial result is what changes when assumptions change:

| Independent diagnostic | Maximum staples | Share of the same modeled baseline |
|---|---:|---:|
| Stated primary model | 10,763,190 t | 93.64475% |
| Remove crop-specific area caps; keep annual land pools and district budgets | 10,978,704 t | 95.51982% |
| Pool district water budgets; keep crop caps and annual land pools | 10,786,332 t | 93.84610% |
| Use Derivation B low budget, 8.921 BCM | 11,026,758 t | 95.93791% |
| Substitute the foundation's alternative Lower Egypt wheat duty, 3,486 m³/ha, holding other requirements fixed | 12,843,545 t | 111.74480% |

These are controlled diagnostics, not alternative policy recommendations. In particular, the last row uses an older, differently sourced regional duty; it does not establish that this duty is preferable. It establishes how strongly the conclusion depends on a disputed input already present in the foundation.

The primary ceiling also has a direct arithmetic explanation. Wheat has the highest full-water staple output per cubic metre in every governorate. At the primary low budget, the capacity calculation plants wheat up to the 50% annual-area cap and uses the remaining water on maize. The annual land sum is slack. This calculation independently reproduces approximately 10,763,190 tonnes. The wheat cap is therefore part of what determines the ceiling.

For a further check, removing the crop caps while adding separate winter and summer physical-land limits still permits approximately **95.04%**, under an explicitly assumed equal seasonal split of potato area. That split is only a diagnostic assumption. The original cap-removal test alone already disproves the internal audit's assertion that formulation choices cannot account for the 95% verdict.

The correct finding is: **95% and 100% are infeasible under the stated primary budgets, crop caps, yield calibration, and land formulation.** It is not a finding that the Delta physically cannot protect 95% of staple output. Prices do not determine this technical capacity ceiling; water requirements, yields, resource limits, and crop caps do.

Evidence: code file 05 and foundation sections 5, 7, 8, 10, and 11. The 93.65% ceiling is stated in the internal audit; the version 3 results note reports the infeasibility statuses but does not itself print that ceiling.

**D. “Production floor at zero” conceals a minimum-irrigation restriction.**

The implemented production expression is:

`q = y[(1 − Ky)x + Ky·w/r]`, with the constraint `q ≥ 0`.

For a planted crop with `Ky > 1`, this forces irrigation of at least `(Ky − 1)/Ky` of its full requirement:

| Crop | Forced minimum irrigation share |
|---|---:|
| Wheat | 4.76% |
| Rice | 16.67% |
| Maize | 20.00% |
| Sugar beet | 0.00% |
| Potatoes | 9.09% |

That is not the same function as `q = max(0, y[(1 − Ky)x + Ky·w/r])`, which would allow a planted crop to receive no water and fail. In the implemented LP, rice must receive water even when its modeled harvest is zero. The code's statement that a zero coverage share means a written-off crop is therefore not a general description of crop failure for crops with `Ky > 1`.

This restriction matters particularly for the fixed historical baseline. Its aggregate minimum irrigation requirement is approximately **2.196 BCM**, including irrigation that can yield zero production at the threshold.

I independently evaluated the fixed baseline with an actual zero-output clipping rule, enumerating the possible surviving crop sets within each district and scenario. Expected baseline margin rises from approximately **EGP 95.108 billion to EGP 97.446 billion** for beet795 and from **EGP 96.780 billion to EGP 103.212 billion** for beet2400. Planting costs remain sunk in these comparisons.

These are baseline diagnostics, not corrected headline gains: the optimized model would also need to be reformulated and resolved under the same crop-failure rule. They demonstrate that the baseline and the gains depend on a consequential restriction that the phrase “floor at zero” does not explain.

Evidence: code file 05, `production_expr` and `ProdFloor` constraints; independent fixed-baseline calculations.

**E. The claimed “guarantee price list” is not yet a price list of the guarantee's cost.**

The primary table reports optimized margin, baseline margin, and their difference at 90%, followed by two infeasible rows. The difference from the historical planting pattern is not the economic cost of imposing a guarantee. That cost requires a comparison with the same optimized model without the guarantee, or differences between feasible guarantee levels.

As a check, my reconstruction gives unrestricted expected margins of approximately **EGP 167.143 billion and EGP 186.251 billion**. Relative to the corresponding 90% runs, imposing the floor costs approximately **EGP 26.632 billion and EGP 38.257 billion** within the current formulation. These are not policy-ready estimates because they inherit the model defects above. They show the missing comparison.

Derivation B does provide two feasible floor levels. Its printed margins imply that raising the floor from 90% to 95% costs **EGP 23,228,604,571** in that sensitivity. That is a genuine difference between floor levels, although the cost is not explicitly presented that way in the table.

The primary model needs several feasible floor levels below its ceiling and a consistent reference to produce the contribution it promises.

Evidence: code file 05, `guarantee_sweep`; logs 06 and 07; results note 08; positioning section C of file 03.

**F. The stress-run language confuses a profit-maximizing choice with unavoidable food loss.**

The floor is infeasible after 10% and 20% cuts under the stated primary formulation. That finding survives. But the subsequent unfloored runs maximize margin, not staple supply.

Under a 20% cut, beet2400 chooses **zero staple output**. My independent capacity calculation under the same reduced budgets and original constraints can still produce approximately **8,782,963 tonnes of staples**, or **76.42%** of the full-water baseline. At a 10% cut, the corresponding capacity is approximately **9,880,833 tonnes**, or **85.97%**.

Therefore “staple output falls to zero” must be presented as the choice of the unfloored profit objective. It is not an agricultural impossibility or a predicted collapse of actual food supply. The internal audit's phrase “the first cut is paid in food” is too broad without this distinction.

Evidence: `stress_runs` in code file 05; log 07; independent capacity calculations.

**G. The historical crop areas are observed; the baseline output and effective district yields are calibrated.**

The code does not directly use the published governorate yields as its effective yields. It divides each governorate yield by a regional crop mean and multiplies by the 2014–2023 national mean. This preserves relative patterns while changing yield levels.

Against the published district yields, the resulting scaling factors are approximately **0.95760 for wheat, 1.00181 for rice, 0.83879 for maize, 1.05705 for beet, and 0.98940 for potatoes**. Thus every district's modeled maize yield is about **16.12% below** its published 2020/2021 yield, and wheat is about **4.24% below**.

The baseline's **11,493,640 tonnes** are therefore modeled full-water staple output, not observed 2020/2021 output. The delivered production panel sums to approximately **12,254,656 tonnes** for the reported wheat, rice, and summer-maize cells; Menoufia rice is unreported in that year. Calling the floor 90% of “current output” without explaining the normalization is misleading. It is 90% of a constructed reference output attached to historical crop areas.

The quantity called a “production weighted mean yield” is actually total production divided by implied total area: an area-weighted aggregate yield, not a production-weighted arithmetic mean. The formula is usable; its label should be corrected.

Evidence: code file 05, `load_district_multipliers`, `load_crop_facts`, and `build_parameter_set`; governorate production and yield CSVs.

**H. The mixed economic years prevent a current-profit interpretation; disclosure does not solve comparability.**

The core combines 2023 producer prices, 2016/2017 nominal costs, 2020/2021 crop areas, and national yields averaged over 2014–2023. The beet2400 variant additionally substitutes a 2024/2025 procurement price. These are historical-input scenarios, not a coherent current-year farm budget.

The foundation itself supplies a later wheat cost of **EGP 40,476.19/ha for 2022/2023**, against the model's **EGP 21,473.81/ha**. That is approximately an 88.5% increase, well beyond the reported ±20% cost exercise. A uniform ±20% change cannot establish robustness to missing, crop-specific cost escalation.

The two beet runs are a useful price sensitivity, but their difference confounds price year and marketing basis. It cannot be attributed solely to the distinction between farm-gate and factory procurement concepts. Cleaning, quality, bonuses, delivery costs, eligibility, and timing would need alignment before treating either as the relevant farmer receipt.

These issues affect optimal planting, expected margin, relative gains, water duals, and information values. Ratios are not automatically reliable because their components carry source labels.

Evidence: foundation sections 1–4; cost and procurement CSVs; choices file 04.

**I. There are small arithmetic and documentary errors.**

The following replay uses the printed log components, with decimal arithmetic:

| Calculation at 90% floor | beet795 | beet2400 |
|---|---:|---:|
| Probability-weighted printed scenario margins | EGP 140,511,553,289.79 | EGP 147,993,830,741.38 |
| Printed optimized expected margin | EGP 140,511,553,290 | EGP 147,993,830,742 |
| Replay minus printed margin | −EGP 0.21 | −EGP 0.62 |
| Printed baseline expected margin | EGP 95,107,983,182 | EGP 96,779,569,341 |
| Gain by subtracting printed margins | EGP 45,403,570,108 | EGP 51,214,261,401 |
| Printed gain | EGP 45,403,570,107 | EGP 51,214,261,401 |
| Gain from printed margins / printed baseline | 47.73896847% | 52.91846383% |

Both headline percentages round correctly. The beet795 gain differs by EGP 1 when printed margins are subtracted. The beet2400 weighted scenario total rounds to EGP 147,993,830,741, not 742; independently rounded components can account for this tiny difference, but the internal audit's assertion that it rounds to 742 is false as written.

The printed beet795 scenario staple outputs average to **10,398,954.40 tonnes**, against **10,398,955 tonnes** printed. The difference is 0.60 tonnes; it is not exact agreement at whole-tonne precision. Likewise, the one-tonne-looking low-scenario floor discrepancy cannot be conclusively classified as pure printing rather than solver tolerance without unrounded outputs. It is immaterial in scale and does not threaten the 90% feasibility conclusion.

Subtracting printed information values produces **EGP 613,178,864 and EGP 8,025,667,500**, each EGP 1 above the printed VSS-style comparison. EVPI subtraction reproduces **EGP 18,394,620,407 and EGP 12,548,049,893** exactly.

The logs do not print baseline scenario margins. Therefore those expected margins cannot be reconstructed independently from log components alone. I reconstructed baseline water allocation from the supplied external panels and national yields inferred from the log's production-to-area ratios. This gives approximately **EGP 95,107,983,492 and EGP 96,779,569,752**, residuals of about **EGP 310 and EGP 411**. The residuals are tiny and compatible with printed-input precision and numerical tolerances; they do not justify claiming exact reproduction from original raw inputs.

The blanket opening sentence of results note 08, saying every figure appears in the version 3 logs, is false for the historical version 2 comparisons, as the internal audit already observes. Prior-work file 03 also describes 2009 as thirty years after 1994; the interval is fifteen years.

**3. Claims that survive exactly, within the stated model**

**The two-stage architecture is correctly recognizable.** Planting variables are shared across scenarios and water variables are scenario-specific. Planting costs are charged once, not once per scenario; scenario revenue is correctly probability-weighted. This is an extensive-form stochastic LP with a guarantee imposed in each represented scenario.

**The headline gain percentages reproduce:** 47.74% and 52.92%, as conditional model arithmetic. This does not establish implementability or a measured economic benefit.

**The primary 95% and 100% floors are infeasible under the stated constraints.** My independent capacity calculation supports the statuses for both beet variants. Because prices do not enter the capacity problem, both variants share that ceiling.

**The sugar-beet contrast survives.** At 795, the printed optimized plan plants no beet. At 2,400, it plants about 321,074 hectares in my reconstruction, or 321,075 when the rounded printed district areas are added. Its low-scenario water coverage is zero, so the linear `Ky = 1` relationship yields zero beet output, with approximately EGP 5.65 billion in sunk planting costs. This is a result of the current formulation and price assumptions, not a recommended insurance strategy.

**The dual conversion is correct.** For the full stochastic model, the raw water dual measures the change in expected objective from an extra cubic metre in the specified governorate and scenario. Dividing by that scenario's probability gives the stated scenario-normalized marginal value. Representative replays are:

| Variant and cell | Printed raw dual / probability | Recomputed EGP/m³ | Printed EGP/m³ |
|---|---:|---:|---:|
| beet795, Beheira low | 11.884 / 0.23 | 51.669565 | 51.67 |
| beet795, Dakahlia expected | 5.820 / 0.45 | 12.933333 | 12.93 |
| beet795, Qalyubia low | 17.370 / 0.23 | 75.521739 | 75.52 |
| beet795, Damietta low | 11.448 / 0.23 | 49.773913 | 49.78 |
| beet2400, Dakahlia expected | 7.211 / 0.45 | 16.024444 | 16.02 |
| beet2400, Qalyubia low | 18.071 / 0.23 | 78.569565 | 78.57 |
| beet2400, Gharbia high | 3.320 / 0.32 | 10.375000 | 10.38 |
| beet2400, Damietta high | 3.278 / 0.32 | 10.243750 | 10.24 |

Across all 48 cells, the maximum discrepancy from dividing the printed raw duals is approximately **EGP 0.006087/m³**. It is consistent with the combined rounding of raw duals to three decimals and normalized values to two. My independently reconstructed LP also reproduces every raw water dual within **EGP 0.000472/m³**, consistent with three-decimal printing.

The smaller bump test is justified for beet2400. My reconstructed Dakahlia expected-scenario raw dual is approximately **7.211139**; a 1% bump implies **6.679507**, while a 0.1% bump implies **7.211139**. For beet795, both bump sizes reproduce approximately **5.819559**. The choices file should identify the variant for which the larger bump crosses a kink. It should not imply that this happens in both.

These are marginal values under the constrained stochastic model. They are not observed market prices, large-volume transfer prices, or automatically the marginal values of an operating system with planting held fixed after the inflow is observed. No average return is presented as a water price in results note 08 or choices file 04; the text consistently labels averages separately.

**The historical scenario arithmetic survives.** The supplied 100 annual flows sum to **9,193.5 BCM**, with a mean of **91.935 BCM** and sample standard deviation approximately **16.92275 BCM**. The stated band rules produce counts **23, 45, and 32**. Their conditional mean-to-overall-mean ratios round to **0.781, 0.955, and 1.221**. The budgets follow from multiplying those rounded factors by the declared 11 BCM anchor.

**4. Claims that survive only in a smaller or conditional form**

**The gain decomposition is an accounting identity, not a causal explanation.**

Using the exact version 2 amounts quoted in the internal audit:

| Component of the increase in the absolute gain | beet795 | beet2400 |
|---|---:|---:|
| Optimized-margin increase | EGP 10.074151bn | EGP 17.556428bn |
| Baseline-margin decrease | EGP 22.998646bn | EGP 21.327060bn |
| Growth in absolute gain | EGP 33.072797bn | EGP 38.883488bn |
| Share accounted for by baseline decrease | 69.5395% | 54.8486% |

The approximately **69.5%** and **54.8%** shares reproduce. The rounded version 2 margins independently available in note 11 also support those approximate shares. However, the precise old amounts appear only in the internal audit; the version 2 raw run is absent.

What does not follow is that water starvation *caused* 69.5% of the change. Prices, costs, area totals, crop patterns, yield calibration, water requirements, budgets, and probabilities all change between versions. Input-by-input counterfactual runs would be needed to isolate causes, with interactions handled explicitly. Moreover, 69.5% refers to growth in the **absolute EGP gain**, not to 69.5% of the increase from 10.44% to 47.74%.

Acceptable wording: “About 69.5% of the increase in the absolute modeled gain is accounted for by the lower modeled baseline margin. The baseline is evaluated under substantial water scarcity, but the contributions of individual input changes have not been isolated.”

Beside any 47.74% or 52.92% headline, print the absolute optimized and baseline margins; the calibrated budget and full-water demand; the mixed input years; the baseline's modeled staple delivery shares of **69.50% and 64.26%**, respectively; and the physical-land and crop-failure limitations identified above. A gain with those qualifications can be presented as a reproducible model result. It cannot be presented as a feasible current farm-income opportunity.

**The food guarantee protects aggregate harvested tonnage, not each staple or a defined nutritional supply.**

The floor sums wheat, paddy rice, and maize tonnes as interchangeable units. The high-beet plan eliminates rice and nearly eliminates maize. The model does not maintain 90% of each crop, household food access, calories, or milled-rice-equivalent supply. Imports, processing yields, consumption shares, and distribution are absent.

Acceptable wording: “Every represented scenario must deliver at least 90% of a modeled reference quantity of aggregate wheat, paddy rice, and summer-maize tonnage.”

**The method is defensible for an exploratory decision exercise, with the following costs to interpretation.**

| Design choice | Academic assessment | Consequence |
|---|---|---|
| Two stages: all planting before inflow, all water after | Standard and useful for a clearly defined commitment decision | Winter and summer crops do not share one real planting date. The information available at each seasonal decision must be specified. |
| Expected-margin objective | Defensible for a risk-neutral planner comparing farm-budget scenarios | It does not protect farmer income, equity, household survival, or consumers. Crop write-offs can be rational to this objective and unacceptable to the affected farmers. |
| Hard floor in each of three scenarios | A coherent guarantee over the represented states | It is not a guarantee for every possible inflow. A conditional band mean hides worse outcomes within the low band. |
| Linear yield response | A transparent approximation over an explicitly validated water range | It extrapolates a response factor to severe deficits and, as coded, imposes minimum irrigation rather than freely allowing crop failure. Applied-water deficits are not automatically evapotranspiration deficits without an efficiency relationship. |
| One annual crop-area pool | Convenient accounting, insufficient physical representation | It demonstrably permits excessive simultaneous winter planting and ignores rotations and other crops' opportunity costs. |
| Governorate budgets proportional to annual cropped area | A transparent allocation rule for a thought experiment | It is not an observed hydrologic allocation. Budgets exclude transfer options, canal capacity, return flows, groundwater, and spatial access. Water rankings partly reflect this rule. |
| Three scenarios from 1871–1970 annual Aswan flow | A reproducible historical discretization | It is not a validated distribution of current Delta deliveries. Reservoir storage and operating policy break a direct proportional mapping from annual inflow to annual crop supply. |
| Fixed crop prices | Acceptable for small perturbations or stated exogenous price scenarios | The optimized potato area is roughly **476,471 ha**, about **4.90 times** the observed five-crop baseline potato area. Constant prices and unrestricted marketing at that scale need justification, along with labor, seed, finance, storage, and processing capacity. |

The 11 BCM anchor is openly labeled a calibration, which is good practice. That label does not validate the anchor. The current baseline's applied-water demand is **16.7242 BCM**, and its staples alone require **14.6301 BCM**. The middle budget is only about 62.8% of full baseline demand. Expected values, feasibility, and the headline baseline comparison therefore rest heavily on a stress level that has not been matched to observed deliveries.

The net-water sensitivity changes requirements while retaining the same numerical budget. If the primary budget represents applied water, substituting net requirements without putting the supply on the same accounting basis changes effective resource availability. That run is a diagnostic of altered input coefficients, not a physically matched alternative water balance. Its suspect **1,272 m³/ha wheat requirement** is an additional problem, not the only problem. The printed 78.94% gain should not be treated as supporting robustness of the primary result.

**The contribution claim needs to describe what is built.**

An applied combination of established stochastic programming, governorate disaggregation, staple constraints, and scenario water duals is an honest project description. The prior-work review correctly abandons claims of method novelty and of an analytical vacuum in Egyptian institutions. On the summaries supplied, Gohar and colleagues, El Shazly and colleagues, Rosa and Yates, the Egyptian sector-model tradition, and existing food-floor studies are appropriate comparators.

I would accept: “The project implements an exploratory governorate-scale stochastic allocation model for eight Nile Delta governorates, compares outcomes against historical crop areas, and reports staple-floor feasibility, conditional expected margins, and scenario-specific water duals.”

I would not yet accept that it delivers a fully priced 90/95/100% guarantee frontier under the primary case. Two levels are infeasible, and opportunity cost relative to unconstrained optimization is missing from the reported primary table. Nor can this package establish that no earlier work combines the same features: it provides literature summaries and links, not the original papers or a reproducible search record. “Not found in the works reviewed” must remain a bounded search statement, never proof of uniqueness.

**5. Claims that must be withdrawn in their present form**

- That the beet2400 planting is a physically feasible allocation under the supplied land base.
- That EGP 613,178,863 and EGP 8,025,667,499 are standard VSS values relative to an expected-input plan.
- That reproducing the 93.65% ceiling independently proves it is not a formulation artifact.
- That 69.5% of gain growth has been causally attributed to applied-water requirements or water starvation.
- That an unfloored profit-maximizing result of zero staples establishes unavoidable staple failure under a 20% cut.
- That the current LP implements unrestricted crop failure through a true zero-output clipping rule.
- That the primary 90/95/100% table already prices the economic cost of each guarantee level.
- That baseline staple output and effective district yields are directly observed 2020/2021 quantities.
- That the package is sufficient for a complete original-input rerun, or that every headline has been independently replayed from printed log components alone.

No claim of being first, unique, or methodologically new is supported. The old version 2 numbers may remain as explicitly historical results; they should not be called false merely because changed inputs produce different version 3 results. Their empirical validity is a separate question.

**6. The three changes that would most raise the paper's quality**

**First: repair the physical decision model.** Separate seasonal land occupancy from annual cropped area, preserve the competing uses of unmodeled land, and specify water accounting at one consistent boundary. Define whether crops may be abandoned and implement that rule correctly. Name the planting decisions and information available at each date. This addresses an actual feasibility failure and a baseline restriction, not cosmetic realism.

**Second: build and test a coherent empirical reference case.** Use compatible price and cost years, distinguish farmer receipts from procurement prices, retain or explicitly justify the national rescaling of district yields, and match water budgets to measured deliveries or clearly bounded alternatives. Test the rice response factor, water duties, crop caps, and budget allocation rule individually and jointly. The critical tests should cover assumptions that can overturn a conclusion, not just ±20% movements around poorly aligned inputs.

**Third: make the economic comparisons answer the stated decision.** Report the cost of each feasible guarantee relative to the same unconstrained optimum and between adjacent feasible levels. Recompute the expected-input benchmark and report infeasible recourse honestly. Separate technical food capacity from profit-maximizing food output in every stress table. Publish the complete raw inputs, environment specification, unrounded outputs, and small independent verification checks with the paper. Decompose changes between versions through controlled input swaps before assigning causes.

**7. What could not be verified, and the evidence needed**

**Parameter provenance: a substantial internal trace, not external authentication.**

I parsed all thirteen delivered CSVs. The area, production, and yield panels each contain 176 rows, including explicitly unavailable cells; they are not 176 complete observations. Their governorate/crop/season/year keys have no duplicates. I found no area-conversion discrepancy above 0.0051 ha, no yield-conversion discrepancy above 0.001 t/ha, no cost-conversion discrepancy above EGP 0.0051/ha, and no duplicate crop/year/currency keys in the price extract.

The following checks cover prices, costs, yields, land, water, response factors, probabilities, and calibration. “Matches” means that code/log values trace through the supplied foundation to the delivered extract. It does not mean that I independently opened or authenticated the original external publication.

| Parameter used | Value | Internal source chain and year | Finding |
|---|---:|---|---|
| Wheat price | EGP 10,000/t | Foundation §2 → FAOSTAT producer-price CSV, 2023 | Matches |
| Paddy-rice price | EGP 18,761/t | §2 → FAOSTAT, 2023, `rice_paddy` | Matches |
| Maize price | EGP 14,400/t | §2 → FAOSTAT, 2023 | Matches |
| Potato price | EGP 8,160/t | §2 → FAOSTAT, 2023 | Matches |
| Farm-gate beet price | EGP 795/t | §2 → FAOSTAT, 2023 | Matches |
| Procurement beet price | EGP 2,400/t | §3 → procurement CSV, 2024/2025 company announcement as press-reported | Matches extract; commercial basis and year differ |
| Wheat cost | EGP 21,473.81/ha | §4 → CAPMAS/MALR 2016/2017; 9,019/feddan ÷ 0.42 | Matches rounded conversion |
| Rice cost | EGP 19,902.38/ha | §4 → 2016/2017; 8,359 ÷ 0.42 | Matches |
| Summer-maize cost | EGP 18,933.33/ha | §4 → 2016/2017; 7,952 ÷ 0.42 | Matches |
| Beet cost | EGP 17,607.14/ha | §4 → 2016/2017; 7,395 ÷ 0.42 | Matches |
| Potato cost | EGP 49,533.33/ha | §4 → summer potatoes, 2016/2017; 20,804 ÷ 0.42 | Matches; extrapolation to all seasons is assumed |
| Beheira annual cropped area | 720,838.86 ha | §5 → MALR bulletin, 2020/2021, Table 19 | Matches; not physical hectares |
| Damietta annual cropped area | 95,607.96 ha | §5 → same bulletin and year | Matches; cultivated area is only 47,260.08 ha |
| Beheira published wheat yield | 6.838 t/ha | §7 → MALR winter bulletin, 2020/2021, Table 2 | Matches extract; effective modeled yield is subsequently rescaled |
| Qalyubia published potato yield | 42.695 t/ha | §7 → MALR all-season panel, 2020/2021 | Multiplier reproduces approximately 1.504; effective yield is about 42.243 t/ha |
| National wheat yield | Printed 6.57 t/ha | §1 → FAOSTAT via OWID, mean 2014–2023 | Raw files missing; original aggregation cannot be verified |
| National maize yield | Printed 7.37 t/ha | §1 → same route and period | Same limitation |
| Wheat water requirement | 5,126 m³/ha | §8 → CAPMAS 2017 via Abdelwahab et al. 2024 | Matches rounded extract; applied-water basis is an interpretation |
| Rice water requirement | 16,600 m³/ha | §8 → same route | Matches extract |
| Summer-maize water requirement | 9,305 m³/ha | §8 → same route | Matches rounded extract |
| Beet water requirement | 9,426 m³/ha | §8 → same route | Matches; geographic transfer and basis need validation |
| Potato water requirement | 4,825.84668 m³/ha | §8 → winter 4,079 and summer 6,145, weighted by 61,667.34 and 34,913.34 ha from 2020/2021 | Arithmetic matches; Nili excluded, then one coefficient used for all potatoes |
| Winter-wheat response | 1.05 | §9 → FAO 33 (1979), as tabulated in FAO 56 (1998) and FAO 66 (2012) | Matches secondary-source extract |
| Maize response | 1.25 | §9 → same FAO family | Matches |
| Beet response | 1.00 | §9 → same FAO family | Matches |
| Potato response | 1.10 | §9 → same FAO family | Matches |
| Rice response | 1.20 | §9; CSV explicitly says GAP | No verified source; declared inherited assumption |
| Scenario probabilities | 0.23, 0.45, 0.32 | §10 → Cobb (1978), annual Aswan series 1871–1970 | Counts reproduce; modern delivery probabilities not established |
| Scenario multipliers | 0.781, 0.955, 1.221 | §10 → conditional means of those historical bands | Reproduce after rounding |
| Water anchor | 11.00 BCM | §11 | Explicit calibration; not an official eight-governorate budget |
| Crop caps | 0.50, 0.35, 0.40, 0.30, 0.15 | Choices and code, carried from version 2 | Declared modeling device; no empirical validation supplied |

The 2025 wheat variant also uses **14,667**, whereas the procurement CSV carries **14,666.67** and the exact conversion of 2,200 per 150 kg is 14,666.666…. This is a disclosed-scale rounding choice, not a material economic error.

**Material open gaps and their consequences.**

| Gap | Materiality | What would settle it |
|---|---|---|
| Recent crop-specific costs | Critical to margins, planting, duals, and information values; not to the purely technical capacity ceiling | Comparable year crop budgets, with rent and marketing treatment stated; crop-specific sensitivity where actual data remain missing |
| Actual Delta deliveries and the 11 BCM calibration | Critical to feasibility, scarcity values, and baseline comparison | Measured or institutionally documented deliveries for the defined crop area and accounting boundary, with scenario construction tied to operating policy |
| Post-1970 flows, reservoir buffering, and multi-year droughts | Critical to interpreting probabilities as current supply risk | A modern hydrologic/release series or a justified reservoir-operation mapping; contemporary data alone do not remove the need for that mapping |
| Primary water duties and uncertain applied/net basis | Critical to scarcity and feasibility | Original duty definitions, relevant geography and seasons, and a consistent supply-demand accounting basis |
| Unverified rice `Ky = 1.20` | Material to baseline revenue, allocation, and duals; less important to the maximum-staple ceiling where wheat and maize dominate | A suitable seasonal estimate and tests over a justified range. As a diagnostic only, setting it to 1.00 changes the beet795 gain to about 42.18%; that alternative is not asserted to be correct |
| Beet applied requirement | Material to beet2400 and the fixed baseline; not the direct driver of maximum staple capacity | Crop- and region-specific applied-water evidence and efficiency treatment |
| Potato seasons and market capacity | Critical to the proposed expansion and seasonal land feasibility | Separate seasonal areas, costs, water requirements, yields, and documented limits or demand responses |
| National yield raw files and rescaling rationale | Material to the reference output and ceiling | Complete national annual files, extraction dates, aggregation checks, and a reason to prefer normalized historical yields over direct district yields |
| Menoufia rice fill | Small for baseline area because 7.98 ha is tiny; potentially relevant to local alternatives and values | Missing-year observation or a bounded sensitivity; do not treat an unreported cell as confirmed absence |
| Nili maize omission | Material to describing the annual baseline as complete; effect for these eight governorates is not quantified | Extract the missing governorate tables and reconcile annual crop totals |
| Conflicting national fresh-water totals | Secondary to current results because neither total fixes the 11 BCM anchor | Reconcile before using those totals as model-budget evidence; resolving 59.25 versus 59.68 BCM alone will not validate the current regional budget |
| FAOSTAT mirror route | Less concerning than absent raw files and mixed-year/quantity definitions | Retain the actual raw extract and, ideally, a direct-source cross-check; a mirror is not itself evidence of wrong data |

**Missing material prevents full original-input reproducibility.**

The combined package lacks the national OWID yield and production files read by `load_crop_facts`, the version 2 model and raw run logs, the three detailed research-notes files, and the original source PDFs/tables. The foundation also contains the literal text **`...[truncated 13571 chars]`** near the end of section 10. That is missing source content in the supplied document, not a display limitation introduced by this audit.

Consequently I cannot authenticate source transcriptions, repeat the original national averages, verify the exact old benchmark amounts, reproduce the historical claim about the version 2 evaluation path, or confirm each literature summary and the claimed breadth of its search. The statement that no public post-1970 extractable series exists is also not established by this package; the defensible statement is that this project did not obtain one.

**Scope of the independent numerical checks.** I read the delivered narrative and code, parsed the thirteen CSVs, replayed the log arithmetic, and wrote a separate LP reconstruction rather than relying on the internal audit or the project's PuLP code. National mean yields were reconstructed to high accuracy from the log's printed production/area ratios because the raw national files are absent. The reconstructed primary objective values are within approximately EGP 1,480 and EGP 687 of the printed optimized margins; the absolute differences are negligible relative to totals near EGP 140–148 billion and do not change any reported percentage. The reconstruction's feasible solutions were checked against their constraints and independent dual optimality certificates. Its capacity ceiling was also checked by direct wheat-then-maize arithmetic. These checks support internal numerical consistency; they do not validate the physical assumptions or authenticate the external sources.

The strongest part of the work is the effort to make assumptions and failed claims visible. The decisive next standard is stricter: the physical allocation must be possible, the comparison must answer the stated economic question, and the evidence must support the claimed real-world interpretation.
