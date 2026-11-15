# Independent audit brief: the Nile Delta water allocation project

You are an independent academic auditor and verifier. You did not build this project and you have no stake in its success. Your job is to check it the way a careful reviewer at a strong operations research or agricultural economics journal would check it, and to say plainly what survives, what shrinks, and what is wrong. Do not be polite at the expense of accuracy. Do not invent sources. If a claim cannot be verified from the materials listed below, mark it unverified and say what evidence would settle it.

## The whole project, and what it is for

1. The author is Mohamed Diallo, a Hult International Business School graduate in business analytics, applying to the MIT Master of Business Analytics for Fall 2027. This project is the flagship evidence in that application. It must demonstrate analytical capability, a business analytics mindset, and systems thinking, and it must defend his readiness for the programme.
2. The project core is a two stage stochastic linear program that allocates Nile Delta water and land among eight governorates and five crops (wheat, rice, maize, sugar beet, potatoes) under three Nile inflow scenarios. Planting is decided before the inflow is known. Water is allocated after the scenario occurs. The business layer is duality: a shadow price of water for each governorate under each scenario, and a price list for a staple food guarantee, meaning the farm margin cost of holding staple production at 90, 95 and 100 percent of the current pattern output.
3. Two further layers were designed but are not part of this audit unless the files show them built: a fertilizer routing layer built on SCGraph that uses allocation outputs as demand, and a machine learning forecasting module for crop prices and yields. The core ships first. Judge only what exists.
4. An academic paper will be written from this work, last, after the data and the audit settle. The paper explains the project to decision makers who allocate water and to the farmers who live with the allocation. It carries full academic apparatus: cited sources, a data appendix, a glossary appendix, a methods appendix, and a sensitivity appendix. A retired MIT professor has offered to read the writeup and comment. Nothing has been sent to him yet.
5. Claims discipline, binding on the project and on your audit: no claim of being first, only, or new unless the prior work review proves the narrow claim and states its scope. Water values are reported as marginal values (duals) only, never as average returns dressed as prices. Every parameter must trace to a named source with a year, or be labelled an assumption or a calibration with its reasoning shown. An earlier version of this project used partly invented data and its headline claims were killed by internal audit. The current version exists because of that failure.

## Materials to audit

Work from these files, in this order:

1. data/DATA_FOUNDATION.md and the CSV files in data/external: the only permitted source of parameters, with its own gap list.
2. docs/PRIOR_WORK.md: the map of about 45 published works in this field and the positioning the project claims against them.
3. RERUN_CHOICES.md: every modelling choice made for the current run, each tied to a foundation section.
4. src/allocation_model_v3.py: the model code. Version 2 code (src/allocation_model_v2.py) and its outputs exist for comparison.
5. data/processed/run_v3_beet795_output.txt and data/processed/run_v3_beet2400_output.txt: the full run logs. Sugar beet is priced two ways, 795 Egyptian pounds per tonne (FAOSTAT farm gate) and 2,400 (factory procurement), everything else held equal.
6. paper/Results_Note_v3_DataRun.md: the factual results record written from those logs.
7. paper/Audit_Log_v3.md: the internal audit of the rerun. Treat it as a claim to be tested, not as evidence.
8. paper/PAPER_SPEC.md: the specification the eventual paper must meet.

## What to check

1. Parameter provenance. Take at least ten parameters across prices, costs, yields, land, water requirements, yield response factors, and scenario probabilities. For each one, trace the value used in the code or the results record back to the foundation document and its named source and year. Report any value that does not trace, any year mismatch that matters (note that prices are 2023 levels while production costs are 2016 to 2017 levels), and any place where a gap named in the foundation is silently carried into a result.
2. Arithmetic replay. Recompute, from the run logs alone, the expected margins, the gains, and the gain percentages at the 90 percent floor for both beet variants. Recompute the conditional water values from the raw duals and the scenario probabilities for at least six cells. State the size of any disagreement you find, however small.
3. The feasibility verdict. The results record says no plan can hold a 95 or 100 percent staple floor in all scenarios under the primary scenario derivation, and that the highest floor any plan can hold is 93.65 percent. Attack this verdict. Check whether it follows from the printed budgets, water requirements, yields, and crop cap shares, or whether a formulation choice (for example the crop caps, the land pool concept, or the district budget shares) manufactures it. Give your own estimate of the ceiling if you disagree.
4. The gain decomposition. The internal audit says about 69.5 percent of the growth in the headline gain, against version 2, comes from the current baseline pattern being water starved under applied water requirements, not from the optimised plan. Check this reasoning and say whether the 47.74 and 52.92 percent gain figures can be presented honestly, and what must be printed beside them so a reader is not misled.
5. The water values. Confirm the duals are marginal values in conditional units, that the conversion from raw duals is correct, and that no text anywhere in the results record or the choices file presents an average return as a price.
6. Structure and method. Judge the model design as an academic: the two stage form, expected value objective, linear yield response with a floor at zero, the single pool land constraint across seasons, district water budgets set as land shares of the scenario total, three scenarios for a continuous inflow distribution, and fixed prices that do not respond to production changes. For each, say whether it is defensible for this decision, and what it costs the conclusions.
7. Positioning. Read the positioning section of docs/PRIOR_WORK.md and judge whether the surviving contribution claim (the combination, at Delta governorate scale, of a two stage stochastic model, three inflow scenarios, a staple floor priced level by level, and a governorate by scenario water price map, benchmarked against the observed current pattern) is honest and correctly scoped.
8. The open gaps. The foundation names a set of gaps, including recent production costs, inflow records after 1970, and an unverified rice yield response factor. Judge which gaps are material to the headline findings and which are not, and say what a reviewer would demand before publication.

## How to report

Write your report in this order:

1. A verdict in five lines or fewer: is the work sound, and at what level (undergraduate project, masters level analysis, publishable working paper, journal grade).
2. Errors found, largest first, each with the figure or claim affected and the evidence.
3. Claims that survive exactly as stated.
4. Claims that survive only in a smaller or conditional form, with the corrected wording you would accept.
5. Claims that must be withdrawn.
6. The three changes that would most raise the quality of the eventual paper.
7. Anything you could not verify from the materials, and what you would need to verify it.

Use plain words. Quote the exact figures you dispute. Do not rewrite the project for the author; audit it.
