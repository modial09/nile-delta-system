# Muse brief: rebuild the analytical foundation, then design the decision interface

Prepared 15 November 2026. Status: proposed execution brief; current model results remain independently unverified.

## Recommendation and scope

Strengthen the evidence and model before building the public interface. Make the core question: **Which aggregate staple-production promises can the study area support, at what modeled opportunity cost, and under which explicit assumptions?**

This is a two-layer project:

1. A reproducible analytical foundation: source data, cleaning, parameter construction, model, verification, and explanation.
2. A decision interface that faithfully displays those verified outputs and makes their assumptions inspectable.

The research model is stochastic because it represents uncertain outcomes. Its data processing and verification should be deterministic and reproducible. Do not describe it as deterministic merely because it uses an optimization solver.

My objective is to demonstrate rigorous analytical judgment, transparent reasoning, and ownership of the work. Do not optimize the project for impressive numbers, complex algorithms, or assumed admissions preferences. Do not promise an admissions outcome. A smaller result that survives scrutiny is more valuable than an expansive unsupported claim.

Work on the foundation first. Write a UX specification in parallel only where it does not depend on unsettled numbers. Build a local, private interface after the analytical acceptance gate passes. If the analytical gate cannot pass, retain an explicitly illustrative model and a labeled demonstration; do not present it as validated policy evidence.

## Your role and operating rules

Act as a rigorous research lead. Coordinate these responsibilities if actual capabilities permit: agricultural economics, Egyptian irrigation/hydrology, operations research, data engineering/statistics, and explanatory UX. Roles are responsibilities, not evidence that real domain experts participated. If only one model is available, perform separate review passes and label them author review. Never invent a team, credentials, independent review, or executed tests.

Use actual executable calculations for arithmetic, units, reconciliation, and solver checks. Use AI for interpretation, source discovery, competing explanations, and clear writing. Separate verification of the code's calculation from validation of the physical and economic model.

Preserve the existing project. Create a working branch or a versioned copy as appropriate. Preserve raw inputs and old results; do not overwrite inconvenient evidence. Record meaningful changes and their effect on findings. Do not upload confidential files, buy services, publish the interface, or contact anyone without authorization.

For each important claim distinguish:

- **Confirmed observation:** directly checked against a named source or original record.
- **Confirmed computation:** reproduced from recorded inputs, code, and execution output.
- **Reported:** asserted in the paper but not independently reproduced.
- **Inference:** an interpretation supported by specified evidence.
- **Assumption/calibration:** a chosen value or relationship, with its reason and sensitivity.
- **Unverified:** required evidence is absent or unresolved.

Do not protect either the paper or the earlier critiques. Test both. Correct a critique when the evidence contradicts it. Never transfer a version 3 finding to revised version 4.1 without checking the changed code and inputs.

For a specific failed check, identify the cause, apply a targeted correction, and recheck its dependencies. Permit at most two unsuccessful correction attempts before reporting that issue and the evidence needed. Continue independent work that remains valid. Do not repeat an unchanged failed search indefinitely.

## Start from the actual project, not the PDF alone

The supplied paper is `Nile_Delta_Paper.pdf`. On Mohamed's current host it is at `/Users/mohameddiallo/Downloads/Nile_Delta_Paper.pdf`; this is a locator, not proof that Muse can access that filesystem.

First inspect the current repository, source register, source tables, model code, forecast code, raw and processed data, run logs, tests, and any re-audit. The PDF describes `src/allocation_model_v4_1.py`. Establish which actual version produced it. Ask Mohamed for missing files only after checking what is accessible. A PDF is insufficient to verify source transcription, model execution, or forecasting performance.

Known reported results, to investigate rather than preserve as targets:

- 80.25% aggregate staple ceiling; 80% floor expected margin of EGP 175.144 billion.
- EGP 227.935 billion opportunity cost against the unrestricted optimum.
- Historical baseline worst-scenario output of 60.12%, alongside a claim that it meets no ladder level.
- A plan meeting its floor in 65 of 100 sampled hydrologic tests.
- Water values from an LP relaxation of a model with discrete keep/abandon decisions.
- Forecast 2024 prices combined with official 2022 costs and historical area/yield panels.
- Extreme potato-area expansion under fixed output prices.

These are PDF claims. None becomes a validated result through repetition in this brief.

## S1. Inventory, decision definition, and claim register

**Owner:** research lead with Mohamed responsible for material scope decisions.

Produce an inventory with file versions and hashes, a claim register linking each headline to its inputs and generating calculation, and a one-page decision definition. Define the decision maker, geographical boundary, modeled activities, time horizon, resource accounting boundary, information available at each decision date, and exactly what the guarantee protects.

Recommend one primary case. Prefer a documented historical decision experiment with the most coherent available data over a nominally current case assembled from incompatible years. If no coherent empirical case exists, label the primary analysis illustrative. Do not choose a year merely to retain an existing headline. Distinguish a retrospective reconstruction from a genuine forecast available at that time.

Classify each model feature as required core, diagnostic sensitivity, or deferred extension. Retain the forecast module if it adds defensible information or demonstrates a meaningful benchmark result. Do not require machine learning to win. Defer supply routing, fertilizer optimization, extra crops without data, and other expansion until the core passes.

**Output:** inventory, decision definition, claim register, prioritized defect list, proposed source plan.

**Acceptance:** every headline is traceable or marked unverified; material definitions and dates are explicit. Ask Mohamed only about a consequential choice that changes the intended decision or scope. Routine repairs within the agreed scope proceed without repeated approval.

## S2. Source integrity, cleaning, and parameter construction

**Owner:** data/reproducibility analyst; hydrology and agricultural economics review relevant definitions.

Retain immutable raw inputs with source URL or supplied-file locator, publication date where known, access date, page/table identifiers, extraction method, and checksum. Record original units and converted units. Keep observed year, publication year, forecast target year, and retrieval date separate.

Build explicit keys for governorate, crop/activity, season, and agricultural year. Name currency and price basis. Test uniqueness and join cardinality; report unmatched records and changes in row counts. Missing, zero, not applicable, and not reported must remain distinct. Reconcile governorate subtotals to appropriate source totals where possible. Inspect original Arabic tables for material values rather than relying only on an English search or secondary transcription.

Log each cleaning or transformation rule with its reason, affected rows, and before/after checks. Do not silently fill gaps. Record the source of each imputation and its influence on results. Check feddan/hectare, tonne/ardab, mm/m³, water scaling inside the solver, and nominal versus real currency.

Create a parameter dictionary with: value/range, unit, location, season, year, source identifier, transformation, status, and assumption identifier. Explain any district-yield normalization. Keep directly observed yields distinct from modeled or forecast yields.

Document the computational pipeline:

`original sources → extracted tables → cleaned data → parameter sets → scenarios → optimization → checks → result records → paper/interface`.

Show what each arrow changes. Readers should be able to follow one governorate/crop record through the complete path. Use the same transformation code for the paper and interface; do not create an independent calculation path in the frontend.

**Output:** versioned source register, cleaned datasets, transformation log, parameter dictionary, data-quality report, lineage diagram.

**Acceptance:** the selected primary inputs reproduce from supplied originals with documented exceptions; important missing cells, unit conflicts, or unsupported parameter definitions cannot be silently admitted to the primary case.

## S3. Physical, economic, and information-timing model

**Owners:** operations-research analyst, hydrology analyst, agricultural economist.

### Land and water

Check physical land occupancy for crops that overlap in the real calendar. Separate winter, summer, and Nili labels do not automatically prevent overlapping occupation. Add a documented occupancy calendar or monthly constraints if the data support them; otherwise state the approximation and bound its effect.

Account for unmodeled crops. Prefer their observed seasonal occupations where available. If seasonal reserves are inferred from annual totals, explain the construction, quantify any area that loses a seasonal home, and test alternative defensible allocations. Do not conceal the reported 30,136 crop-hectare reserve discrepancy.

Define the water boundary before adding constraints: canal release, district delivery, field application, or crop consumption. Do not directly equate satellite evapotranspiration with irrigation deliveries or treat it as a calibrated water-budget validation. Distinguish withdrawals, deliveries, consumption, and recoverable return flows. Keep a simplified water-budget model if a full hydrological network is unsupported; do not imply it simulates dam operations.

### Economics and markets

Reconcile prices and costs to a defensible common reference, or clearly present mixed-year scenarios with meaningful crop-specific uncertainty. Distinguish farmer receipts, procurement prices, quality adjustments, and delivery costs. Retain the winter-potato cost gap as an assumption until evidence closes it.

Treat unlimited potato sales at fixed prices as a relaxed diagnostic, not the principal implementable opportunity. Build a transparent, more constrained primary case using observed areas and documented adjustment/market limits where available. Sensitivity-test any assumed bounds. If credible demand evidence exists, consider a piecewise market-response formulation; do not fabricate elasticities or import a national demand curve without checking the study area's market linkages. Compare relaxed and restricted cases so readers can see what the benchmark changes.

Retain aggregate wheat, paddy-rice, and summer-maize tonnage as the narrow primary guarantee if that remains the chosen question. State that it does not protect each crop, calories, household access, or processed rice supply. Do not bolt on a nutritional model without the required conversion and consumption evidence.

### Timing and uncertainty

Write an information timeline. Identify what is known at winter planting, summer/Nili planting, irrigation allocation, and harvest. Enforce nonanticipativity: decisions with identical observed information must be identical. Do not let water allocation use realized yield or prices that would only be learned later without labeling this as an ideal-information assumption and testing its effect.

Reassess the scenario construction. The paper combines annual inflows with overlapping ten-year means; do not treat the resulting weights as established present-day supply probabilities. For the primary case, choose one well-defined uncertainty object and time horizon. Treat multi-year drought as a separate stress or model a storage/operating-policy link if adequate data exist. Where probabilities cannot be justified, show stress cases rather than false probability precision.

Check the joint behavior of prices, yields, crops, and hydrology. Perfect common price/yield movement and independence from inflow require evidence or explicit sensitivity. Evaluate forecast intervals for coverage as well as point accuracy. Do not convert forecast RMSE into quartile probabilities without a defensible distributional argument.

For historical forecasts, respect actual information availability. Fit transformations and select models using training information only. Keep the evaluation periods separate from model selection or label the selection bias. Investigate the paper's differing price and yield forecast target years. Forecast accuracy and allocation quality are different outcomes: a statistically better forecast need not produce a better planting decision.

**Output:** equations, decision/information timeline, a dependency table explaining how inputs affect decisions and outputs, primary configuration, and a small set of diagnostic configurations.

**Acceptance:** the model is internally coherent at the chosen physical/economic boundary; assumptions that remain unresolved have bounded interpretations. Do not add complexity solely to appear advanced.

## S4. Independent verification and robustness

**Owner:** verification analyst, separate from the model author where actual access permits.

First reconcile the baseline statement. If its worst-scenario output is 60.12% of the same reference, explain how it could fail a 50% floor. Inspect whether different statuses, definitions, constraints, or evaluations are being mixed. Resolve with code and unrounded results; do not presume that the earlier critique or the paper is correct.

Test at least these substantive properties:

1. Every accepted plan respects actual overlapping land, water budgets, valid crop responses, and nonanticipativity.
2. Abandonment gives zero water and output while preserving incurred costs. If minimum viable water is assumed, its meaning and sensitivity are explicit.
3. Increasing a hard staple floor cannot improve the globally optimal profit under an otherwise identical maximization problem. Increasing available water cannot reduce the optimal objective or maximum feasible staple capacity. Apply tolerances and solver bounds correctly.
4. Scenario probabilities sum to one; expected values independently recompute from scenario results. Costs are charged once for each planting commitment with the correct probability weighting.
5. The guarantee's cost is the difference from the same model without that guarantee. Historical-pattern comparison is a separate result. Infeasible or failed runs never acquire invented zero margins.
6. Capacity and chosen production are reported separately under stress. A profit-maximizing zero does not mean zero physical capacity.
7. Standard expected-value and perfect-information calculations use comparable decisions, information, objectives, and feasible sets. An infeasible expected-value plan is not assigned a finite standard VSS. Penalized variants retain their penalty and definition.
8. LP-relaxation duals are labeled as such. Because abandonment decisions are discrete, show finite water increments on the full mixed-integer model as separate operational sensitivities. Report LP/MIP objective differences, degeneracy, and scale dependence. A relaxation dual is not automatically an operational marginal value of the integer model.
9. Out-of-sample policy tests use an explicit rule for how late decisions respond to observed information. Freezing every sample at the normal-state planting rule must be labeled and compared with the intended adaptive policy. Do not call mixed annual/window sample frequencies measured annual reliability.
10. Test numerical scaling, solver status, bounds/gaps, and tolerances near feasibility limits. Preserve failed runs and explain discrepancies.

Use a small hand-solvable example, an independent calculation/solver for important results, and saved unrounded outputs. Define unit-specific tolerances before judging agreement. Separate numerical tolerance from substantive parameter uncertainty.

Test the economic conclusions under a restricted market case, alternative land reserves, plausible costs, water budgets, response factors, forecast errors, and alternative dependence assumptions. Report what changes the recommendation, not merely every number that can be varied.

**Output:** executed test report, independent calculation record, revised claim register, sensitivity summary, unresolved issues with consequences.

**Gate A:** validated research results require the material physical/economic checks and independent numerical checks to pass. A missing essential dataset or unresolved contradiction blocks empirical-policy claims, not the delivery of an honest illustrative study. Cross-vendor AI critique is useful only with verified vendor identity and available authorized access; it supplements executable checks and does not substitute for a real Egyptian irrigation/agricultural specialist. If unavailable, mark independent critique pending and provide its brief.

## S5. Short research narrative and evidence package

**Owner:** research lead/editor; Mohamed owns the final account of his contributions.

The current PDF already has about ten pages of main discussion; much of the 28-page length consists of references and appendices. Do not delete methodological evidence to achieve a cosmetic page count.

Aim for a **6–8 page main research memo**, plus separate technical appendices and repository documentation. This is an editorial target, not an admissions rule:

- One-page executive summary: question, method, central result, conditions, and implication.
- One page on the decision, prior work, and narrow contribution.
- One to two pages on data, cleaning, timing, and the model, with a compact lineage diagram.
- Two pages on the guarantee trade-off, benchmark, stress/robustness, and one district comparison.
- One page on limitations, what changed after audit, and what evidence is needed next.

Keep formulas, source tables, complete forecast scores, extraction details, solver settings, and expanded sensitivities in appendices. Use three or four decisive figures rather than repeating every table in prose. Give each main result its units, reference case, source, and material caveat nearby.

Use plain English and ASD-STE100 principles: short sentences, stable terms, explained technical words, and direct verbs. Do not claim certified compliance without a proper language check. Clearly distinguish a claim about the model from a claim about Egypt.

Produce a short contribution record: what Mohamed decided, implemented, checked, rejected, or revised; what AI assisted; what external reviewers actually verified. Supply a brief oral-defense sheet with the hardest questions and evidence-backed answers. Do not invent a personal story or expert endorsement.

**Output:** research memo, executive summary of at most 300 words, technical appendices, contribution record, oral-defense sheet.

**Acceptance:** all displayed findings derive from the same approved result records; contradictions and unsupported novelty/policy claims are absent; the author can explain the methods without relying on polished wording.

## S6. Interface specification, then a private prototype

**Owners:** explanatory UX lead with the data analyst owning result bindings.

Design for a reader who needs to understand a decision in two minutes and inspect its evidence in more depth. The interface is a way to examine assumptions and consequences, not evidence that the model is correct.

Use one front page with these views:

1. **The question and reference case:** selected period, geography, data mode, and what the staple promise means.
2. **Choose a promise:** a discrete control over verified floor levels. Show expected margin, opportunity cost, worst-case tonnage, and feasibility together. Label the reference used for opportunity cost.
3. **Where outcomes differ:** a governorate comparison or map linked to an accessible ranked table; explain what each water value represents and its model type.
4. **Test the assumptions:** a small selection of verified water, cost/market, and land-reserve cases. Show which change materially alters the conclusion.
5. **What the model leaves out:** a concise limitations panel with access to source and method details.

Prefer a saved, versioned result explorer first. A live solver is optional later and only if it adds a needed interaction. If the interface reads precomputed runs, only allow combinations actually computed. Do not interpolate across feasibility boundaries or invent solver responses. A failed or missing run displays unavailable status, not zero. Prevent stale outputs from appearing under newly changed controls.

Separate three data modes visibly at all times:

- **Observed historical data:** what sources record; never an optimized result.
- **Modeled case:** output of a named verified configuration with its historical/as-of dates.
- **Synthetic teaching example:** fabricated solely to explain the mechanism, clearly labeled and excluded from empirical claims and model validation.

Use genuine prior-year cases only when data availability, cost/price basis, and forecast cutoffs support them. Do not attach real years to synthetic outputs. Do not show a historical replay as an actual forecast made at that date.

Give every result record a stable run ID, source/input hashes, model/code version, configuration and assumption IDs, decision/as-of dates, reference quantity, units and economic basis, scenario probabilities, solver status and gap/bound, objective, floor/capacity information, scenario and governorate outputs, benchmark ID, and value type (observation, model output, LP dual, or finite MIP increment). Infeasible quantities remain null with an explanation. The paper and frontend must consume these same records.

Test feasible/infeasible transitions, missing and stale data, mode changes, keyboard use, mobile layout, labels/units, and a reader's interpretation. A synthetic or precomputed demo must never imply live computation. Use a table if a map would add little. Do not build an AI chat panel unless a tested reader need justifies it.

**Gate B:** build a private/local prototype only after Gate A permits the displayed claims. An illustrative prototype is allowed with persistent illustrative labels. Mohamed reviews the final paper and prototype before any public publication. Do not add per-file or per-edit approval steps.

## Execution outputs and first response

Keep one progress/decision record. Report completed checks separately from planned checks. Do not create a report claiming a test passed because the test was merely specified.

First return:

1. What current files and execution capabilities are actually available.
2. The five highest-impact issues, each with evidence status and practical consequence.
3. The proposed primary decision case, what is core/deferred, and the exact first checks.
4. Only the missing information that is necessary to continue.

Then perform the authorized foundation work in order. Provide concrete outputs and evidence after each stage. Do not build a polished interface while the numerical basis remains unsettled.

Optional companion handoff files, when supplied: `workflow-spec.md`, `stages.json`, `acceptance-tests.md`, `eval-cases.json`, `evaluation-report.md`, `critic-brief.md`, and `source-register.md`. They organize this brief; they do not replace it. If only this Markdown prompt is supplied, it is sufficient to start S1.

## Method references and their limited purpose

These sources support checking principles, not the project's numerical inputs. Reopen source material as needed and retain its actual access date.

- Forecasting with rolling historical origins and appropriate benchmarks: Hyndman and Athanasopoulos, *Forecasting: Principles and Practice*, [forecaster's toolbox](https://otexts.com/fpp3/toolbox.html), especially time-series cross-validation. Training must precede the period evaluated.
- [Gurobi guidance on dual values in mixed-integer models](https://support.gurobi.com/hc/en-us/articles/360034305272-How-do-I-retrieve-the-dual-Pi-values-for-a-MIP-problem), updated 23 February 2026. This supports distinguishing continuous-model duals from sensitivities of a discrete allocation; it is not a requirement to adopt Gurobi.
- [FAO AQUASTAT water-use methodology](https://www.fao.org/aquastat/en/overview/methodology/water-use/). This supports separating water withdrawal, consumption, and returns; it does not validate the study's regional supply calibration.

Do not claim that this execution brief, the proposed model, or the future interface has already passed independent expert verification.
