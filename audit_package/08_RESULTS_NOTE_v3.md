# Results note, Problem One, version 3, data run

Factual internal record of the version 3 rerun on the real data foundation. This is not a paper and carries no narrative. Every figure below appears in data/processed/run_v3_beet795_output.txt or data/processed/run_v3_beet2400_output.txt, produced by src/allocation_model_v3.py. Prices carry the year 2023 and costs carry the years 2016 to 2017 wherever a money figure is reported, except the two procurement anchors, which carry their own years. RERUN_CHOICES.md records every modelling choice with its foundation section.

## Parameters

* National yields: FAOSTAT via Our World in Data, Egypt means over 2014 to 2023, loaded as version 2 loads them. Foundation Section 1. Wheat 6.57, rice 9.15, maize 7.37, sugar beet 52.19, potatoes 28.09 tonnes per hectare.
* Prices, FAOSTAT producer prices, 2023, Egyptian pounds per tonne. Foundation Section 2. Wheat 10,000; rice paddy 18,761; maize 14,400; potatoes 8,160. Sugar beet: 795 in variant beet795 (FAOSTAT farm gate, Section 2) and 2,400 in variant beet2400 (factory procurement for the 2024 to 2025 season, Section 3).
* Costs, CAPMAS 2016 to 2017, Egyptian pounds per hectare, rent inclusive. Foundation Section 4. Wheat 21,473.81; rice 19,902.38; maize summer 18,933.33; sugar beet 17,607.14; potatoes summer 49,533.33. The potatoes summer row is adopted because CAPMAS publishes no winter potatoes cost; the choice is flagged in RERUN_CHOICES.md.
* Land base: total cropped area 2020 to 2021 from the delivered CSV, total 3,176,474 hectares across the eight governorates. Foundation Section 5.
* District yield multipliers: real, crop specific, computed from the 2020 to 2021 panels. Foundation Section 7. Computed production weighted means match the foundation printed values for all five crops: wheat 6.87, rice 9.14, maize 8.79, sugar beet 49.37, potatoes 28.39 tonnes per hectare.
* Baseline pattern: real district hectares by governorate and crop for 2020 to 2021. Foundation Section 6. Baseline staple production at full water: 11,493,640 tons. Food floor at 90 percent: 10,344,276 tons per scenario.
* Water requirements, applied basis, primary case, cubic metres per hectare. Foundation Section 8. Wheat 5,126; rice 16,600; maize 9,305; sugar beet 9,426; potatoes 4,825.85, computed as the area weighted mean of the winter value 4,079 (weight 61,667.34 hectares) and the summer value 6,145 (weight 34,913.34 hectares), Nili area excluded.
* Water requirements, net basis, sensitivity case, cubic metres per hectare, Gabr 2022. Foundation Section 8. Wheat 1,272; rice 11,441; maize 5,762; sugar beet 3,927; potatoes 2,448. The wheat net row carries the foundation flag of internal inconsistency, printed in the beet795 log where the net case is reported.
* Yield response factors. Foundation Section 9. Wheat 1.05; rice 1.20, carried from version 2 and labelled unverified per Section 9 and gap 23; maize 1.25; sugar beet 1.00; potatoes 1.10.
* Scenarios, primary: Derivation A of Foundation Section 10 on the calibration anchor of 11.00 billion cubic metres. Probabilities low 0.23, expected 0.45, high 0.32. Budgets 8.591, 10.505 and 13.431 billion cubic metres. The 11.00 figure is a calibration, per Foundation Section 11.
* Scenarios, sensitivity: Derivation B of Foundation Section 10. Probabilities 0.33, 0.34, 0.33. Budgets 8.921, 10.703 and 13.387 billion cubic metres on the same calibration anchor.
* Baseline water demand at full watering: 16.724 billion cubic metres against an expected budget of 10.505 billion cubic metres.

## Headline results at the 90 percent floor

Prices at 2023 levels, costs at 2016 to 2017 levels in every figure in this section.

* Variant beet795: optimised expected margin EGP 140,511,553,290; baseline expected margin EGP 95,107,983,182; gain EGP 45,403,570,107, which is 47.74 percent. Margin per cubic metre, an average return and never a price: EGP 13.92 optimised against EGP 8.70 baseline. Baseline expected staple output 7,988,507 tons. The optimised plan plants zero hectares of sugar beet in every district. Water coverage in the low scenario: wheat 0.991, rice 0.167, maize 0.987, potatoes 0.188.
* Variant beet2400: optimised expected margin EGP 147,993,830,742; baseline expected margin EGP 96,779,569,341; gain EGP 51,214,261,401, which is 52.92 percent. Margin per cubic metre, an average return and never a price: EGP 13.45 optimised against EGP 8.85 baseline. Baseline expected staple output 7,386,025 tons. Water coverage for sugar beet: 0.000 in the low scenario, 0.033 in the expected scenario, 1.000 in the high scenario. Water coverage for potatoes in the low scenario: 0.211.
* Dual verifications, Dakahlia expected scenario. Deterministic model: solver dual EGP 15.794 per cubic metre, brute force bump implies EGP 15.794, in both variants. Stochastic model: variant beet795 reported raw dual 5.820, brute force implies 5.819; variant beet2400 reported raw dual 7.211, brute force implies 7.211.
* Information values. Variant beet795: wait and see EGP 158,906,173,697; EVPI EGP 18,394,620,407; expected result of planning on the average year EGP 139,898,374,426; VSS EGP 613,178,863. Variant beet2400: wait and see EGP 160,541,880,635; EVPI EGP 12,548,049,893; expected result of planning on the average year EGP 139,968,163,242; VSS EGP 8,025,667,499. Wait and see statuses are Optimal in all scenarios in both variants.

## Guarantee price list, both beet prices side by side

The food floor at three levels of baseline staple production. Prices at 2023 levels, costs at 2016 to 2017 levels. Margin per cubic metre is an average return, never a price.

* Floor at 90 percent. Beet795: optimised EGP 140,511,553,290; baseline EGP 95,107,983,182; gain EGP 45,403,570,107 (47.74 percent); margin per cubic metre EGP 13.92 optimised and EGP 8.70 baseline. Beet2400: optimised EGP 147,993,830,742; baseline EGP 96,779,569,341; gain EGP 51,214,261,401 (52.92 percent); margin per cubic metre EGP 13.45 optimised and EGP 8.85 baseline.
* Floor at 95 percent. Beet795: the floor cannot be held in every scenario; solve status Infeasible; no margin reported. Beet2400: the floor cannot be held in every scenario; solve status Infeasible; no margin reported.
* Floor at 100 percent. Beet795: the floor cannot be held in every scenario; solve status Infeasible; no margin reported. Beet2400: the floor cannot be held in every scenario; solve status Infeasible; no margin reported.

## Water value map, conditional units

Values inside each scenario, raw dual divided by the scenario probability, Egyptian pounds per cubic metre. These are duals, that is marginal values. Prices at 2023 levels, costs at 2016 to 2017 levels.

District levels and rankings in this map now rest on real district yields: the multipliers behind them are computed from the 2020 to 2021 governorate panels, foundation Section 7. Menoufia rice multiplier is a neutral fill of 1.00 for an unreported cell, foundation Sections 6 and 7, so the Menoufia row carries that flag.

Variant beet795, conditional values by governorate and scenario:

* Beheira: low 51.67, expected 13.41, high 0.00.
* Dakahlia: low 58.81, expected 12.93, high 0.00.
* Damietta: low 49.78, expected 12.89, high 0.00.
* Gharbia: low 55.80, expected 10.50, high 0.00.
* Kafr El Sheikh: low 68.00, expected 10.32, high 0.00.
* Menoufia: low 52.20, expected 13.82, high 0.00. Menoufia rice fill flag applies to this row.
* Qalyubia: low 75.52, expected 6.17, high 0.00.
* Sharkia: low 57.31, expected 8.84, high 0.00.

Variant beet2400, conditional values by governorate and scenario:

* Beheira: low 49.83, expected 15.87, high 6.10.
* Dakahlia: low 53.44, expected 16.02, high 8.32.
* Damietta: low 43.91, expected 16.08, high 10.24.
* Gharbia: low 55.80, expected 16.21, high 10.38.
* Kafr El Sheikh: low 68.00, expected 12.31, high 6.47.
* Menoufia: low 47.42, expected 16.63, high 7.82. Menoufia rice fill flag applies to this row.
* Qalyubia: low 78.57, expected 13.14, high 7.30.
* Sharkia: low 57.31, expected 13.85, high 8.01.

## Stress results

Stochastic model rebuilt at reduced budgets, 90 percent floor, honest reporting as in version 2: when the floor cannot be held, the margin of the unfloored run is stated as not comparable. Prices at 2023 levels, costs at 2016 to 2017 levels.

* Variant beet795, water cut 10 percent: the food floor cannot be held. Staple output falls to 6,212,681 tons, which is 60 percent of the floor. Margin without the floor is EGP 157,547,600,225 and is not comparable to the floored runs. District absorbing the largest staple loss: Beheira, 1,156,202 tons in the expected scenario.
* Variant beet795, water cut 20 percent: the food floor cannot be held. Staple output falls to 5,285,121 tons, which is 51 percent of the floor. Margin without the floor is EGP 147,951,710,417 and is not comparable to the floored runs. District absorbing the largest staple loss: Beheira, 1,334,816 tons in the expected scenario.
* Variant beet2400, water cut 10 percent: the food floor cannot be held. Staple output falls to 326,570 tons, which is 3 percent of the floor. Margin without the floor is EGP 176,203,394,815 and is not comparable to the floored runs. District absorbing the largest staple loss: Sharkia, 2,387,509 tons in the expected scenario.
* Variant beet2400, water cut 20 percent: the food floor cannot be held. Staple output falls to 0 tons, which is 0 percent of the floor. Margin without the floor is EGP 165,237,311,866 and is not comparable to the floored runs. District absorbing the largest staple loss: Sharkia, 2,387,509 tons in the expected scenario.

## Sensitivity results, variant beet795

Each swing reevaluates the baseline under the same moved parameters. Prices at 2023 levels, costs at 2016 to 2017 levels. Gain is optimised expected margin minus baseline expected margin at the 90 percent floor.

* Base case: gain EGP 45,403,570,107 (47.74 percent).
* Rice price times 0.8: gain EGP 51,273,409,700 (57.48 percent).
* Rice price times 1.2: gain EGP 36,598,726,427 (35.15 percent).
* Potatoes price times 0.8: gain EGP 31,161,489,906 (34.38 percent).
* Potatoes price times 1.2: gain EGP 59,656,348,291 (59.92 percent).
* Rice and potatoes prices times 0.8: gain EGP 37,029,644,156 (43.70 percent).
* Rice and potatoes prices times 1.2: gain EGP 50,811,418,287 (46.80 percent).
* All production costs times 0.8: gain EGP 49,288,433,618 (47.91 percent).
* All production costs times 1.2: gain EGP 41,611,580,409 (47.64 percent).
* All water budgets times 0.95: gain EGP 7,252,817,004 (8.15 percent).
* All water budgets times 1.05: gain EGP 48,026,658,431 (47.62 percent).

Wheat procurement variant, beet795 set, wheat at EGP 14,667 per tonne (confirmed 2025 procurement anchor, foundation Section 3), sugar beet held at 795, everything else held equal:

* Floor at 90 percent: optimised EGP 188,894,115,012; baseline EGP 115,243,156,635; gain EGP 73,650,958,377 (63.91 percent); margin per cubic metre EGP 18.76 optimised and EGP 10.54 baseline, an average return and never a price.
* Floor at 95 percent: the floor cannot be held in every scenario; no margin reported.
* Floor at 100 percent: the floor cannot be held in every scenario; no margin reported.

Net water basis run, beet795 set, Gabr 2022 net requirements, foundation Section 8, with the wheat net row flag of internal inconsistency printed in the log:

* Headline at the 90 percent floor: optimised expected margin EGP 262,534,931,795; baseline expected margin EGP 146,717,442,067; gain EGP 115,817,489,728 (78.94 percent). Margin per cubic metre EGP 26.02 optimised and EGP 16.94 baseline, an average return and never a price. Optimised expected staple output 18,421,506 tons; baseline expected staple output 11,253,819 tons.
* Guarantee sweep on the net basis: the floor never binds. The 90, 95 and 100 percent levels return the same three figures: optimised EGP 262,534,931,795, baseline EGP 146,717,442,067, gain EGP 115,817,489,728 (78.94 percent).

Derivation B run, beet795 set, foundation Section 10, on the same calibration anchor:

* Headline at the 90 percent floor: optimised expected margin EGP 137,175,511,984; baseline expected margin EGP 95,119,555,100; gain EGP 42,055,956,884 (44.21 percent). Margin per cubic metre EGP 13.49 optimised and EGP 8.70 baseline, an average return and never a price.
* Floor at 95 percent: optimised EGP 113,946,907,413; baseline EGP 95,119,555,100; gain EGP 18,827,352,313 (19.79 percent); margin per cubic metre EGP 11.27 optimised and EGP 8.70 baseline.
* Floor at 100 percent: the floor cannot be held in every scenario; no margin reported.

## What changed against version 2

Each version 2 headline from paper/Results_Note_v2.md, beside its version 3 counterpart or the words does not survive. Version 3 money figures carry prices at 2023 levels and costs at 2016 to 2017 levels.

* Version 2: gain of 10.44 percent at the 90 percent floor. Version 3: gain of 47.74 percent with sugar beet at 795, and 52.92 percent with sugar beet at 2,400.
* Version 2: gain of 4.54 percent at the 95 percent floor. Version 3: does not survive. Under the primary scenario set the 95 percent floor cannot be held in either variant and no margin is reported. Under Derivation B with sugar beet at 795 the level can be held and the gain is 19.79 percent.
* Version 2: loss of EGP 3.75 billion at full protection, floor at 100 percent. Version 3: does not survive. The 100 percent floor cannot be held under the primary scenario set in either variant, so there is no margin and no loss figure at that level. On the net water basis the floor never binds at any level.
* Version 2: expected year water values of EGP 8.02 to 10.21 per cubic metre, conditional units. Version 3: EGP 6.17 to 13.82 with sugar beet at 795, and EGP 12.31 to 16.63 with sugar beet at 2,400.
* Version 2: dry year water values of EGP 33.03 to 37.90 per cubic metre, conditional units. Version 3: EGP 49.78 to 75.52 with sugar beet at 795, and EGP 43.91 to 78.57 with sugar beet at 2,400.
* Version 2: sugar beet write off of 317,308 hectares with EGP 11.42 billion of planting cost sunk in the low scenario. Version 3: does not survive as stated. With sugar beet at 795 the plan plants zero hectares of sugar beet, so no write off exists. With sugar beet at 2,400 the plan plants sugar beet in all eight districts and delivers 0.000 of its water requirement in the low scenario and 0.033 in the expected scenario; the write off pattern returns under the procurement price, at a different scale.
* Version 2: a 10 percent water cut costs EGP 13.70 billion with the guarantee held. Version 3: does not survive. At a 10 percent cut the floor cannot be held in either variant, so no comparable margin cost exists. Staple output falls to 6,212,681 tons with sugar beet at 795 and to 326,570 tons with sugar beet at 2,400 in the unfloored runs.
* Version 2: at a 20 percent water cut, staple output falls to 6.16 million tons. Version 3: staple output falls to 5,285,121 tons with sugar beet at 795 and to 0 tons with sugar beet at 2,400 in the unfloored runs.
* Version 2: EVPI of EGP 10.37 billion. Version 3: EVPI of EGP 18,394,620,407 with sugar beet at 795, and EGP 12,548,049,893 with sugar beet at 2,400.
