# Extractions for Step 1b of the Nile Delta version 4 build

Date of extraction: 14 November 2026. All values in the three files below were taken from the documents named in this note. No value was invented to fill a cell. Where a source gives no value, the cell is empty in the CSV file and the gap is named in this note.

## File 1. ministry_cost_bulletin_2019_2022.csv

* Rows: 16.
* Source document: Ministry of Agriculture and Land Reclamation, Economic Affairs Sector, Bulletin of Cost Statistics and Net Return, Arabic title نشرة إحصاءات التكاليف وصافى العائد.
* Part 1, winter field and vegetable crops: wheat from Table 2 and sugar beet from Table 9, for the winter seasons 2019 to 2020, 2020 to 2021 and 2021 to 2022. Six rows.
* Part 2, summer and Nili field crops, vegetables and fruit: rice from Table 2, summer maize from Table 3, Nili maize from Table 4, summer potatoes from Table 18 and Nili potatoes from Table 19, for the summer seasons 2020 and 2022. Ten rows.
* Each row carries total cost including rent and total cost without rent, in pounds per feddan as published and in pounds per hectare converted by division by 0.42, plus rent on both bases, the source document, the source address, the table number and the date accessed.
* Every value was verified in Mining Sweep 2, Target 1, where total cost without rent plus rent equals total cost including rent inside each source table. The same addition check was run again on the assembled rows in this step and all 16 rows pass.
* Source addresses, all at agri.gov.eg: winter 2019 to 2020 Part 1, https://www.agri.gov.eg/uploads/topics/16578851521219.pdf ; winter 2020 to 2021 Part 1, https://www.agri.gov.eg/uploads/topics/16636744802811.pdf ; winter 2021 to 2022 Part 1, https://www.agri.gov.eg/uploads/topics/17163517037851.pdf ; summer 2020 Part 2, https://www.agri.gov.eg/uploads/topics/16578863234800.pdf ; summer 2022 Part 2, https://agri.gov.eg/uploads/topics/17165866014459.pdf
* Caveat carried from the sweep: the summer 2020 potato figures carry the most identification risk of the set because the text layer of the Ministry PDFs is garbled, and those two rows would benefit from one visual check of the printed page.

## File 2. nili_maize_governorate_2020_2021.csv

* Rows: 24, being eight governorates for each of three crop rows: Nili maize combined, Nili maize white and Nili maize yellow.
* Source document: Ministry of Agriculture and Land Reclamation, Economic Affairs Sector, Agricultural Statistics Bulletin, Part 2, Summer and Nili Crops, agricultural year 2020 to 2021, at https://www.agri.gov.eg/uploads/topics/16692385498467.pdf . The PDF was retrieved in this step on 14 November 2026 and Tables 27 to 31 were read in full.
* Combined Nili maize from Table 27, white Nili maize from Table 28 and yellow Nili maize from Table 30. Tables 29 and 31 give the white and yellow totals broken down by variety; they contain no governorate totals beyond Tables 28 and 30, and they contain no rows at all for Kafr El Sheikh, Menoufia, Qalyubia or Damietta, so no variety rows are carried in the CSV file.
* National check from the Table 27 total row: area 196372 feddan, yield 2.993 tons per feddan and production 587789 tons. White maize in Table 28 totals 124428 feddan and 372342 tons, and yellow maize in Table 30 totals 71944 feddan and 215448 tons. The two areas sum exactly to 196372 feddan.
* Governorates with published combined values: Beheira 12804 feddan and 35751 tons; Dakahlia 50332 feddan and 190495 tons; Gharbia 6677 feddan and 19133 tons; Sharkia 241 feddan and 556 tons.
* One source fault found and resolved inside the bulletin itself: in the tons version of Table 27 the English governorate labels on the two smallest Lower Egypt rows are shifted, printing the Sharkia row as Damietta and the Suez row as Sharkia, while the Arabic labels, the ardab version of the same table and the white plus yellow sum all agree that the 241 feddan row is Sharkia. The CSV file follows the Arabic labels and the ardab version.
* Two rounding differences of one ton stand in the published tables and are recorded, not corrected: Beheira combined production is printed as 35751 tons in Table 27 while its white and yellow parts sum to 35752 tons, and the national combined production is printed as 587789 tons while the white and yellow national totals sum to 587790 tons.

## File 3. potato_season_split.csv

* Rows: 24, being eight governorates for each of the winter, summer and Nili seasons.
* Areas, yields and production by governorate and season come from the Ministry of Agriculture and Land Reclamation, Economic Affairs Sector, Agricultural Statistics Bulletin, Part 2, Summer and Nili Crops, agricultural year 2021 to 2022, at https://www.agri.gov.eg/uploads/topics/17172249083909.pdf . The PDF was retrieved in this step on 14 November 2026. Winter potatoes from Table 76, summer potatoes from Table 77 and Nili potatoes from Table 78. Table 75, all seasons, was used as the control total.
* Reconciliation: for every one of the eight governorates, winter area plus summer area plus Nili area equals the all seasons area in Table 75 exactly. The eight governorate areas are winter 143926 feddan, summer 96139 feddan and Nili 1252 feddan, summing to 241317 feddan. National totals in the same tables are winter 366878 feddan, summer 170350 feddan and Nili 47656 feddan, summing to the all seasons national total of 584884 feddan.
* The only Delta governorate with a Nili potato row in Table 78 is Beheira, at 1252 feddan and 9527 tons, which is also the whole Lower Egypt total in that table.
* Costs by season are national general average values from the cost bulletin in File 1, season 2022, attached to each governorate row of the matching season and labelled national in the column names: summer potatoes from Table 18 and Nili potatoes from Table 19.
* Water by season is applied water from the CAPMAS 2017 printing held in crop_water_requirements_egypt.csv: winter 1713 cubic metres per feddan, equal to 4079 cubic metres per hectare, and summer 2581 cubic metres per feddan, equal to 6145 cubic metres per hectare.

## What could not be retrieved, and why

* The summer 2021 Part 2 edition of the cost bulletin. It is listed in the Ministry catalogue but its PDF was not retrieved in Mining Sweep 2, where the catalogue item was login gated and targeted searches returned only the summer 2020 and summer 2022 PDFs. It is outside the season set requested for File 1, which names summers 2020 and 2022, and it is named here so the hole in the cost series stays visible. The named route that remains is a signed in Ministry library session.
* No other retrieval failed in this step. Both statistics bulletin PDFs named above were retrieved in full and read at the tables named.

## Every named gap created or carried in these files

* Gap 1b A, winter potato cost: no winter potato table exists in Part 1 of the Bulletin of Cost Statistics and Net Return; potatoes appear only in Part 2, as summer and Nili crops. In potato_season_split.csv the cost cells on all winter rows are empty and the cost source column names this gap. No winter cost was derived from the summer or Nili figures.
* Gap 1b B, Nili potato water: no Nili potato water figure exists in crop_water_requirements_egypt.csv or in the foundation. In potato_season_split.csv the water cells on all Nili rows are empty and the water source column names this gap.
* Gap 1b C, summer 2021 costs: no cost row for summer or Nili 2021 exists in ministry_cost_bulletin_2019_2022.csv, for the retrieval reason given above.
* Gap 1b D, Nili maize not reported for four governorates: Kafr El Sheikh, Menoufia, Qalyubia and Damietta have no row in Tables 27, 28 or 30 of the 2020 to 2021 bulletin, and Gharbia also has no row in the white maize Table 28. Those cells are empty in nili_maize_governorate_2020_2021.csv with data status not reported in source table. They are recorded as absences in the source, never as zero.
* Gap 1b E, Nili potatoes not reported for seven governorates: in Table 78 of the 2021 to 2022 bulletin, Sharkia, Dakahlia, Kafr El Sheikh, Gharbia, Menoufia, Qalyubia and Damietta have no Nili potato row. Those cells are empty in potato_season_split.csv with area data status not reported in source table. The season areas for those governorates still reconcile to Table 75 through winter plus summer alone.
* Gap 1b F, cost series ceiling: the Ministry catalogue for the cost bulletin ends at 2022, as recorded in Mining Sweep 2, so no official cost values for 2023 onward exist in these files and none were estimated.
