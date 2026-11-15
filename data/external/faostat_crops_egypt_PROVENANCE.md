# FAOSTAT crops domain, Egypt: provenance note for faostat_crops_egypt.csv

Written 14 November 2026. This note records where the delivered crops file came from, what it holds, and how it compares with the Our World in Data mirror it replaces. Every figure below comes from the pull itself or from arithmetic on the pulled values, and the arithmetic is named where it appears.

## Route used

* Bulk download from the FAOSTAT bulk host, file Production_Crops_Livestock_E_All_Data_(Normalized).zip, at https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_(Normalized).zip, downloaded 14 November 2026, HTTP status 200, 33,921,825 bytes as downloaded.
* Inside the archive sits one normalised data file of 545,005,770 bytes dated 23 December 2025, plus four code list files covering areas, elements, flags and items.
* Dataset identity: Production: Crops and livestock products, domain code QCL. The bulk service manifest, datasets_E.json, read on the same day, gives the QCL update date as 31 December 2025, a file size of 33,127 kilobytes and 4,209,110 rows for the full world file. The vintage of this pull is therefore the December 2025 release.
* First attempt, recorded for honesty: a shorter guessed file name without the opening word Production returned HTTP 403 with an AccessDenied error body. The full published file name above returned 200 and is the route that carried this pull. The FAOSTAT API was not used for this pull because the bulk route worked once the correct file name was used.
* Filter applied: area Egypt, area code 59, M49 code 818, and the five item codes below. Every source row for those items and for the three elements below was kept. No value was changed except the single yield unit conversion stated below.

## Items and elements

Items, with the item names exactly as printed in the source:

1. Wheat, item code 15, CPC code 0111.
2. Rice, item code 27, CPC code 0113. The prices work in this project already established that FAOSTAT item code 27 is paddy rice, so the delivered crop label is rice_paddy on that basis.
3. Maize (corn), item code 56, CPC code 0112, delivered crop label maize.
4. Sugar beet, item code 157, CPC code 01801.
5. Potatoes, item code 116, CPC code 01510.

Elements:

1. Area harvested, element code 5312, published unit ha, delivered unit hectares, values unchanged.
2. Production, element code 5510, published unit t, delivered unit tonnes, values unchanged.
3. Yield, element code 5412, published unit kilograms per hectare, delivered unit tonnes per hectare, delivered value equals the published value divided by 1,000. Both values sit in the file, in the columns value and value_as_published, with their units beside them.

## What the delivered file holds

File faostat_crops_egypt.csv holds 942 rows and 16 columns: crop, crop_faostat_item, item_code, item_code_cpc, year, element, element_code, value, unit, value_as_published, unit_as_published, flag, area, area_code, source, date_accessed. The source column on every row names the bulk file and its internal date, and the date_accessed column records the pull date on every row.

Coverage, counted from the delivered file:

1. Wheat: area harvested 64 rows, production 64 rows, yield 64 rows, covering 1961 to 2024 with no missing years. Total 192 rows.
2. Rice paddy: area harvested 64 rows, production 64 rows, yield 64 rows, covering 1961 to 2024 with no missing years. Total 192 rows. Rice has no hole in any element in this domain.
3. Maize: area harvested 64 rows, production 64 rows, yield 64 rows, covering 1961 to 2024 with no missing years. Total 192 rows.
4. Sugar beet: area harvested 64 rows and production 64 rows covering 1961 to 2024, but yield only 46 rows covering 1979 to 2024. Yield is missing for 1961 to 1978, 18 years. Total 174 rows.
5. Potatoes: area harvested 64 rows, production 64 rows, yield 64 rows, covering 1961 to 2024 with no missing years. Total 192 rows.

Sugar beet before 1979 needs one plain sentence: the source publishes area harvested of 0 hectares for every year from 1961 to 1978, small production values in most of those years (500 tonnes in 1961, 0 tonnes in 1973 to 1976 and in 1978, and 10 tonnes in 1977), and no yield at all for those years. The delivered file copies this exactly, so yield based work on sugar beet can only start in 1979 on this series.

The flag column copies the FAOSTAT flag from the source. Across the 942 rows: flag A, official figure, 898 rows; flag E, estimated value, 31 rows; flag I, value imputed by a receiving agency, 6 rows; flag X, figure from external organization, 7 rows.

Internal consistency check, my arithmetic on the delivered values: for every crop and year where yield, area and production are all present, production divided by area reproduces the published yield to within 0.00011 tonnes per hectare. The three elements are internally consistent as published.

National yields for 2023 from the direct pull, tonnes per hectare: wheat 6.7769, rice paddy 9.1529, maize 7.6235, sugar beet 50.8023, potatoes 31.4370. The series also carry 2024, one year beyond the window the model has used: wheat 6.7777, rice paddy 9.1315, maize 7.5853, sugar beet 52.4121, potatoes 30.0944.

## Comparison against the Our World in Data mirror, 2014 to 2023

Method: the mirror files in data/raw, the owid yield and production files pulled 12 November 2026, were compared year by year against the direct pull for every crop. The mirror carries yields and production only, so the area comparison uses the area implied by the mirror, production divided by yield in each year, which is the same construction the model code has used until now.

Verdict: the direct pull agrees with the mirror. No material difference exists in this window, and the mirror can be retired for these series.

Differences, stated numerically:

1. Yield, 50 crop and year pairs compared. The largest absolute difference for any crop is 0.000005 tonnes per hectare, sugar beet in 2021, direct 49.4826 against mirror 49.482605. Per crop, the largest absolute differences are wheat 0.0000007, rice paddy 0.000001, maize 0.0000005, sugar beet 0.000005 and potatoes 0.000002 tonnes per hectare. These differences sit at the level of the decimal representation the mirror files carry and change no rounded value.
2. Production, 50 pairs compared. Forty nine pairs are identical to the last digit. The single exception is wheat in 2021, direct 9,842,410.95 tonnes against mirror 9,842,411 tonnes, a difference of 0.05 tonnes. For every other crop the largest absolute difference in the window is 0 tonnes.
3. Area harvested, 50 pairs against mirror implied area. The largest absolute differences are wheat 10.17 hectares in 2016, maize 6.08 hectares in 2019, rice paddy 2.46 hectares in 2022, sugar beet 0.63 hectares in 2021 and potatoes 0.38 hectares in 2022. The largest in relative terms is 0.00073 percent of the direct area for that year. This small gap comes from the mirror yield being printed at four decimal places, not from a different area series, because the direct pull now supplies the published area itself.
4. Ten year means over 2014 to 2023, direct against mirror, tonnes per hectare: wheat 6.5745 against 6.5745, rice paddy 9.15458 against 9.154581, maize 7.37104 against 7.37104, sugar beet 52.18709 against 52.187092, potatoes 28.08669 against 28.086691. The direct pull therefore reproduces the national mean yields the model has used, printed in the project paper as 6.57, 9.15, 7.37, 52.19 and 28.09 tonnes per hectare.

## Two published values that stand out

Two values inside the comparison window look odd and stand exactly as published, because the mirror carries the identical values and both rows carry flag A in the direct pull. Maize in 2019: area harvested 1,533,571 hectares and yield 4.9513 tonnes per hectare, against 976,401 hectares and 7.7767 tonnes per hectare in 2020, with production nearly unchanged at 7,593,140 tonnes in 2019 and 7,593,175 tonnes in 2020. Sugar beet in 2020: yield 72.8148 tonnes per hectare on an area of 141,235 hectares, against 48.1588 tonnes per hectare on 254,308 hectares in 2019 and 49.4826 tonnes per hectare on 286,879 hectares in 2021. Neither value was corrected or smoothed in the delivered file. A later modelling step should decide how to treat these two years; the data layer only records that they are what FAOSTAT publishes in this vintage.
