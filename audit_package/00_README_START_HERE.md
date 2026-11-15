# Start here: the full audit package

This package contains everything an independent auditor needs to assess the Nile Delta water allocation project, version 3. The brief alone, sent without these files, cannot be audited, which is why this package exists.

## How to use it

Option A, one upload: upload the zip file Nile_Audit_Package_v3.zip and let the model open it.
Option B, file by file: upload the numbered files in order, 01 to 11, plus the data_external folder contents.
Option C, one document: upload Nile_Audit_Package_v3_COMBINED.md, which holds the full text of files 01 to 11 and every CSV in one file.

Then paste the opening prompt below.

## Opening prompt, paste this with the files

Act as an MIT professor and data analytics PhD holder. Examine and assess this project with high human judgement. The file 01_AUDIT_BRIEF.md gives you the whole project objectives, the materials, the eight checks to run, and the exact report format to follow. Work only from the files in this package. Read them in numbered order. Replay the arithmetic yourself from the run logs, 06 and 07. Trace parameters back to 02_DATA_FOUNDATION.md and the CSV files. Treat 09_INTERNAL_AUDIT_LOG_v3.md as a claim to test, not as evidence. Where the package does not let you verify something, say so and name what you would need. Follow the brief's report order: verdict first, then errors largest first, then claims that survive, claims that shrink, claims that must be withdrawn, the three changes that would most raise the paper's quality, and anything unverifiable.

## What each file is

01_AUDIT_BRIEF.md: the audit instructions, the project objectives, the eight checks, the report format.
02_DATA_FOUNDATION.md: every parameter, its source, its years, and the named gap list. The only permitted source of parameters.
03_PRIOR_WORK.md: the map of about 45 published works and the positioning the project claims.
04_RERUN_CHOICES.md: every modelling choice in the version 3 run, each tied to a foundation section.
05_MODEL_CODE_v3.py: the model code, 1,171 lines.
06_RUN_LOG_beet795.txt: the full run log with sugar beet at the farm gate price of 795 Egyptian pounds per tonne.
07_RUN_LOG_beet2400.txt: the full run log with sugar beet at the factory procurement price of 2,400.
08_RESULTS_NOTE_v3.md: the factual results record written from those logs.
09_INTERNAL_AUDIT_LOG_v3.md: the internal audit of the rerun. A claim to test, not evidence.
10_PAPER_SPEC.md: the specification the eventual academic paper must meet.
11_RESULTS_NOTE_v2_for_comparison.md: the version 2 results record, so the version 3 comparison and the gain decomposition can be checked.
data_external: the 13 source CSV files behind the foundation, including the FAOSTAT price series 1991 to 2023, the governorate area, production and yield panels, the production costs, the water requirements, the yield response factors, and the hundred year Aswan inflow series.
