# Independent Check 2: a domain critique of the Nile Delta paper

Written cold, as if the paper had arrived on my desk from an author I do not know. Basis: paper/Nile_Delta_Paper.md in full, docs/FOUNDATIONS.md, and the code in src/allocation_model_v4_1.py and src/forecasting.py. No audit file was opened before these findings were written. The comparison with the earlier audits sits in the final section, added after they were read.

## What is genuinely strong

Fairness first, because this paper earns it in places most student work does not.

1. The guarantee is defined in the exact words the model uses, aggregate wheat, paddy rice and summer maize tonnage, held in every scenario, and the paper repeats what the floor does not protect until the reader cannot miss it.
2. The ceiling is printed as a band with its conditions, never as a physical fact about the Delta. That single discipline puts the paper ahead of most published work in this field.
3. The forecast failure is printed, not buried. No learning model beat a drift line on prices, and the paper says so in its own abstract level summary and builds its scenarios from measured errors anyway.
4. Abandonment is a real decision with sunk cost, land binds by season against physical area, late planting is charged at inflow probabilities, and planting respects what is known at each decision date. The stochastic structure is built correctly.
5. Stress results always pair capacity with choice. The sentence that a reader who reports only one of the two numbers misleads is exactly right.
6. The dual values carry their own warning about non uniqueness, with a concrete counterexample value from a second optimal solution. Almost nobody at this level does that.
7. The Arabic source work is real. The ministry cost bulletin found under its Arabic title is the kind of find that changes a project's data quality, and the paper is honest that no official cost table exists after 2022.

None of what follows cancels these strengths. The findings below are the places where a skeptical reader stops believing, in the order a referee would meet them.

## 1. Physical coherence

### 1.1 Seasonal pools against the real crop calendar

Verdict: a standard approximation, used silently, with a bounded cost.

The model gives each season its own land pool, and each pool binds at physical area minus its reserve. Inside a season that is correct. Across seasons it is not quite the calendar. Nili maize and Nili potatoes are sown in July and August, while summer crops, rice above all, still stand until September and October. Summer potatoes are planted in January and February, while wheat and beet still stand, yet they sit in the summer pool. So in the overlap windows the model can commit the same hectare twice: once to a standing summer crop and once to the Nili crop that in the field must wait for that land or take other land. The exposure is bounded by the Nili and summer potato areas, which are small against 1.68 million hectares, so no headline plausibly turns on it. But the paper never names the approximation, and a paper this careful about land should.

Smallest supported correction: one paragraph in Section 5 or Appendix C naming the overlap approximation, with the combined observed area of the Nili activities and summer potatoes printed as its bound.

### 1.2 The reserve for unmodeled crops, and the 30,136 hectares

Verdict: internally consistent, built on one untested assumption, and the sensitivity offered does not test that assumption.

The reserve takes each governorate's annual unmodeled area and splits it across the three season pools in proportion to the observed modeled area of each pool, then caps each pool reserve at the free land of that pool. The cap writes off 30,136 hectares of unmodeled area, which receives no seasonal home. The paper discloses the write off plainly, and that disclosure is to its credit.

The problem is the split. Splitting by modeled shares assumes unmodeled crops follow the modeled seasonal shape. They do not. The largest unmodeled crop in the Delta is berseem clover, a purely winter crop that occupies a very large share of winter land. A season true split would put more of the unmodeled area into the winter pool and less into summer than the proportional rule does. The winter reserve is therefore plausibly too small, and the winter pool, the pool that binds in all eight governorates at the ceiling, is plausibly too generous. The sensitivity in Appendix D compares the capped split with the uncapped split and finds the ceiling barely moves, 80.25 against 80.12 percent. But both constructions share the same proportional split, so the test varies the cap and never touches the assumption that matters.

Smallest supported correction: one alternative run with a winter heavy split of the unmodeled area, built from the bulletin's own seasonal totals where they exist, with the ceiling and the 80 percent rung repriced under it. If the ceiling holds, the paper's most exposed construction becomes a tested one.

### 1.3 The water boundary, and what WaPOR is asked to prove

Verdict: the paper uses WaPOR at the right weight; the foundations document promises more than the build does; and the check itself proves less than the word validation suggests.

The model's water charges are applied duties, water delivered to the field. Its budgets are a calibrated total for the model area. WaPOR measures actual evapotranspiration over all surfaces inside each governorate polygon, with no cropland mask, so its total covers cities, water bodies, drains and every crop, modeled or not. The paper compares the two only as an order check, modeled demand of 16.398 billion cubic metres below the WaPOR mean of 24.416 in every governorate, and derives no calibration from it. That restraint is correct. But an order check of this kind is close to guaranteed to pass, since the WaPOR total counts far more surface than the five modeled crops occupy. It rules out a gross scaling error and nothing finer. Calling it a validation role in Section 3 slightly overstates what was validated.

The foundations document, Section 3, says the satellite product calibrates the water side of the allocation model. The build performs no calibration at all. One of the two documents misdescribes the project a reader is being asked to trust.

Smallest supported correction: change the foundations wording from calibration to validation, and in the paper call the WaPOR comparison a scale check. No computation needs to change.

### 1.4 The calibrated budget and the land share split

Verdict: the most consequential physical choice in the paper, and the least examined.

Every governorate budget in every state is the calibrated anchor of 11.00 billion cubic metres, scaled by the state ratio and split among governorates by physical cultivated area share. Two consequences follow, and the paper interprets neither. First, every governorate receives exactly the same water per hectare in a given state, so the district water values of Section 6.5 differ only because crop mix and yields differ, never because supply geography differs. A tail end district and a head district are given identical endowments per hectare, and the dual table is then read as a scarcity map. Second, the entire feasibility story, the ceiling, the ladder, the stress pairs, scales with an anchor that no source publishes and the paper labels a calibration. The stress runs scale all budgets to 0.90 and 0.80, but they report capacity and choice only. The ladder and the ceiling are never repriced at a scaled anchor. The one sensitivity a decision maker most needs, what the promise costs if the true Delta budget is ten percent lower or higher than the calibration, does not exist in the paper.

Smallest supported correction: rerun the frontier and the ceiling at anchor scales of 0.90 and 1.10 and print the two ladders beside the primary one in Appendix D. The machinery already exists in the stress code path.

## 2. Economic coherence

### 2.1 Forecast 2024 prices with official 2022 costs

Verdict: disclosed honestly, bounded nowhere, and biased in a known direction.

Every margin in the paper is revenue at a forecast 2024 price level minus cost at official 2022 nominal values, in a country that passed through very high inflation between those two years. Revenues are stated in 2024 pounds and costs in 2022 pounds. The result is that every margin is overstated, and the overstatement is largest in absolute terms for the highest cost crops, which are the potatoes that drive the frontier. The paper states the mixed basis in the abstract, in Section 3 and again in the limits, and that candour is real. But stating a bias is not bounding it. The foundations document set the rule for stale inputs: forecast them with printed errors, or carry them as a named gap with the cost of the gap stated. The paper names the cost gap and never states its cost. No run anywhere in the paper reprices the ladder with costs carried to 2024.

Smallest supported correction: one frontier run with all costs scaled by an official price index from 2022 to 2024, printed beside the primary ladder. If the rung prices survive in ranking, the paper is stronger for having shown it. If they do not, the reader was owed the run.

### 2.2 Fixed prices and the potato frontier

Verdict: the warning is exemplary and the headline still belongs to the relaxed run.

Section 6.3 tells the reader, in plain words, that the free model plants Nili potatoes at 366 times their observed area and that no market would absorb it. The limits repeat the warning. This is more honesty than the published literature usually offers. And still: the abstract's headline, the 227,935,234,023 pounds cost of holding the 80 percent guarantee, is measured against that same impossible potato plan. The capped run, with named rotation and market shares, exists in the project, and Appendix D reports its ceiling, 77.44 percent. Its price list is never printed. So the paper's central product, the priced ladder of the guarantee, is available only for the world the paper itself says no one should believe, and unavailable for the market sane world the caps describe. A reader who accepts the paper's own warning is left with no ladder at all.

Smallest supported correction: print the capped frontier, margins and rung costs, in Section 6.1 beside the relaxed ladder, or promote the capped run to primary and demote the relaxed run to a diagnostic. Either repair is one table.

### 2.3 Price concepts: beet gets a variant, wheat does not

Verdict: asymmetric treatment, and the asymmetry sits on the crop that matters most.

The primary run pays sugar beet at its forecast farm gate price, and Section 6.8 then reruns the frontier at the documented factory procurement price of 2,400 pounds per tonne, showing nothing changes because the model plants no beet at either price. Wheat receives no such treatment. The model pays wheat at a forecast farm gate price of 10,296.94 pounds per tonne. The paper's own Appendix A documents the wheat procurement price for the 2025 harvest at 14,667 pounds per tonne, about 42 percent higher, under a system in which the state procures a large share of the wheat crop at announced prices. A guarantee whose reference tonnage is more than a third wheat is priced throughout with wheat paid well below the price the procurement system actually offers for it. That overstates the cost of every rung, by an amount the paper never measures, while the beet variant measures an effect the paper itself shows is zero.

Smallest supported correction: run the frontier once with wheat at the documented procurement price, exactly as was done for beet, and report the change in the rung costs in Section 6.8 or beside the ladder.

## 3. Information timing

### 3.1 Planting decisions

Verdict: correct, and correctly described.

Winter planting is a single decision across all twelve scenarios. Late planting varies by inflow state only and never sees the price and yield layer. Late planting costs are charged with the inflow state probabilities, winter costs at weight one. I checked the code on each of these points. This is the part of the design a referee probes first, and it holds.

### 3.2 Water allocation sees the yield layer

Verdict: a mild leak of future information, defensible in substance, nowhere acknowledged.

Served area and water are chosen separately in each of the twelve scenarios, so irrigation responds not only to the inflow state, which a farmer does learn in season, but also to the price and yield layer, including the exogenous yield shock that in the field is known only at harvest. Mid season irrigation does respond to the observed state of the crop, so a defender can justify part of this. But the layer is a whole season outcome, and letting water chase it gives every plan a within season foresight no irrigator has. The paper, which is scrupulous about planting timing, says nothing about this choice.

Smallest supported correction: one sentence in Section 5 stating that water and abandonment respond to the full scenario, with the within season adaptation reading offered as the justification. A variant tying water to the inflow state alone would bound the effect, but the sentence alone removes the silence.

### 3.3 Winter planting treated as blind

Verdict: a conservative simplification that the paper never defends.

The model fixes winter planting before the year type is known. In Egypt the flood season has passed by October and the supply position of the coming year is broadly known before winter sowing begins. Farmers and the ministry alike go into the winter season with a fair reading of the year. Treating winter planting as fully blind costs the plan information it would really hold, and it slightly inflates the measured value of planning stochastically at all. The direction is conservative, which is the safe direction, but a foundations document that argues the two decision points from the field calendar should argue this one too.

Smallest supported correction: two or three sentences in the foundations and the paper tying each decision point to the release and sowing calendar, stating plainly that winter blindness is a conservative choice.

### 3.4 The robustness run: a frozen planting, a best case recourse, and a mixed sample

Verdict: the freeze is labelled with care, and the headline sentence then reads more into the run than its design carries.

The paper states that late planting is frozen at the normal inflow variant, because a sampled budget carries no state label. That is honest. Two further features are not carried into the headline. First, each sample reoptimises water and abandonment to maximise tonnage, so the run measures what the frozen planting could still deliver under the best possible recourse, not what the fixed plan, operated as planned, would deliver. The paper's own phrase, the maximum share it could hold, is accurate; the sentence that follows it, that the promise breaks about one year in three under historical hydrology, is a performance claim the design does not support. Second, the sample alternates single years with ten year window means. Half the draws are decadal averages, whose spread is far narrower than annual flows, and overlapping windows share nine of their ten years, so the sample is not 100 draws of anything a year can be. A frequency computed over that mixture is not an annual reliability, and the worst decile shortfall inherits the same mixture.

Smallest supported correction: report the single year samples and the window samples as two distributions, and retitle the measure as the share of sampled years in which the frozen planting can still reach its floor under best recourse. The finding survives in a weaker and truer form.

## 4. Uncertainty design

### 4.1 The drought state does not belong in the probability simplex

Verdict: the weakest piece of formal design in the paper.

Dry, normal and high are frequencies of single years in the 1871 to 1970 record. The drought state is built from ten year window means of the same record: its ratio is the minimum window ratio, and its probability is the share of windows at or below that minimum, which is one window in 91 by construction, since the minimum window itself always qualifies. The probability is therefore not estimated from the record; it is manufactured by the construction, and would be 1 in 91 for any record whatsoever. The three annual probabilities are then rescaled to make room for it, and expectations are taken across the mixture as if all four states were the same kind of year. They are not. Worse, the drought state's annual budget ratio, 0.8709, is higher than the dry state's 0.7807. The state named drought carries more water than the state named dry, because the real content of a drought is duration, and duration is exactly what a one year budget cannot express in a model that holds no storage variable. The paper concedes that dropping the state changes no result, because the dry state binds harder. A state that changes nothing, whose probability is an artifact, and whose name contradicts its budget should not sit inside the probability weights of every expected number in the paper.

Smallest supported correction: remove the drought state from the simplex and present it where it belongs, as a named stress beside the runs of Section 6.4. The frontier and the ceiling barely move, and the design becomes clean.

### 4.2 The layer weights contradict the band construction

Verdict: a checkable inconsistency between the code and Appendix C, with money attached.

The forecasting code builds the low and high states from the 10th and 90th percentiles of the one step backtest residuals. That is an 80 percent band. Appendix C then assigns the three layers probabilities of 0.25, 0.50 and 0.25, describing the band as read in quartiles. Both statements cannot be true of the same construction. If the low state sits at the 10th percentile of the residual distribution, the mass below it is near a tenth, not a quarter. The chosen weights therefore load the two tail layers with roughly two and a half times the probability the project's own residuals support. Every expected margin, every rung cost and the expected value of perfect information inherit that overweighting. The hard floor results, the ceiling and feasibility, do not depend on the weights and are untouched. Separately, the coverage of the band is reported nowhere: the reader is never told in what share of backtest origins the realised value actually fell inside the band the model treats as its uncertainty.

Smallest supported correction: either rebuild the layers at the residual quartiles and keep the weights, or keep the band and set the layer weights from the empirical masses, and print the backtest coverage of the band per crop in Appendix A. One of the two repairs must be made; at present the paper asserts a probability distribution its own code does not produce.

### 4.3 One shock for everything

Verdict: named as an assumption, never measured as a cost.

Inside a layer, the prices and yields of all five crops move together, and the yield movement is a single national proportional factor applied identically to all eight governorates. There is no scenario in the twelve in which wheat yields fail while maize holds, none in which the northern districts suffer and the southern do not, and none in which prices fall while yields rise. Every hedge that crop diversity and geography could offer a guarantee is designed out, and the guarantee must then survive the joint bad state in full. That pushes the ceiling down and the rung prices up by an amount the paper never estimates. The independence of the layers from the inflow state is also named, and is the more defensible half of the design, since Egyptian staple prices are heavily administered and import linked. The co movement within the layer is the expensive half.

Smallest supported correction: one run with the yield layers decorrelated by crop group, prices held at expected, reported beside the ceiling. If the ceiling moves little, a named assumption becomes a tested one.

### 4.4 Forecast evaluation hygiene

Verdict: careful code, two faults, one of them presentational and one statistical.

The backtest respects its origins: features are lags and a trend only, training pairs are cut at the origin, failed fits are logged, and losing models are printed. Two faults remain. First, model selection is performed on the same backtest whose errors are then reported as the selected model's errors. With five candidates the winner's curse is mild, and the headline result, that nothing beat drift on prices, is plainly not a selection artifact. But where a learner won narrowly, on yields, its printed error is optimistically biased by an unstated amount. Second, the target years do not match, and Section 4 blurs the fact. Prices are forecast for 2024. Yields are forecast for 2025. And the model's expected yields are neither forecast: they are the published district yields of 2020 to 2021, with only the band ratios borrowed from the 2025 national forecast. Section 4 reads as though the model consumes next season yield forecasts as levels. It consumes their spread only. A reader who stops at Section 4 misunderstands what the model ate.

Smallest supported correction: one sentence each in Sections 4 and 5 stating which forecast product enters as levels and which as ratios, and one sentence acknowledging that selection and scoring share a single backtest.

## 5. Claims discipline

### 5.1 What the guarantee protects

Verdict: the body of the paper is exact; the title and the abstract promise in a larger voice.

The floor protects one number: aggregate tonnage of wheat, paddy rice and summer maize, summed over eight governorates, in each of twelve constructed scenarios, measured against a reference built from one observed pattern. It does not protect wheat if maize can carry the tonnage, and nothing in the constraint stops a plan from meeting the floor with a crop mix no food policymaker would accept as the same promise. It does not protect milled rice, calories, protein, or any household's access to food. Sections 5, 6.1 and 8 say all of this with unusual clarity. The abstract, though, speaks of a guarantee that staple output holds in a dry year, and the title names a food guarantee without qualification. Readers of applications read titles and abstracts. The distance between the front door and the fine print is the one place this disciplined paper oversells.

Smallest supported correction: carry the words aggregate tonnage of three staples into the abstract's guarantee sentence. The body needs no change.

### 5.2 The historical pattern: 60.12 percent, and no guarantee at any level

Verdict: on the face of the paper, these two statements cannot both be true, and the reconciliation is not given. This is the first wound a careful reader finds.

Section 6.2 prints the historical pattern delivering 7,367,358 tonnes in its worst scenario, 60.12 percent of the reference quantity. The same section states that inside this model the pattern holds no guarantee at any level on the ladder. The ladder's lowest rung is 50 percent. A pattern whose worst scenario delivers 60.12 percent holds the 50 percent rung and the 60 percent rung, under the paper's own definition of holding a floor, unless the two sentences rest on different evaluations. A reconciliation may exist: the tonnage figure may come from an evaluation in which water is reallocated optimally under the pattern's planting, while guarantee holding may be judged on the pattern as actually watered, which the dry state budgets cannot supply at full duty, since baseline demand at full duties is 16.398 billion cubic metres against a dry budget of 8.588. If that is the explanation, the paper must print it, because as written the section contradicts itself in consecutive paragraphs and a referee will not do the author's repair work for him.

Smallest supported correction: one paragraph in Section 6.2 stating the two evaluations, which quantities each fixes and which it frees, and the per scenario tonnage of the pattern under each. If no such distinction exists, one of the two sentences must be withdrawn.

### 5.3 Filled cells beyond the one the paper names

Verdict: small quantities, a real principle, and an easy repair.

The paper names exactly one filled cell, the Menoufia rice area and yield. The code fills more. Nili maize yields are missing in four of the eight governorates and are filled with the area weighted mean of the four that report. Nili potato yields are published for Beheira alone, and Beheira's figure is carried to the other seven governorates. I verified both against the source files. The affected areas are small and no headline plausibly moves. But Section 3 opens with the claim that every number in the model comes from a named source, and Appendix A, which lists the Menoufia fill with care, is silent on these. A paper whose authority rests on naming every gap cannot leave fills for a referee to find in the code.

Smallest supported correction: list every filled cell in Appendix A in the same format as the Menoufia entry. The run log already records them.

### 5.4 The contribution claim

Verdict: stated at the strength the evidence carries, which is rarer than it should be.

The claim is a combination claim: no published model searched joins a Delta only governorate level stochastic allocation, a staple floor swept level by level with its margin cost, scenario specific district water values, and a benchmark against the observed pattern. The paper names its closest neighbours, concedes the method is textbook, and prints the narrower restatement its prior work review supports. That is the most a single author exploratory model can honestly claim, and the paper claims no more. The one softness is that the claim rests on a literature search the reader cannot inspect from the paper itself, so the searched form of the claim, which the paper mostly keeps, must be kept everywhere, including any summary written for an application.

No correction required beyond vigilance in derivative documents.

### 5.5 The MIT admissions reader

What that reader assumes on finishing: an author with unusual data honesty, genuine Arabic source skill, and the instinct to print his own failures before a referee can find them. Those assumptions are worth a great deal in a business analytics cohort.

What that reader doubts: every number that rests on the calibrated water anchor, and every money figure that rests on fixed potato prices. Between them, those two doubts cover the abstract's two money headlines.

What that reader asks first: show me the ladder and the ceiling as functions of the water anchor, and reconcile the 60.12 percent worst case with no guarantee at any level. If both answers arrive clean and printed, the reader's respect rises sharply, because by then they have learned that this author's stated conditions are the whole story, and the remaining claims are mostly as strong as their conditions say.

## 6. The three hardest questions

Question 1. Your ceiling and your 227.9 billion pound price both scale from an 11.00 billion cubic metre budget that you calibrated and no source publishes. What are the ceiling and the ladder at 9.90 and at 12.10, and at what anchor value does your headline change its meaning?
A good answer requires the frontier and ceiling actually rerun at the scaled anchors and printed, with the rung costs, not a verbal assurance that the results are robust. It also requires the author to say which anchor evidence, if it existed, would settle the number, and why the land share split of the budget is the right geography.

Question 2. Section 6.2 gives the historical pattern a worst scenario of 60.12 percent of the reference tonnage and, two sentences later, no guarantee at any level, on a ladder that begins at 50 percent. Which sentence should I believe, and what exactly differs between the two evaluations that produced them?
A good answer requires the two evaluation definitions stated side by side, the pattern's tonnage in each of the twelve scenarios under each, and a corrected sentence in the paper. An answer that explains without printing the table has not answered.

Question 3. Three choices sit upstream of your price for the guarantee. The floor can be met by maize alone while wheat collapses. Wheat is paid at a farm gate forecast about 42 percent below the procurement price your own appendix documents. And your layers force every crop's price and yield to move together, in every district at once. Which of the three, relaxed, moves the price of the guarantee most, and why does the paper test the beet price concept, which it shows changes nothing, and none of these?
A good answer requires at least one of the three runs actually performed, wheat at procurement, a per crop floor variant, or a decorrelated layer run, with its effect on the ladder reported, and an honest account of why the tested variant was the one with a zero effect.

## Closing judgment

This is a strong exploratory paper with an honest spine and three open wounds: a baseline section that contradicts itself on its face, a probability design that mixes objects and contradicts its own code, and a headline price for the guarantee that is measured only in the relaxed world the paper itself warns against, on a water budget nobody can check. None of the three is fatal. All three are repairable with runs the existing code can already perform, plus a small number of sentences. Repaired, the paper's claims and its evidence would finally be the same size, which is the standard this author has set for himself everywhere else in the document.

## Comparison with the earlier audits, added after reading them

This section was written after the findings above were complete. It records where the earlier audits agree with this critique, where they reached the same ground first, and what none of them examined. The audits read were paper/Audit_Log_v4_1.md, paper/Audit_Log_Paper.md and docs/GPT_AUDIT_v3.md, together with the stage S1 inventory in this folder.

### Where the earlier audits were first, and I agree

The version 4.1 reaudit found the dual non uniqueness before I did, quantified it with its own solves, and named the Damietta value of 16.68 pounds per cubic metre that falls outside the printed range. The paper already carries that correction, which is why my critique lists the dual presentation among the strengths. The reaudit also raised the reserve write off of 30,136 hectares and the fact that the reserve acceptance test cannot fail by construction. My finding 1.2 agrees with both points and adds the part the reaudit did not test: the seasonal shape of the split itself, and the observation that comparing the capped split with the uncapped split varies the cap while leaving the shared assumption untouched.

The paper audit caught wording faults that are already repaired in the text I reviewed, including the limits section sentence about which drought enters the model, the forecast error discipline, the backtest lengths and the abstract ceiling wording. My critique read the corrected paper throughout, and its findings are against the corrected text.

The GPT audit of version 3 found six formulation level defects, and the foundations document adopted all six. Every one of them belongs to the superseded version. Nothing in my critique revives them, and the build I read has genuinely repaired each: seasonal land pools, true mean benchmarks, real abandonment, a priced frontier and paired stress reporting are all present in the code.

### Where an earlier audit verified the numbers and the wording question stayed open

The reaudit graded the historical pattern evaluation as survived: expected tonnage 8,908,274 and minimum 7,367,358 tonnes both reproduce under its own code. That verification is about the numbers. My finding 5.2 is about the sentence printed beside them. The reaudit never asks how a pattern with a worst scenario of 60.12 percent holds no guarantee at any level of a ladder that starts at 50 percent, and the paper audit, which was alert to wording elsewhere, does not ask it either. The concern is not mine alone: the handoff package prepared for this rebuild carries an adversarial case, E03, built on exactly this pair of statements and requiring it to be resolved with unrounded outputs. As of this writing no executed audit has resolved it. It remains, in my judgment, the first repair the paper needs.

The reaudit likewise rederived twenty of the hundred robustness samples exactly and confirmed that the frozen late planting convention is material and disclosed. It did not question the reading of a sample that mixes single years with ten year window means as an annual failure frequency. Finding 3.4 stands as new.

### What none of the earlier audits examined

The following findings of this critique have no counterpart in any of the three audits.

1. The layer weights against the band construction, finding 4.2. The reaudit verified the probability arithmetic: the weights sum, the true mean budget replays at 10.9844. Neither it nor the paper audit compares the 0.25, 0.50 and 0.25 layer weights with the forecasting code, where the low and high states are built from the 10th and 90th percentiles of the backtest residuals. The parallel numerical check now running in this folder recomputes the probabilities as given, which is the same remit. The inconsistency between the weights and the band is therefore still unexamined by any check but this one.
2. The drought state as a probability object, finding 4.1. The paper audit touched the drought state only to correct which drought the limits section said enters it. No audit asks what a probability of one window in 91, guaranteed by construction, is doing inside the simplex, or why the drought state carries more annual water than the dry state.
3. The missing wheat price variant, finding 2.3. The reaudit verified the sugar beet identity claim to the pound. No audit asks why the price concept variant was run for the crop where it changes nothing and not for wheat, where the documented procurement price sits about 42 percent above the price the model pays.
4. The cost basis carried no further than its name, finding 2.1. No audit tests the frontier against costs carried from 2022 toward 2024, although the foundations document requires the cost of a named gap to be stated.
5. The capped price list that the paper never prints, finding 2.2. The reaudit solved the capped frontier itself and reproduced five capped margins to the pound, so the numbers exist and are verified. The omission is at paper level: the paper prints only the capped ceiling. No audit graded the paper on the absence of its own central product in its market sane form.
6. The yield fills beyond Menoufia, finding 5.3, verified by me directly against the source files. No audit lists them.
7. The timing and dependence questions of findings 3.2, 3.3, 4.3 and 4.4, and the two interpretation points of finding 1.4: district budgets split by land share, so the dual map reflects crop mix rather than supply geography, and the ladder never repriced at a scaled water anchor. The audits verified the stress runs at scaled budgets for capacity and choice, which is a different question from the price of the guarantee at those budgets.

### One caution the S1 inventory adds to all of the above

The inventory in this folder records that the reaudit artefacts predate the final saved form of the model code, and that no run log from the version 4.1 run behind the first results note survives. The agreement between the audits, the logs and the paper is numerical, not byte level. That caution applies to my critique as well: everything above describes the saved build as found on 15 November 2026.

### Net assessment after comparison

The earlier audits prove, to a high standard, that the printed numbers are the numbers this code produces on this data. My critique does not disturb that conclusion, and its arithmetic findings are confined to presentation points the reaudit had already caught. The disagreement is one level up. The reaudit closed with a verdict of minor revision, which is the right verdict on the arithmetic and an incomplete verdict on the paper, because its remit was reconstruction. Read together, the record now shows a build whose computations reproduce and whose design, in the probability weights, the drought state, the price concepts and the untested reserve split, is in four places not the design the paper describes. Those four, with the baseline reconciliation of finding 5.2, are the repairs that decide whether the paper's evidence and its claims are the same size.
