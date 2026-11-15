# S1 Inventory: Nile Delta repository as found on 15 November 2026

Stage S1 of the foundation rebuild, written under docs/handoff_2026-11-15/builder-brief.md Section S1. This file records what exists, what version evidence it carries, and which code generated the current paper. Nothing was rerun and nothing was fixed. All dates and times below are file system modification times on this machine, Africa/Cairo time.

## 1. Repository shape

The repository holds 173 files outside the Python virtual environment and the git internals. One git commit exists: a6dc190, dated 1 November 2026, titled as the initial scaffold. That commit tracks 15 files only: the scaffold code (src/allocation_model.py, src/data_loading.py, src/forecasting.py, src/routing_model.py), the design and problem statement documents, the paper outline, data/SOURCES.md, requirements.txt, the README and two placeholder files. No git remote is configured. Every file produced after 1 November 2026, including all model versions 2 to 4.1, all run outputs, all audits and the paper itself, is uncommitted working tree material. Version identity for everything after the scaffold therefore rests on file names, internal version labels and timestamps alone. There is no commit history to appeal to.

The README.md at the root is still the 1 November 2026 scaffold text. It does not describe the current model, the current data or the current paper.

## 2. The chain that produced the current paper

The paper is paper/Nile_Delta_Paper.md (saved 14 November 2026 at 18:14), rendered to HTML and PDF at 18:16 by paper/render_paper.py. The PDF has 28 pages at A4. The chain behind it, in time order on 14 November 2026:

| Time | Artefact | Role in the chain |
| --- | --- | --- |
| 16:36 to 16:39 | src/forecasting.py saved; data/processed/forecast_prices_yields_v4.csv, backtest_scores_v4.csv and run_forecasting_v4.txt written; docs/FORECASTING_RESULTS.md written | The forecast module and its saved outputs |
| 17:13 to 17:15 | src/allocation_model_v4.py saved; run_v4 logs and plan_v4_robust_plan.csv written | The version 4 build, kept on disk |
| 17:17 to 17:30 | paper/Results_Note_v4.md and paper/Audit_Log_v4.md written, with data/processed/audit_v4_work/ scripts | The version 4 results note and its audit |
| 17:44 | paper/Results_Note_v4_1.md written | The version 4.1 results note |
| 17:47 to 17:52 | data/processed/audit_v4_1_work/au.py and its nine JSON outputs written | The independent reaudit computations |
| 17:56 | paper/Audit_Log_v4_1.md written | The reaudit verdict: 49 figures survived, 5 shrunk, 0 withdrawn, of 54 |
| 18:00 | src/allocation_model_v4_1.py saved in its current form | The model code the paper cites |
| 18:01 to 18:02 | data/processed/run_v4_1_main.txt, run_v4_1_caps.txt, run_v4_1_beet2400.txt, run_v4_1_robust.txt and robustness_samples_v4_1.csv written | The surviving author run logs for version 4.1 |
| 18:07 to 18:08 | data/processed/plan_precision_recovery.py run; plan_v4_1_floor50 to floor80 CSVs and plan_v4_1_robust_plan.csv written at full precision | The saved plans at full precision |
| 18:10 | paper/Results_Note_v4_2.md written | The corrected note: two one pound step costs repaired |
| 18:14 to 18:16 | paper/Nile_Delta_Paper.md, then HTML, PDF and paper/Audit_Log_Paper.md | The paper and its own audit log |

Two facts in this table matter for S4. First, the reaudit artefacts predate the final saved form of the code they audit: au.py and its JSON outputs are stamped 17:47 to 17:52 and the audit log 17:56, while src/allocation_model_v4_1.py is stamped 18:00 and the surviving author run logs 18:01 to 18:02. Second, no run log from the version 4.1 run that fed Results_Note_v4_1 at 17:44 survives on disk; the log on disk is the 18:01 run. The numbers agree between the audit outputs, the 18:01 log and the note, at almost every point checked in the claim register. The chain therefore proves numerical agreement. It cannot prove that the code file on disk is byte for byte the code the reaudit executed. Both points are carried into S1_Defect_List.md.

## 3. Which code generated the paper

Verdict: the version 4.1 build generated the paper, and src/allocation_model_v4_1.py is the right file to cite, with one stated reservation.

Evidence for the verdict. The paper Appendix C names src/allocation_model_v4_1.py as the exact build. The file opens with a docstring that labels it version 4.1, a repair build of version 4, built to docs/FOUNDATIONS.md combined version 2 and to the repair list in paper/Audit_Log_v4.md. The run logs on disk self title as version 4.1 repair build and print the paper headline numbers: the frontier table, the ceiling at 9,833,867 tonnes, the baseline figures, the information values and the stress pairs all appear in data/processed/run_v4_1_main.txt with the values the paper prints. The reaudit JSON outputs in data/processed/audit_v4_1_work/ reproduce the same values from an independent rebuild, in unrounded form. Results_Note_v4_2.md, the note the paper follows, cites the same run.

The reservation. Because the audit artefacts predate the final save of the code file, and because no earlier version 4.1 run log survives, identity between the audited build and the saved file rests on numerical agreement rather than on a hash or a commit. S4 should treat the saved file as the generating code and should say that the audit agreement is numerical, not byte level.

No other candidate version fits. Version 4 outputs (run_v4_main.txt, Results_Note_v4.md) carry different headline values and a different yield basis, and the paper prints the version 4 construction only as a labelled sensitivity. Version 3 material lives in audit_package/ as a frozen bundle dated 14 November 2026 at 15:02 and in paper/Results_Note_v3.md; its numbers do not appear in the paper.

## 4. Material files by group

Sizes are in bytes. Dates are modification dates in November 2026. The full SHA256 hash of every file is in the appendix to this document.

### 4.1 Source code, src/

| File | Size | Modified | What it is |
| --- | --- | --- | --- |
| allocation_model_v4_1.py | 63,648 | 14 Nov, 18:00 | The generating model code for the paper |
| allocation_model_v4.py | 53,549 | 14 Nov, 17:13 | The version 4 build, kept unchanged |
| allocation_model_v3.py | 53,262 | 14 Nov, 13:54 | The version 3 build |
| allocation_model_v2.py | 40,785 | 12 Nov, 08:10 | The version 2 build |
| allocation_model.py | 31,771 | 12 Nov, 07:06 | The version 1 build, modified after the scaffold commit |
| forecasting.py | 25,871 | 14 Nov, 16:36 | The forecasting module used for the version 4 family |
| data_loading.py | 1,130 | 1 Nov | Scaffold loader, tracked in git |
| routing_model.py | 1,442 | 1 Nov | Scaffold routing skeleton, never built out |
| __init__.py | 70 | 1 Nov | Package marker |

### 4.2 External data, data/external/ (24 files)

The input tables the model and the audits read. The load bearing ones: faostat_crops_egypt.csv (304,520 bytes, 14 Nov 16:25, with faostat_crops_egypt_PROVENANCE.md beside it), faostat_producer_prices_egypt.csv (59,703), ministry_cost_bulletin_2019_2022.csv (7,645), capmas_governorate_area.csv (23,336), capmas_governorate_production.csv (22,414), capmas_governorate_yield.csv (24,902), capmas_governorate_total_cropped_area.csv (3,644), potato_season_split.csv (14,639), nili_maize_governorate_2020_2021.csv (9,591), nile_inflow_aswan_series.csv (15,541), crop_water_requirements_egypt.csv (4,175), fao33_ky_values.csv (986), production_costs_egypt.csv (3,473), procurement_prices_egypt.csv (1,763), egypt_water_budget_anchors.csv (4,033), pink_sheet_crosscheck.csv (4,399), wapor_aeti_governorate_2018_2025.csv (6,566, 14 Nov 17:01, with WAPOR_METHODS.md), capmas_secondhand_isi_cropped_and_rice_area.csv (1,904), plus the research notes (research_notes_capmas.md, research_notes_hydrology.md, research_notes_prices.md, EXTRACTIONS_1B.md) that record how the tables were found.

### 4.3 Processed outputs, data/processed/ (53 files)

Run logs: run_v1_output.txt, run_v2_output.txt, run_v3_beet795_output.txt, run_v3_beet2400_output.txt, run_v4_main.txt, run_v4_caps.txt, run_v4_beet2400.txt, run_v4_robust.txt, run_v4_1_main.txt (35,442 bytes, 14 Nov 18:01), run_v4_1_caps.txt, run_v4_1_beet2400.txt, run_v4_1_robust.txt, run_forecasting_v4.txt. Saved plans: plan_v4_robust_plan.csv, plan_v4_1_floor50.csv, plan_v4_1_floor60.csv, plan_v4_1_floor70.csv, plan_v4_1_floor75.csv, plan_v4_1_floor80.csv, plan_v4_1_robust_plan.csv, all regenerated at full precision on 14 Nov at 18:07 to 18:08 by plan_precision_recovery.py. Forecast outputs: forecast_prices_yields_v4.csv (1,334) and backtest_scores_v4.csv (10,764). Robustness samples: robustness_samples_v4_1.csv (10,298, 100 rows). Audit work folders: audit_v4_work/ (eight scripts from the version 4 audit) and audit_v4_1_work/ (au.py, nine run scripts named run_*.py, and nine JSON outputs: basics.json, ceilings.json, clearance.json, duals.json, frontier.json, frontier_scaled.json, info_stress.json, penalised.json, robust_numerics.json).

### 4.4 Paper folder, paper/ (20 files)

Nile_Delta_Paper.md (66,269), Nile_Delta_Paper.html (71,737), Nile_Delta_Paper.pdf (114,967, 28 pages), render_paper.py, PAPER_SPEC.md, Audit_Log_Paper.md, Reading_Guide_2026-11-15.md, Results_Note_v1.md to Results_Note_v4_2.md including Results_Note_v3_DataRun.md, Audit_Log_v2.md, Audit_Log_v3.md, Audit_Log_v4.md, Audit_Log_v4_1.md, paper_outline.md. One naming hazard lives here: Nile_Delta_Paper_Sendable.md (6,216 bytes, 14 Nov 06:47) is an earlier and different document, written in the version 3 framing with three inflow states. It is not the current paper and it is not a sendable copy of it.

### 4.5 Documents, docs/ (20 files)

FOUNDATIONS.md (the combined foundation, version 2, that version 4.1 was built to), FOUNDATIONS_v1_preGPT.md, GPT_AUDIT_v3.md, GPT_INDEPENDENT_AUDIT_BRIEF.md, PRIOR_WORK.md, FORECASTING_RESULTS.md, REASSESSMENT_AND_UPGRADE_DESIGN.md, design.md and problem_statement.md from the scaffold, and the handoff package at docs/handoff_2026-11-15/ (eight files, added 15 Nov 15:35). Root level also holds RERUN_CHOICES.md (14 Nov 13:53), the choice sheet the version 4 build answered.

### 4.6 Frozen and raw material

audit_package/ (25 files, all stamped 14 Nov 15:02) is the frozen version 3 audit bundle: the brief, the data foundation, the prior work review, the version 3 code, both version 3 run logs, the version 3 results note and audit log, and a copy of the version 3 era external data. data/raw/ holds ten Our World in Data crop files (12 Nov) from the early data pass and wapor_work/ (the WaPOR zonal script, its run log, the monthly and annual result JSONs and the governorate boundary file). notebooks/01_first_look.ipynb and video/SCRIPT_v3.md complete the tree.

## 5. Access notes

Everything the brief names was present and readable in the local repository: code, source tables, run logs, audit outputs, notes and the paper. The locator in the brief for a copy of the paper on the user own machine was not needed and was not used. The state of any remote copy of this repository could not be checked from here, because the local repository has no remote configured; whether the scaffold copy held elsewhere matches this tree is unverified.

## Appendix: SHA256 hashes of all 173 files

Paths are relative to the repository root. The list excludes the Python virtual environment, the git internals and compiled Python caches.
```
31a227924efa5b076a260be6e04fcffc0cabdd13d922acacfa301a7dd24a86da  .gitignore
183d99d2318afa08fbf785face5acff52faa37f542b6f23a08aad5d4ad7e0c07  README.md
b6d8ea6951ce19fe30408cdcbdeebfb3da2774b495ee5cc6c752cd86ed63d96d  RERUN_CHOICES.md
afb601d38c03fa6636e760fb83c5a3eb1647a140e608714bad988b95199b0e46  audit_package/00_README_START_HERE.md
4604e392189f311551c67a3fe1231b5ceb57359a98fad88ecd756ea5df5e24fb  audit_package/01_AUDIT_BRIEF.md
8c8a973e69121cff14b3c6f385511273859a99c997781ebf7c8e19a33cce2fd8  audit_package/02_DATA_FOUNDATION.md
934b2c2a63718b2e48fc6cca8ca630f2fd0fe544ef207f26398f73db5d161f08  audit_package/03_PRIOR_WORK.md
b6d8ea6951ce19fe30408cdcbdeebfb3da2774b495ee5cc6c752cd86ed63d96d  audit_package/04_RERUN_CHOICES.md
aa154fb2240910e68c807e674598fac66a56465e06f204d518fa010c64a274ba  audit_package/05_MODEL_CODE_v3.py
4b483c54ccbf6c5c76d519c9b387ea20b39338d7d79bb7787a5f97391d392967  audit_package/06_RUN_LOG_beet795.txt
251968848190931274f11597ed770ea4b0393c06b8e490850e9a1128e4c51f8e  audit_package/07_RUN_LOG_beet2400.txt
200420c79f2b36435ce6a9eda26e84567821f10cfb3679e2ca6c2696b13d9615  audit_package/08_RESULTS_NOTE_v3.md
9930b864728766acfb93e866e4f9f234f7b6922dcfde5b8bf90594e3fcb607da  audit_package/09_INTERNAL_AUDIT_LOG_v3.md
b2767a4a35da3392622a2da701fc0c757c02aac629e1e8a884007a60630a9b1f  audit_package/10_PAPER_SPEC.md
a95a09439459f2bfc2170d27a186a8837aa1545a4b43c5d814ab5da3be359855  audit_package/11_RESULTS_NOTE_v2_for_comparison.md
a46c0e13e171be8f262eedd90e2008139c709ffc844d5c611863d41db420280a  audit_package/data_external/capmas_governorate_area.csv
097594f57410f631d3157a7bea93d6d8d779a6e7ce1c498b5833d69ef20c7868  audit_package/data_external/capmas_governorate_production.csv
95b001ff427045641efa7cf1bf175d31c2d526e6fe18a8b97293664fe3d56ed7  audit_package/data_external/capmas_governorate_total_cropped_area.csv
e3232906b3d59e663e47cd736cf7aa599338f17303fdea5bf91f9db0943030c6  audit_package/data_external/capmas_governorate_yield.csv
b491d8625bbe38837f9a5c2785a4e785450f46cc7451360acba0c6bda4f226e7  audit_package/data_external/capmas_secondhand_isi_cropped_and_rice_area.csv
6c8e3b84394819189b48e5ad9183d9b1719459a5b903115eedf8c31f0ccc1d9f  audit_package/data_external/crop_water_requirements_egypt.csv
977cde1ec2c72d8c3d80fa56c5093689b30fda58ae3c02d8548315c278f60126  audit_package/data_external/egypt_water_budget_anchors.csv
fa1d38c1b179fef4200bc2e4562358a67abdb8e5438d28a113b2c605298b548d  audit_package/data_external/fao33_ky_values.csv
ad4fb169ca1f8ac7c991e978471d702cb0fcff7d9337be962c1e3cff2fadecbd  audit_package/data_external/faostat_producer_prices_egypt.csv
b8de53b94307446b1cef30ba866391ad23ae3656baea266dc0edbee1e130f792  audit_package/data_external/nile_inflow_aswan_series.csv
3de42e9c2c630ff7a44ffab4b44da540cdc591e36a5c33153387bd284c9f48c2  audit_package/data_external/pink_sheet_crosscheck.csv
ca972a92fe6df7904b0c74c66900b17df8085ef4548c95f35431d0092e4d6fe5  audit_package/data_external/procurement_prices_egypt.csv
d1b77642225e62be5e3a05f3affde71b352eb0cd649f494618a59b9429983f01  audit_package/data_external/production_costs_egypt.csv
8c8a973e69121cff14b3c6f385511273859a99c997781ebf7c8e19a33cce2fd8  data/DATA_FOUNDATION.md
219c93570e61cab2f56f23ff8088a162747453750863bd9b789686a8cbf78277  data/MINING_SWEEP_2.md
ff23ebf9340dc22b26d176e6a69e670c20b5e6c49e53c0b9ef996455b0d1a9db  data/SOURCES.md
71f6d7a3f91273f183bc2a646bce9ca3a9f6c73493c5d9a80c3579cf79795b48  data/external/EXTRACTIONS_1B.md
a1b04f71e8a669b3cd1c8f820ed003e874306c6d7a1cac2fe16066cba568acb3  data/external/WAPOR_METHODS.md
a46c0e13e171be8f262eedd90e2008139c709ffc844d5c611863d41db420280a  data/external/capmas_governorate_area.csv
097594f57410f631d3157a7bea93d6d8d779a6e7ce1c498b5833d69ef20c7868  data/external/capmas_governorate_production.csv
95b001ff427045641efa7cf1bf175d31c2d526e6fe18a8b97293664fe3d56ed7  data/external/capmas_governorate_total_cropped_area.csv
e3232906b3d59e663e47cd736cf7aa599338f17303fdea5bf91f9db0943030c6  data/external/capmas_governorate_yield.csv
b491d8625bbe38837f9a5c2785a4e785450f46cc7451360acba0c6bda4f226e7  data/external/capmas_secondhand_isi_cropped_and_rice_area.csv
6c8e3b84394819189b48e5ad9183d9b1719459a5b903115eedf8c31f0ccc1d9f  data/external/crop_water_requirements_egypt.csv
977cde1ec2c72d8c3d80fa56c5093689b30fda58ae3c02d8548315c278f60126  data/external/egypt_water_budget_anchors.csv
fa1d38c1b179fef4200bc2e4562358a67abdb8e5438d28a113b2c605298b548d  data/external/fao33_ky_values.csv
6d4e6337c407d1d2e82d3fe1f7b0a8784647509983272161e155c7687d933a05  data/external/faostat_crops_egypt.csv
93157e713115998006b3f1fa2b09fa663f196cf1f355d40d46930ad9b02afd91  data/external/faostat_crops_egypt_PROVENANCE.md
ad4fb169ca1f8ac7c991e978471d702cb0fcff7d9337be962c1e3cff2fadecbd  data/external/faostat_producer_prices_egypt.csv
027934fc659743dc5efe4511f0bf61656beb0677759250d24e5c4fc005aa4b3f  data/external/ministry_cost_bulletin_2019_2022.csv
b8de53b94307446b1cef30ba866391ad23ae3656baea266dc0edbee1e130f792  data/external/nile_inflow_aswan_series.csv
5d480fab00a51572c99e10c0c411e8e5d69a23fcedda49aa061d58a9126976f4  data/external/nili_maize_governorate_2020_2021.csv
3de42e9c2c630ff7a44ffab4b44da540cdc591e36a5c33153387bd284c9f48c2  data/external/pink_sheet_crosscheck.csv
f2c6ae0734d666c972eeae6173b799fac287ae26afa5f3eaa16915ec729255f2  data/external/potato_season_split.csv
ca972a92fe6df7904b0c74c66900b17df8085ef4548c95f35431d0092e4d6fe5  data/external/procurement_prices_egypt.csv
d1b77642225e62be5e3a05f3affde71b352eb0cd649f494618a59b9429983f01  data/external/production_costs_egypt.csv
27f5d15d343a666691caff16f54b5d620ab2b2b590e252ef38d792bf5cd42118  data/external/research_notes_capmas.md
68b4596101dc4842e6db14c0f8bc086641bf89c41692b4cccfc055c653ff6921  data/external/research_notes_hydrology.md
462803a7f958d51417f38bdb8427d5d362bd0daa50b64d7309a973904750bc02  data/external/research_notes_prices.md
638d40891e75dbbb0eacde697ea9847885780dce0bc600c06dedb9f2ecc88fd4  data/external/wapor_aeti_governorate_2018_2025.csv
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  data/processed/.gitkeep
1256fc25b75508d821d2163f66626404bb35d5e603b1e61d9b46ec90d4dc38b6  data/processed/audit_v4_1_work/au.py
9075b22fcff92c5ef1da39a65092425a9969cec2c547856fe61592747f6f7bbc  data/processed/audit_v4_1_work/basics.json
8da995074748296122c5c5161c9b58cbe0ca31a342e09548eab940d2c3e4f369  data/processed/audit_v4_1_work/ceilings.json
05b1c6e0c7db781f8131a635b2610252f60189834b3d02ab4408e62ecd15ad8f  data/processed/audit_v4_1_work/clearance.json
9520c40921cba18338ddc5dd048929d081db217614220e252182f19604228230  data/processed/audit_v4_1_work/duals.json
a8ce73fe7916c08c35d53ef3dccd282d8f7003593cf676af09c0e495c3c7346c  data/processed/audit_v4_1_work/frontier.json
73985615afcb22f891bbef66ad9e84a67b848603f95de5b7dbee26ccc0e34c3b  data/processed/audit_v4_1_work/frontier_scaled.json
abfd3a586928b94683554f03b4239d65ae9c5430ba9051c6b51d10d435976193  data/processed/audit_v4_1_work/info_stress.json
012d7adaf9c3d7293c96e68df7d80679c79674532d1269f9fe3b4f1786257041  data/processed/audit_v4_1_work/penalised.json
a6d0a77167fa461728d28377a69946eec94c13bce0e2fa4d47fb5aeeeba7831f  data/processed/audit_v4_1_work/robust_numerics.json
aab498a2edbfc925634e3109f08cd43ed1410157af8631a59ab3bbd9d5bf1f6d  data/processed/audit_v4_1_work/run_basics.py
93becd71c3328b85e0071d858e9dfe747c7083185bafa13f28b38b9169161aaf  data/processed/audit_v4_1_work/run_ceilings.py
402c8fd2d207ab0c815e3320c422ec079a64cfb25dc1e24242aa1b543b880c14  data/processed/audit_v4_1_work/run_clearance.py
8fcda69c711df28369f622ec799695f29926b085f8580919d25f83a6c433eb80  data/processed/audit_v4_1_work/run_duals.py
0e98e5fd27dae0a263abc6cdc832aa97c331b846d2cdfb7cfbbb7e872e008aa0  data/processed/audit_v4_1_work/run_frontier.py
ab5e8b65db91b2e99c82b8c24f938e93dcd2d31a5920072ae3108e9d7bdb056c  data/processed/audit_v4_1_work/run_frontier_scaled.py
957c1ffd7838de5a707be2e85fd6ea4a9c90f9a350519d07aee1f0eba0e156a8  data/processed/audit_v4_1_work/run_info_stress.py
a58ad821475a3d54acf525a6ddb35b4c63abecdaf455ebba50228ea0f4da5630  data/processed/audit_v4_1_work/run_penalised.py
77fb9ee13fc0793f0b47148c826fbb5a38ba864799f013012c836e758ebef179  data/processed/audit_v4_1_work/run_robust_numerics.py
627e8c2c901f49f4553ba77341e32e4d9e24a67034f0b620d9a4cb28d6482e63  data/processed/audit_v4_work/audit_load.py
ad83bed0f59f5ef5fd275f7bedf38427e11427b1b21695a32941754603ac3065  data/processed/audit_v4_work/audit_model.py
ec7c3684b3cbbedbdc10b336c643ab65bdbfcf322a03b951112205cd3fce8e1c  data/processed/audit_v4_work/run_baseline_diag.py
f3d6bf1b11fc845fea39b57c072fb0963ca3371bc69afe8d72c181809528208f  data/processed/audit_v4_work/run_baseline_diag2.py
a3555f8b38dd15aed4f7d81abb5c9456f356d980d7c52454187add49c385341b  data/processed/audit_v4_work/run_ceiling.py
93c94f514e4a2b5517182bd77602ba6d661319114bab6204163b4c98fb30adf5  data/processed/audit_v4_work/run_ev_robust.py
4865a1f6ce2b47f29a8af538b68b33de20d9471883e92c0c96310710bb8bd32a  data/processed/audit_v4_work/run_frontier.py
edb4468fe9dab6666cad33a139694832d631db1e67ede6715c2c9ac4b5f8316b  data/processed/audit_v4_work/run_info.py
9c85bc4fe45428180c2c8871955874123724315c81d8e6d9c6300a1423961a4d  data/processed/audit_v4_work/run_misc.py
a6d4f61f69f9989f9cadb896e377cc68ce04acd3dbf1e50cb3c896bcef12828c  data/processed/backtest_scores_v4.csv
6a24554e9e0154b49c0a0a4a6ba6b4fc4ca4aa6ad676769623b2a7565f37c7d1  data/processed/forecast_prices_yields_v4.csv
80a49ebff522f1f0371be39b552af0089d0c7e8d5c41ed5c1fa9ce8dbd105672  data/processed/plan_precision_recovery.py
1e28478342be5ba2870b4043356e91bb89bccb7571f91ed3c0d1b16c2f970e49  data/processed/plan_v4_1_floor50.csv
137c0b4d3d6595994a2c01257f82ec40a723055773efef187ef5c8e6c0a63633  data/processed/plan_v4_1_floor60.csv
ecbba0460b73f866b613ba460435076ccecb7276dc26478039071cab57f11f35  data/processed/plan_v4_1_floor70.csv
e55b91097a2f7719f20847039f69ba36363e86bd6b5c39184d90556e83220a3c  data/processed/plan_v4_1_floor75.csv
c2b831b1179377c95f088fb934e97e77f40a16918e817e17fd105d40fa47847a  data/processed/plan_v4_1_floor80.csv
c2b831b1179377c95f088fb934e97e77f40a16918e817e17fd105d40fa47847a  data/processed/plan_v4_1_robust_plan.csv
9667827b4a96f2869db900f31276aca9de8a752613b7fdca089cd0f2970f5731  data/processed/plan_v4_robust_plan.csv
5e83a5314aa7a76bcff45c1890a163f4452ab5b9038efb74d29acf4992d2bdeb  data/processed/robustness_samples_v4_1.csv
31e518e6845132dea39e2b5a052c2a7c2082e172d9d54eba9c5484e698543c74  data/processed/run_forecasting_v4.txt
39079d1fd3ad0d7d9a1a301fd78528060226706757c937a2c60b9eccf243979c  data/processed/run_v1_output.txt
36dc0c68bbfbd313f4b941ff2abf7a84748b730b351b02e45312cce479c8d4d2  data/processed/run_v2_output.txt
251968848190931274f11597ed770ea4b0393c06b8e490850e9a1128e4c51f8e  data/processed/run_v3_beet2400_output.txt
4b483c54ccbf6c5c76d519c9b387ea20b39338d7d79bb7787a5f97391d392967  data/processed/run_v3_beet795_output.txt
ec4ba3f8d15bd101e5598f4a273c746fe389506bf8b7e7bfaf9e8ada704f2cfa  data/processed/run_v4_1_beet2400.txt
73fdbf5337dd82a707c7cb552fd132b53dd093e710950b4c6244a94739aa2ea8  data/processed/run_v4_1_caps.txt
8df03c60b5113c8fb2f78793741ef698cf14f4a29e401235c88e44ff8c899e92  data/processed/run_v4_1_main.txt
1c0028e9e950d9a5d1049feb4012c016a16deda630c93233af8100024e0470e7  data/processed/run_v4_1_robust.txt
a37be3778803b3186d3cee14a7ef59e47ccc6c11e9a13f761171838c3404a066  data/processed/run_v4_beet2400.txt
b574a1c37ec7f119195f6268d296d6dc80d05e189dc0b28ea5d5f6d85c69108d  data/processed/run_v4_caps.txt
5feb64deb8dbeb53bfb525dd51b844b53b76268b404747576483a6c3e3739f3f  data/processed/run_v4_main.txt
36e8544118e49f24e710f2d2569eda3a237079a4beba66487f8d8c486ef8322a  data/processed/run_v4_robust.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  data/raw/.gitkeep
6f30eebe8dd2f9ec8c58c6c89728a2ccdf34014441264954a8fd571fd631b407  data/raw/owid_maize-production.csv
b0d59dd2a824f4cccd8eaaae91e402bd83b8853cd65a3063363c11409902d192  data/raw/owid_maize-yields.csv
15af73801294a5fec25e57bd4674450724319bfbd5865dc6415279c325c0fa4d  data/raw/owid_potato-production.csv
0bd7f1f21cb7cbdafcaec51cfff25b296fc1db23262f42ba16cd393c5e706313  data/raw/owid_potato-yields.csv
1a5c9e70644e8067fba9728b28b09c23466f8c178f9a0ca6d1cdaac4f1a3ad1d  data/raw/owid_rice-production.csv
0bd0a02138dc147b06cb49865271e4aac14963284f5cfd5066f11277e72e87ed  data/raw/owid_rice-yields.csv
aaaf4d50e2fa2b68a2d270d8125a7e13b0defb559f0900180e947523c0534f6d  data/raw/owid_sugar-beet-production.csv
70f31985fb8f67d3c7c5abc1642ee463b29fa8c0c58d5b2326217ee64bd512c5  data/raw/owid_sugar-beet-yields.csv
d3dfeb8bc4272fd1a6c85bc96435d23ec848720d3513e08aa468abfb327ccd6c  data/raw/owid_wheat-production.csv
511cca58ee7e657e38f9880106ca74f3c352d953b9ef813cc41874e04173cb68  data/raw/owid_wheat-yields.csv
5d433be32968207703cf8aec66b22b6c2973a93208d22feea873b920cb999343  data/raw/wapor_work/annual_results.json
d55fe552bb2c426f49e5fcec850b17e541bce684f11508d148988bfc6e7de196  data/raw/wapor_work/egy_admin1.geojson
011ac425f11d26fee4bdbfec1aa066a32111d015a40b604908837af29e2e627a  data/raw/wapor_work/monthly_results.json
8bc8f7b3322e491a2f6fc490af1986bc69790c54fe2068c1930bc729e11bdf86  data/raw/wapor_work/run.log
eed9c3e3c59d7b376b525a0102415d318dbdfdc02b885bcfa00738ea3a1482ae  data/raw/wapor_work/wapor_zonal.py
680b3e2b211633c59f8683340f2d9ffbf201492fe91a4a3e363b7e4c96d1bb61  docs/FORECASTING_RESULTS.md
1b8516ed46f9c90e00a36c4ed5a2bf70409a48331cc24a206e0f6b647ed24436  docs/FOUNDATIONS.md
ee1737086040702f17bdd1faaf71b059cd8fd32ab89063d742d440fab058857e  docs/FOUNDATIONS_v1_preGPT.md
67c4706ddd79131fe88eb8bd84635e8fb6aad81c2256272b01c4e50f0fd60b8b  docs/GPT_AUDIT_v3.md
4604e392189f311551c67a3fe1231b5ceb57359a98fad88ecd756ea5df5e24fb  docs/GPT_INDEPENDENT_AUDIT_BRIEF.md
934b2c2a63718b2e48fc6cca8ca630f2fd0fe544ef207f26398f73db5d161f08  docs/PRIOR_WORK.md
59107e22c93e8be310d31142f27fdf23a15c943af6f8cde3cf9998474675d04a  docs/REASSESSMENT_AND_UPGRADE_DESIGN.md
f92e0fc09fef5582fcf1e45f9c19649b0fdbb5024bdb30e449b95f69d6e496a1  docs/design.md
49504bc5414b35baa77d7505958eae2ef23c71c720ef691860efb22d3887d168  docs/handoff_2026-11-15/acceptance-tests.md
f138491ac254f3294330397ec87b52888ea0f93cbbca62c2791314ea5cb10d61  docs/handoff_2026-11-15/builder-brief.md
939bfc657322a98529fb3bff1aa0256f8eedc1ea3d7c4e3836cc469f46002fdb  docs/handoff_2026-11-15/critic-brief.md
0bd529fe6a5c7f4c38a36382346b1f6e85b543429df2a63e14a1856deebeb6a3  docs/handoff_2026-11-15/eval-cases.json
b557090716a22866e007e7ec8c20364298e8deafef6dce81e31ceedd111cb0db  docs/handoff_2026-11-15/evaluation-report.md
024c66d53f3d2ee150d3f4ab4cb36374459531c3bffd1deb13dd677f7d08cbf8  docs/handoff_2026-11-15/source-register.md
d9a70b36b27bea1860036e8d4ecad2fe0672b3b07479416522ee73c359b90e74  docs/handoff_2026-11-15/stages.json
1f3356b625d7c815abf40bb5e64e0277896896682a072b7c3d5474490f9f9b4a  docs/handoff_2026-11-15/workflow-spec.md
5d147b16bcefc5f41292a0ecc6d8ab451a43d3dc65375d582c8f98185279fe5d  docs/problem_statement.md
61ca60d22c0b16313caf66bbce17c6ee595a225e6f22f87d25892af61c062305  notebooks/01_first_look.ipynb
64f1853558880aa33c2a6efb6293ffa51783694cb12e63050b03cdea54e40ad9  paper/Audit_Log_Paper.md
1d579bc5596f4c0ba6c0115dd5636f97b96f00d9dc70a215abebbc2c0bf28df0  paper/Audit_Log_v2.md
9930b864728766acfb93e866e4f9f234f7b6922dcfde5b8bf90594e3fcb607da  paper/Audit_Log_v3.md
bfb92e3257fbe9c84cfe6f9de21a51e5eaa9337ffdac09dc1cc4fa38f7934eb0  paper/Audit_Log_v4.md
af9b25ceecbf01c7c49a7b25feb1751ce09eb2fee08e30574bf22f653528e726  paper/Audit_Log_v4_1.md
c47a33d7bec8cc7add4d504e5d27e2a6c9546af3e9a76e871ada74f78ca732ee  paper/Nile_Delta_Paper.html
91b4ece1173e339339b8d99c375ec2e71b24ea5802ab54837b040cdbf2936a5b  paper/Nile_Delta_Paper.md
193809746f93f51f9477735dad37d45f85d8ca5e671a4d3967247cd2052d6f09  paper/Nile_Delta_Paper.pdf
f5892703d99753ea2104fb7b03a969141ec1e2808e293ea2de5fe74dac28abc8  paper/Nile_Delta_Paper_Sendable.md
b2767a4a35da3392622a2da701fc0c757c02aac629e1e8a884007a60630a9b1f  paper/PAPER_SPEC.md
db59a168fe1e707af64db87ec6431c2c1a0a36a496c61b9fbe3a7e6f329e126a  paper/Reading_Guide_2026-11-15.md
476d3f3bd34e50cd1fcb43d402c5716d6b871cf28487366b885f28990042a2ad  paper/Results_Note_v1.md
a95a09439459f2bfc2170d27a186a8837aa1545a4b43c5d814ab5da3be359855  paper/Results_Note_v2.md
2b9e1baf78bd73a6b8e2eba369e43bf66b21c4e6880145e0963888a19d6af1ac  paper/Results_Note_v3.md
200420c79f2b36435ce6a9eda26e84567821f10cfb3679e2ca6c2696b13d9615  paper/Results_Note_v3_DataRun.md
11d11fcdcb8598fe6eb520fa5ab34097d01451f29e76751eeea30e61820ef78d  paper/Results_Note_v4.md
f2800e3ef9c854129c428561251652e4f40e525c551a7091e0582ad821f1225e  paper/Results_Note_v4_1.md
cef1ab71c52b8f1ab158c6e26d8b704b72b415b147b272b1c6ffb02c74fd0b69  paper/Results_Note_v4_2.md
befcc37e572a32ba845e1026f1ac5dd7a46bbe7a4785f473a415695f258bd231  paper/paper_outline.md
a15ee93f4696f7e3588a517202b0b5a53adac7831080bbbc0b7db1a110540cfb  paper/render_paper.py
6e2b7f13a1b8b6480616a4e32319acd4d79fe03697d58119396a9dbba44596ed  requirements.txt
e20759d5115c624bc8d5bd113d94b42ecdcca1b87a4e7ba70cadb319c1da1fb4  src/__init__.py
ae9d352f0cc03277bf7ed2bd1a1575aeb18d6c10cb71b3e733a62ad58f343454  src/allocation_model.py
a61e9cca1f9353d745fe36b609df82b20708a6231ed11119343ecb3d39d03ae7  src/allocation_model_v2.py
aa154fb2240910e68c807e674598fac66a56465e06f204d518fa010c64a274ba  src/allocation_model_v3.py
541ace3c7b04ea3541d686b57530c51df8d4702235a968d71b8934308dde710a  src/allocation_model_v4.py
adeb2b183d25016172521f1e60362f25d5e073c92f145969f2b3e8e2d9a577e8  src/allocation_model_v4_1.py
2a41de3d5d87d00c1a07b079f4b0d49f418af5ff331698c54ca18388fcf1c54d  src/data_loading.py
6cb970e52880110aff73f1b202986d223ac9bd6d74377697029589ebf4a41fb5  src/forecasting.py
df48f91eda49e88178064e964fcf6de151aa5c93f6941a0c62a8f63dd42eafe2  src/routing_model.py
39ee0932c1747506e4cb7919a954f068e0f567f642db14761377dc702adf2396  video/SCRIPT_v3.md
```
