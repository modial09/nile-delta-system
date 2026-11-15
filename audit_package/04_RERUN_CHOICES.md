# Rerun choices for version 3 of the Nile Delta water allocation model

This file records every choice made in the version 3 rerun, each with the section of data/DATA_FOUNDATION.md that governs it. The foundation is the permitted source of parameters. Where a choice is a modelling decision rather than a sourced value, this file says so in plain words.

## Prices

* Crop prices are FAOSTAT producer prices, latest complete year 2023, Egyptian pounds per tonne, foundation Section 2: wheat 10,000; rice paddy 18,761; maize 14,400; potatoes 8,160.
* Sugar beet runs under two price concepts and everything else is held equal between the two variants. Variant beet795 uses 795 Egyptian pounds per tonne, the FAOSTAT farm gate value, foundation Section 2. Variant beet2400 uses 2,400 Egyptian pounds per tonne, the factory procurement price for the 2024 to 2025 season, foundation Section 3. The foundation states that the two series measure different things and differ by a factor of three, and that the model must state which concept it uses. Running both is the statement.
* Wheat variant run, inside the beet795 log: wheat at 14,667 Egyptian pounds per tonne, the confirmed 2025 procurement anchor, foundation Section 3, with sugar beet held at 795 and everything else held equal. Its guarantee table is printed in the beet795 log.

## Costs

* Production costs are CAPMAS 2016 to 2017, Egyptian pounds per hectare, rent inclusive, foundation Section 4: wheat 21,473.81; rice 19,902.38; maize summer 18,933.33; sugar beet 17,607.14; potatoes summer 49,533.33.
* The potatoes cost choice is a named decision. CAPMAS publishes no winter potatoes cost in the tables the foundation carries, so the summer row is adopted and flagged here and in the run logs. The model carries one potatoes parameter set while the sources split potatoes by season, which foundation gap 25 records.
* Every cost figure in every output carries the label 2016 to 2017 levels, and every price figure carries the year 2023, except the two procurement anchors, which carry their own years from foundation Section 3.

## Yields and district multipliers

* National yields stay the FAOSTAT via Our World in Data Egypt means over 2014 to 2023, loaded exactly as version 2 loads them, foundation Section 1.
* The single invented district multiplier of version 2 is replaced by real crop specific district multipliers computed from the 2020 to 2021 panels, foundation Section 7. The multiplier for district d and crop c equals the district yield in capmas_governorate_yield.csv divided by the production weighted mean of the eight governorate yields for that crop. The weighted mean is computed as total production from capmas_governorate_production.csv divided by total area, where each governorate area is implied by its production and its published yield in the two delivered CSV files.
* The computed weighted means were checked against the foundation printed values before any run: wheat computed 6.87 against 6.87 printed; rice 9.14 against 9.14; maize 8.79 against 8.79; sugar beet 49.37 against 49.37; potatoes 28.39 against 28.39 tonnes per hectare. The comparison is printed in both run logs.
* Menoufia rice yield for 2020 to 2021 is not reported in the source. That one multiplier cell is filled with 1.00, the weighted mean itself. This is a neutral fill for an unreported cell, flagged here, in both run logs wherever the water value map is printed, and in the results note.

## Land base

* The land base is total cropped area for 2020 to 2021 by governorate from capmas_governorate_total_cropped_area.csv, foundation Section 5, read from the CSV in code and never hard coded: Beheira 720,839; Sharkia 679,538; Dakahlia 533,501; Kafr El Sheikh 450,195; Gharbia 308,142; Menoufia 269,172; Qalyubia 119,480; Damietta 95,608 hectares, total 3,176,474 hectares as printed by the CSV values in the run logs.
* Why total cropped area is the concept adopted: the model land constraint binds the sum of winter and summer plantings in one pool, and total cropped area counts every crop season in the year, so it is the published concept that matches a single pool summed across seasons. Foundation Section 5 states that the model pool matches neither published concept exactly, because a physical hectare can carry a winter crop and then a summer crop while the model makes them compete. The decision is recorded here as a modelling decision, openly.
* The alternative on the record: cultivated area for 2020 to 2021 totals 1,676,580 hectares across the eight governorates, foundation Section 5. It was not adopted, for the reason above.

## Baseline pattern

* The baseline is the real district pattern, hectares by governorate and crop for 2020 to 2021 from capmas_governorate_area.csv, foundation Section 6: wheat winter, sugar beet winter, rice summer, maize summer, potatoes all seasons.
* Menoufia rice for 2020 to 2021 is not reported in the source table. The delivered 2019 to 2020 published value of 7.98 hectares is used for that one cell and flagged here and in the run logs.
* Baseline staple production is computed at full water with the same national yields and the same real crop specific multipliers as the model, so the food floor and the baseline stay consistent.

## Water requirements

* Primary case, applied basis, cubic metres per hectare, CAPMAS 2017 as printed in Abdelwahab et al. 2024, foundation Section 8: wheat 5,126; rice 16,600; maize summer 9,305; sugar beet 9,426.
* Potatoes applied value is arithmetic on sourced values, not a published value. It is the area weighted mean of the winter value 4,079 and the summer value 6,145, using the delivered 2020 to 2021 winter and summer potato areas summed over the eight governorates. The weights are winter 61,667.34 hectares and summer 34,913.34 hectares. The result is 4,825.85 cubic metres per hectare. The Nili area is excluded from the weighting for want of a published Nili requirement.
* Sensitivity case, net basis, cubic metres per hectare, Gabr 2022, foundation Section 8: wheat 1,272; rice 11,441; maize 5,762; sugar beet 3,927; potatoes 2,448. The wheat net row carries the foundation flag of internal inconsistency, and that flag is printed in the beet795 run log where the net case is reported, at its start and at its end.

## Yield response factors

* Foundation Section 9: maize 1.25; sugar beet 1.00; potatoes 1.10; wheat 1.05. The wheat value is the foundation correction: Egypt grows winter wheat, and version 2 used 1.00.
* Rice 1.20 is carried from version 2 but is labelled unverified in the outputs, per foundation Section 9 and gap 23. No citable FAO table carries a seasonal rice value.

## Scenarios

* Primary case: Derivation A of foundation Section 10 applied to the calibration anchor of 11.00 billion cubic metres. Probabilities: low 0.23, expected 0.45, high 0.32. Budget multipliers: 0.781, 0.955 and 1.221, giving budgets of 8.591, 10.505 and 13.431 billion cubic metres.
* Sensitivity case: Derivation B of foundation Section 10. Probabilities 0.33, 0.34 and 0.33; multipliers 0.811, 0.973 and 1.217 on the same anchor, giving budgets of 8.921, 10.703 and 13.387 billion cubic metres.
* Every output that prints a budget or a probability labels the 11.00 figure a calibration, exactly as foundation Section 11 requires. No official figure exists for a water budget of the eight governorate model area, and none is claimed.

## Structure carried from version 2

* Two stage stochastic linear program in PuLP; stage one hectares by district and crop; stage two water by district, crop and scenario; linear yield response production with the production floor at zero on every planting and scenario; the food floor as one constraint per scenario on staple production for wheat, rice and maize; district water budgets as shares of the scenario total by land share; dual extraction reporting both the raw dual and the conditional per scenario value; brute force dual verification inside the stochastic model and inside the deterministic model; the water coverage table; information values with wait and see statuses reported, never silently zeroed; stress runs at 10 and 20 percent water cuts with the version 2 honest reporting when the floor cannot be held.
* Crop cap shares are as in version 2 and remain a declared modelling device: wheat 0.50, rice 0.35, maize 0.40, sugar beet 0.30, potatoes 0.15 of district land.
* The guarantee sweep reports the food floor at 90, 95 and 100 percent of baseline staple production as a standing output for both beet variants, with margin per cubic metre labelled an average return, never a price.
* Two implementation choices inside the carried machinery are recorded here because the version 3 run exposed them. One: plan evaluation holds the planting through the fixed planting path of the problem builder, the path its own design note names for this evaluation. The version 2 approach of bounding the stage one variables misreported cap binding plans as infeasible on the real data, because solver values carry rounding at the cap boundary; the average year plan scored as infeasible in all three scenarios under that approach and scores correctly under this one. Two: the brute force bump inside the stochastic dual check is 0.1 percent of the district budget rather than the version 2 share of 1 percent, because on the real data a 1 percent bump crosses a kink point and understates the dual, while a 0.1 percent bump reproduces it. Both run logs print the verification values so the reader can judge the agreement.
