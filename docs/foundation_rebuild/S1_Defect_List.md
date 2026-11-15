# S1 Defect List: traceability defects only, in priority order

Written 15 November 2026 under Stage S1. Every item below rests on files on disk: a missing trail, a version ambiguity, or a clash between two saved statements. Model quality questions that need a rerun or a domain judgment are out of scope here and belong to S3 and S4. Nothing in this list was fixed. One apparent defect was tested and cleared, and it is recorded at the end so that later stages do not chase it.

## Item 1. The historical pattern sentence clashes with the pattern own worst scenario figure

Evidence. Paper Section 6.2 prints three saved values for the historical planting pattern: expected staple tonnage of 8,908,274 tonnes (72.69 percent of the reference), worst scenario tonnage of 7,367,358 tonnes (60.12 percent), and the sentence that inside this model the pattern holds no guarantee at any level on the ladder. The lowest ladder level is 50 percent, a floor tonnage of 6,127,204 tonnes. The pattern worst scenario value sits above that floor tonnage. No saved output on disk shows the pattern evaluated scenario by scenario against the floor, and no saved output records a feasibility failure for the pattern that would explain the sentence. The run log baseline section (run_v4_1_main.txt) prints only the expected and minimum tonnage and the margin.

Consequence. A checker who compares the two printed numbers reads the benchmark sentence as false, and the benchmark carries the paper central contrast between the present pattern and a priced guarantee. Until the definitions are reconciled in code and in unrounded output, the sentence should be treated as unproven. The handoff acceptance test A07 and eval case E03 target exactly this point. Evidence needed: the per scenario staple tonnage of the fixed pattern, its water feasibility per scenario under the model budgets, and the exact definition of holds that the build applied to it.

## Item 2. The reaudit predates the final saved form of the code it audits

Evidence. The reaudit artefacts in data/processed/audit_v4_1_work/ are stamped 14 November 2026 at 17:47 to 17:52, and paper/Audit_Log_v4_1.md at 17:56. The code file they audit, src/allocation_model_v4_1.py, is stamped 18:00, and the surviving author run logs are stamped 18:01 to 18:02. Results_Note_v4_1.md, stamped 17:44, was written from a version 4.1 run whose own log does not survive on disk; the log on disk is the later 18:01 run.

Consequence. The audit chain proves that an independent rebuild agrees numerically with the printed results. It cannot prove that the saved code file is the exact code the audit executed, because the file was saved after the audit closed. Any future dispute about what was audited has no hash, commit or preserved log to settle it. Evidence needed: none recoverable for the past run; the repair is procedural, at the next build, by hashing and committing the code before the audit runs.

## Item 3. No version control covers any work after the scaffold

Evidence. Git holds one commit, a6dc190 of 1 November 2026, tracking 15 scaffold files. No remote is configured. All model versions 2 to 4.1, all data tables built after 1 November, all run outputs, all audits and the paper are uncommitted working tree files. The root README still describes the scaffold.

Consequence. There is no independent record of what any file contained at any past moment, and any file can change without leaving a trace. Every version claim in the project, including the claim that version 4 is kept unchanged on disk, rests on timestamps and internal labels alone. This weakens each other item in this list, because none of the trails can be anchored to a fixed state. Evidence needed: a commit of the current tree with the hashes in S1_Inventory.md, taken before S2 changes anything.

## Item 4. The paper data appendix documents one yield fill; the code fills twelve cells

Evidence. The model code (src/allocation_model_v4_1.py, the fill block at lines 244 to 259) fills any blank district yield with the area weighted mean of the published yields for that crop, and the run log prints the fills at lines 83 to 95 of run_v4_1_main.txt: rice in Menoufia at 9.138 tonnes per hectare, Nili maize in four governorates at 8.358, and Nili potatoes in seven governorates at 18.120. The paper Appendix A documents only the Menoufia rice fill, in its Menoufia rice fill row and in the reference tonnage notes. The Nili fills are nowhere in the paper.

Consequence. A reader who rebuilds the parameter set from the appendix alone uses unpublished values for Nili yields in up to seven governorates without knowing it, and cannot reproduce the model inputs. The gap is documentation, not concealment: the code states the rule and the log prints every fill. Evidence needed: the full fill list carried into the paper data appendix or into a parameter file the appendix cites.

## Item 5. The clearance sentence is exact in print and approximate in the saved unrounded output

Evidence. Paper Section 6.1 states that at every floor level the smallest headroom above the floor is zero tonnes, a four way tie across the low layer in all four inflow states. The audit clearance.json gives unrounded headrooms for the saved plans: at floor 50 the four low layer cells sit at 0.045, 0.029, 0.095 and 0.048 tonnes; at floors 60 to 80 the minimum headroom in the audit cell bound evaluation is slightly below zero, down to 0.052 tonnes below zero at floor 80. The run log prints these as 0.0 tonnes.

Consequence. The sentence is true at whole tonne print precision and false as an exact statement. The size is immaterial (hundredths of a tonne against millions), but the paper elsewhere corrects one pound errors, so its own standard makes this worth aligning: the sentence should claim tightness within a stated tolerance, not exact zero. Evidence needed: a single clearance evaluation, on the record, whose unrounded output the sentence can cite word for word.

## Item 6. One frontier step cost in the raw run log disagrees with the paper by one pound

Evidence. The frontier table in run_v4_1_main.txt prints the 80 percent step cost as 27,839,856,443 pounds. Subtraction on the log own printed margins (202,983,384,826 minus 175,143,528,384) gives 27,839,856,442, which is the value Results_Note_v4_2.md and the paper print. The audit log records the same class of slip at both the 60 and 80 percent steps in the earlier note, in opposite directions, and the correction note repaired them.

Consequence. Anyone tracing the paper to the raw log alone finds a mismatch and cannot tell which side is right without reading the correction note. The paper value is the correct arithmetic; the trail to it runs through two note versions. Evidence needed: none for the value; the log should be annotated or superseded so the first trail a checker follows is the corrected one.

## Item 7. One audit output file carries stray penalised fields that contradict the file that holds the values

Evidence. Audit info_stress.json contains the fields penalised_eev at 0.0 and penalised_vss_mine at 175,143,528,383.63, which is the recourse value, not a penalised value. The penalised values the paper prints (penalised expected result 167,535,664,790 pounds; penalised value of the stochastic solution 7,607,863,594 pounds) live in audit penalised.json, at unrounded 167,535,664,789.85 and 7,607,863,593.78, and they check against the run log.

Consequence. A tracer who opens info_stress.json first, which is the natural file for information values, concludes that the penalised figure has no audit support or that the audit failed to compute it. The support exists, one file over. Evidence needed: none for the values; the stray fields should be struck or the file annotated at the next build.

## Item 8. One member of the ceiling band rests on the audit side alone

Evidence. The ceiling of 80.12 percent under the uncapped proportional reserve split appears in the paper Section 6.1 and Appendix D. No author run log on disk prints it: run_v4_1_main.txt prints the primary ceiling, the no reserve bound and the scaled yields sensitivity only. The value traces to audit ceilings.json (uncapped_proportional at 9,818,690.3 tonnes, 80.1237 percent) and to the replay text in Audit_Log_v4_1.md.

Consequence. The band is presented as one family of results, but one member has no author side run behind it. If the audit file were lost, that member would become a prose only claim. Evidence needed: an author side run of the uncapped variant saved with the other ceiling runs, or a sentence in the paper that credits the figure to the reaudit.

## Item 9. A superseded document in the paper folder carries a name close to the current paper

Evidence. paper/Nile_Delta_Paper_Sendable.md (6,216 bytes, 14 November 2026 at 06:47) is an earlier, shorter document in the version 3 framing: three inflow states, a different title, and results the current paper replaced. Its name invites confusion with paper/Nile_Delta_Paper.md.

Consequence. The wrong file can be sent, cited or audited against the current claims. Evidence needed: a rename or a move to an archive folder, with the inventory hash list updated to match.

## Item 10. The author frontier survives only as whole pound prints

Evidence. The author run log prints frontier margins rounded to whole pounds. No author side file holds the frontier in unrounded form. Unrounded frontier values exist only in the audit outputs (frontier.json and frontier_scaled.json), where they agree with the prints.

Consequence. Exact reproduction of the headline margins depends on the audit rebuild rather than on the author own saved outputs. Combined with Item 2, the strongest form of the trail (author code, author unrounded output, independent check) is not available for the central table of the paper. Evidence needed: at the next build, the model should write its headline results to a structured unrounded file as part of the run.

## Tested and cleared: the audit frontier gap at 50 and 80 percent is a scaling effect, not an error

The audit frontier.json solves sit below the printed margins by 7,713,181 pounds at floor 50 and by 325,601 pounds at floor 80, while matching at 0, 60, 70 and 75 percent. Audit_Log_v4_1.md records the cause: the audit unscaled cubic metre formulation returns slightly lower optima at those two levels, and its scaled formulation, saved in frontier_scaled.json, reproduces both printed margins to the pound (297,739,198,931.58 and 175,143,528,383.63 unrounded). The printed values stand. The scaling sensitivity itself is worth S4 attention, because a solver result that moves with unit scaling at two of six levels is a property a checker may probe; but as a traceability matter the trail is complete and explained on disk.
