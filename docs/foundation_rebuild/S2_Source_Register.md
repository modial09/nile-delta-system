# S2 source register for the Nile Delta project

Stage S2 of the foundation rebuild, written 15 November 2026. This register covers every data file in data/external, data/processed and data/raw as found on disk on this date. It supersedes data/SOURCES.md, which still describes the version 1 state and must not be cited as current.

Conventions. A checksum is the SHA256 of the file bytes as found on disk, given in full so any later copy can be tested against it. Access date means the date the project first pulled or computed the file, as recorded in the file itself or in its provenance note. Web addresses and file names are identifiers copied exactly as published, not prose. Where a field is not recorded anywhere in the project, the register says not recorded rather than guessing.

## Part 1. Files in data/external

### 1. capmas_governorate_area.csv

* Holds: cropped area by governorate, crop, season and agricultural year, 176 rows.
* Source: Agricultural Statistics Bulletins of the Economic Affairs Sector, Ministry of Agriculture and Land Reclamation, Part 1 Winter Crops and Part 2 Summer and Nili Crops, editions 2019 to 2020 through 2023 to 2024, read first hand. One series inside the file is second hand: Menoufia wheat and maize for 2021 to 2022 and 2022 to 2023, quoted from the CAPMAS bulletins by a 2025 Human and City Studies paper.
* Publisher: Ministry of Agriculture and Land Reclamation, Egypt.
* Locator: the bulletin PDFs sit in the Ministry uploads index at agri.gov.eg; the per row source identifier and table number are carried inside the file. The second hand study sits at hcsr-eg.org.
* Publication: bulletin editions for the agricultural years named in each row. Access: the 2020 to 2021 panel was extracted in the first foundation pass of 14 November 2026.
* Tables: Part 1 Table 2 for wheat, Table 12 for sugar beet; Part 2 Table 20 for rice, Table 22 for summer maize, Table 78 for potatoes across seasons; each row names its own table.
* Extraction: manual transcription from the bulletin PDFs into the CSV, one row per governorate, crop, season and year, with source identifier, table, evidence grade and data status on every row.
* Units: feddan as published; hectares converted by multiplication by 0.42.
* Checksum: a46c0e13e171be8f262eedd90e2008139c709ffc844d5c611863d41db420280a
* Used by: src/allocation_model_v4_1.py, baseline areas for wheat, sugar beet, rice and summer maize, plus the Menoufia rice fill.

### 2. capmas_governorate_production.csv

* Holds: production by governorate, crop, season and agricultural year, 176 rows, the same key set as the area file.
* Source, publisher, locator, publication, access, tables and extraction: as entry 1.
* Units: tonnes as published; no conversion.
* Checksum: 097594f57410f631d3157a7bea93d6d8d779a6e7ce1c498b5833d69ef20c7868
* Used by: no model file reads it directly. It is the check file for the panel: production against area times yield.

### 3. capmas_governorate_yield.csv

* Holds: yield by governorate, crop, season and agricultural year, 176 rows, the same key set as the area file.
* Source, publisher, locator, publication, access, tables and extraction: as entry 1. Rows in the second hand Menoufia series carry yields computed from that study's published area and production, flagged in the yield basis column as computed, never as published.
* Units: tons per feddan as published; tons per hectare converted by division by 0.42. The converted column is stored rounded, with a largest deviation from the exact conversion of 0.0005 tonnes per hectare.
* Checksum: e3232906b3d59e663e47cd736cf7aa599338f17303fdea5bf91f9db0943030c6
* Used by: src/allocation_model_v4_1.py, published district yields.

### 4. capmas_governorate_total_cropped_area.csv

* Holds: three land measures by governorate, 27 rows: total cropped area, cultivated area and zemam area, for 2019 to 2020, 2020 to 2021, 2022 to 2023 and one 2023 zemam set.
* Source: Ministry Agricultural Statistics Bulletin Part 2, 2020 to 2021, Table 19 for total cropped area and Table 17 for cultivated area; Part 2 of 2019 to 2020, Table 19; the zemam rows come from the CAPMAS zemam bulletin of 2023 as quoted in the second hand Menoufia study.
* Publisher: Ministry of Agriculture and Land Reclamation.
* Units: feddan as published; hectares by multiplication by 0.42.
* Checksum: 95b001ff427045641efa7cf1bf175d31c2d526e6fe18a8b97293664fe3d56ed7
* Used by: src/allocation_model_v4_1.py, physical cultivated area and annual cropped area for 2020 to 2021.

### 5. capmas_secondhand_isi_cropped_and_rice_area.csv

* Holds: total cropped area and rice area by governorate from a 2026 conference paper by a CAPMAS author, 8 rows.
* Status: isolated on purpose. The paper states no agricultural year and its national total contradicts the CAPMAS national figure, so the file is used nowhere. It is registered so it is not rediscovered as a shortcut.
* Checksum: b491d8625bbe38837f9a5c2785a4e785450f46cc7451360acba0c6bda4f226e7

### 6. crop_water_requirements_egypt.csv

* Holds: crop water requirement values from four source families, 21 rows, each row carrying its basis, its location basis and its source.
* Sources: Gabr (2022), Management of irrigation requirements using FAO CROPWAT 8.0 model, Modeling Earth Systems and Environment volume 8, Table 6, net requirement and evapotranspiration for the Delta territory; Abdelwahab and coauthors (2024), Acta Scientiarum Polonorum Formatio Circumiectus volume 23 issue 4, Table 3, printing water requirements sourced from CAPMAS (2017) for the Ismailia Canal area; Sallam and Abd El Nasser (2006), printing the MWRI (2003) duty tables for Lower Egypt; and a 2008 west Delta CROPWAT study in the Australian Journal of Basic and Applied Sciences, held as a check only.
* Units: millimetres per season, or cubic metres per feddan, as published; converted cubic metres per hectare by multiplication by 10 for millimetres and by division by 0.42 for per feddan values.
* Checksum: 6c8e3b84394819189b48e5ad9183d9b1719459a5b903115eedf8c31f0ccc1d9f
* Used by: no code reads this file. The model carries its values as constants in src/allocation_model_v4_1.py, transcribed from the Abdelwahab rows and from the arbitrated sugar beet range. S2 verified every constant against this file; see the data quality report.

### 7. egypt_water_budget_anchors.csv

* Holds: official Egyptian water totals and shares, 11 rows, each with publisher, publication year, address and access date of 14 November 2026 inside the file.
* Sources: MWRI Strategy for the Development and Management of Water Resources until 2050 (2016); Nile Basin Initiative (2025), Reporting the Nile Basin; CAPMAS, Egypt in Figures 2024, reached through a Scribd republication; OECD (2025), Policies for the Future of Farming and Food in Egypt; Gabr (2022); and one press report of an MWRI Senate presentation, labelled press inside the file.
* Units: billion cubic metres per year, as published.
* Checksum: 977cde1ec2c72d8c3d80fa56c5093689b30fda58ae3c02d8548315c278f60126
* Used by: no code. Context and citation only. The model area budget is a calibration and comes from none of these rows.

### 8. fao33_ky_values.csv

* Holds: seasonal yield response factors, 6 rows.
* Source: FAO Irrigation and Drainage Paper 33 (Doorenbos and Kassam, 1979) as tabulated in two secondary sources that agree: FAO Paper 56 (Allen and coauthors, 1998), Table 24, and FAO Paper 66 (Steduto and coauthors, 2012), Table 1. The 1979 original was not read.
* Values: winter wheat 1.05, spring wheat 1.15, maize 1.25, sugar beet 1.00, potatoes 1.10, and rice recorded as a gap, because neither secondary table carries a seasonal rice value.
* Units: dimensionless.
* Checksum: fa1d38c1b179fef4200bc2e4562358a67abdb8e5438d28a113b2c605298b548d
* Used by: no code reads it. The model carries the factors as constants; S2 verified them against this file.

### 9. faostat_crops_egypt.csv

* Holds: FAOSTAT Crops and Livestock Products domain for Egypt, five crops, three elements (area harvested, production, yield), 942 rows, 1961 to 2024. Sugar beet yield begins in 1979; the source publishes zero area and no yield for sugar beet before 1979 and the file copies that exactly.
* Source and publisher: Food and Agriculture Organization of the United Nations, FAOSTAT bulk download, file Production_Crops_Livestock_E_All_Data_(Normalized).zip from bulks-faostat.fao.org. The archive file inside is dated 23 December 2025 and the dataset update date in the bulk manifest is 31 December 2025, so this is the December 2025 vintage. Full provenance in faostat_crops_egypt_PROVENANCE.md beside the file.
* Access: 14 November 2026, recorded on every row.
* Extraction: filter to area Egypt, area code 59, and item codes 15 (wheat), 27 (rice, paddy), 56 (maize), 157 (sugar beet), 116 (potatoes). No value changed except the yield conversion.
* Units: hectares and tonnes as published; yield published in kilograms per hectare and converted to tonnes per hectare by division by 1000, with both values kept in the file.
* Checksum: 6d4e6337c407d1d2e82d3fe1f7b0a8784647509983272161e155c7687d933a05
* Used by: src/forecasting.py, national yield series and lagged area features.

### 10. faostat_producer_prices_egypt.csv

* Holds: FAOSTAT Prices domain, producer prices for Egypt, five crops, 318 rows: annual values 1991 to 2023 in Egyptian pounds per tonne and in US dollars per tonne. Rice paddy and sugar beet have no value for 2019, 2020 or 2021 in this vintage.
* Source and publisher: Food and Agriculture Organization of the United Nations, FAOSTAT bulk download, file Prices_E_All_Data_(Normalized).zip from bulks-faostat.fao.org, the archive file dated 9 October 2026 inside the archive. Item codes: wheat 15, rice 27 (paddy by the FAO commodity definition), maize 56, sugar beet 157, potatoes 116.
* Access: 14 November 2026.
* Extraction: downloaded in full and filtered to Egypt. A Humanitarian Data Exchange mirror of the same file was compared value by value during the first foundation pass with zero differences; the mirror was not retained, so that comparison cannot be replayed from the delivered files.
* Units: pounds per tonne and dollars per tonne, as published; no conversion.
* Checksum: ad4fb169ca1f8ac7c991e978471d702cb0fcff7d9337be962c1e3cff2fadecbd
* Used by: src/forecasting.py, price series, filtered to the pounds per tonne element in the loader.
* Vintage warning: this file is the older of the two FAOSTAT pulls on disk. The December 2025 vintage that entry 9 carries for crops was mined for prices in the second sweep and holds observed 2024 values for wheat, maize and potatoes, but no updated prices file was ever saved. See the data quality report, finding 1.

### 11. ministry_cost_bulletin_2019_2022.csv

* Holds: total production cost with and without rent, and rent, per crop and season, 16 rows: wheat and sugar beet for the winter seasons 2019 to 2020, 2020 to 2021 and 2021 to 2022; rice, summer maize, Nili maize, summer potatoes and Nili potatoes for the summer seasons 2020 and 2022. The summer 2021 edition exists in the Ministry catalogue but its PDF was not retrieved, so that season is absent.
* Source: Ministry of Agriculture and Land Reclamation, Economic Affairs Sector, Bulletin of Cost Statistics and Net Return, Part 1 for winter crops and Part 2 for summer and Nili crops. The address of each edition is carried on every row: five documents at agri.gov.eg.
* Tables: Part 1 Table 2 (wheat) and Table 9 (sugar beet); Part 2 Table 2 (rice), Table 3 (summer maize), Table 4 (Nili maize), Table 18 (summer potatoes), Table 19 (Nili potatoes).
* Access: 14 November 2026, on every row.
* Extraction: values read from the bulletin PDFs, whose text layer is garbled, and verified inside each source table by the addition check that cost without rent plus rent equals cost including rent. The check was rerun on the assembled file in S2 and passes on all 16 rows. Detail in data/external/EXTRACTIONS_1B.md.
* Units: pounds per feddan as published; pounds per hectare by division by 0.42, both kept in the file.
* Checksum: 027934fc659743dc5efe4511f0bf61656beb0677759250d24e5c4fc005aa4b3f
* Used by: no code reads it. The model carries the seven 2022 values as constants; S2 verified them to the cent against this file.

### 12. nile_inflow_aswan_series.csv

* Holds: annual flow of the Nile at Aswan, 1871 to 1970, 100 rows, no missing years.
* Source: Cobb (1978), The problem of the Nile, Biometrika volume 65, Table 1, as republished in Durbin and Koopman (2001) and distributed as the Nile data set in the R datasets package; the file copy read was the University of Auckland Rdatasets text file. The source does not state whether values are calendar year or water year totals and publishes no naturalisation method, so the series is registered as gauged flow as published.
* Units: published in units of 100 million cubic metres; converted to billion cubic metres by division by 10, both kept in the file.
* Checksum: b8de53b94307446b1cef30ba866391ad23ae3656baea266dc0edbee1e130f792
* Used by: src/allocation_model_v4_1.py, inflow states, probabilities and the robustness sampling pool.

### 13. nili_maize_governorate_2020_2021.csv

* Holds: Nili maize by governorate for 2020 to 2021, 24 rows: combined, white and yellow rows for eight governorates. Combined values are published for Beheira, Sharkia, Dakahlia and Gharbia only; Kafr El Sheikh, Menoufia, Qalyubia and Damietta are recorded as not reported in the source table, with empty value cells.
* Source: Ministry Agricultural Statistics Bulletin Part 2, 2020 to 2021, at https://www.agri.gov.eg/uploads/topics/16692385498467.pdf , Tables 27 (combined), 28 (white) and 30 (yellow). Tables 29 and 31 hold variety detail only and were not carried.
* Access: 14 November 2026, on every row.
* Extraction: read from the retrieved PDF in the Step 1b extraction. One source fault was found and resolved inside the bulletin: in the tons version of Table 27 the English governorate labels on the two smallest Lower Egypt rows are shifted, printing the Sharkia row as Damietta and the Suez row as Sharkia. The Arabic labels, the ardab version of the same table and the white plus yellow sum agree that the 241 feddan row is Sharkia. The file follows the Arabic labels. Two rounding differences of one ton stand in the published tables and are recorded in EXTRACTIONS_1B.md, not corrected.
* Units: feddan and tons per feddan as published; hectares and tons per hectare converted at 0.42.
* Checksum: 5d480fab00a51572c99e10c0c411e8e5d69a23fcedda49aa061d58a9126976f4
* Used by: src/allocation_model_v4_1.py, Nili maize baseline areas and yields.

### 14. pink_sheet_crosscheck.csv

* Holds: World Bank Commodities Price Data (the Pink Sheet), annual averages for wheat, rice and maize, 2022 to 2025, 12 rows.
* Publisher: World Bank. Editions dated 3 November 2026 and 3 September 2025, as recorded in data/DATA_FOUNDATION.md.
* Units: US dollars per tonne, international reference prices. Status: sanity check only, never an Egyptian farm gate price. The file holds no fertilizer series, which is why the forecasting module has no fertilizer feature; see the parameter dictionary.
* Checksum: 3de42e9c2c630ff7a44ffab4b44da540cdc591e36a5c33153387bd284c9f48c2

### 15. potato_season_split.csv

* Holds: potato area, yield and production by governorate and season (winter, summer, Nili) for 2021 to 2022, 24 rows, with national season costs and season water values attached to each row and labelled national in the column names.
* Source: Ministry Agricultural Statistics Bulletin Part 2, 2021 to 2022, at https://www.agri.gov.eg/uploads/topics/17172249083909.pdf , Table 75 (all seasons, used as the control total), Table 76 (winter), Table 77 (summer), Table 78 (Nili). Costs attached from entry 11, season 2022. Water attached from entry 6, the Abdelwahab rows.
* Access: 14 November 2026.
* Extraction: for every governorate, winter plus summer plus Nili area equals the Table 75 all seasons area exactly. Nili potatoes are published for Beheira only; the other seven governorates are recorded as not reported, with empty cells. Winter rows carry empty cost cells naming the winter potato cost gap; Nili rows carry empty water cells naming the Nili potato water gap.
* Units: feddan and tons per feddan as published; hectares and tons per hectare converted at 0.42.
* Checksum: f2c6ae0734d666c972eeae6173b799fac287ae26afa5f3eaa16915ec729255f2
* Used by: src/allocation_model_v4_1.py, potato baseline areas and yields in all three seasons.

### 16. procurement_prices_egypt.csv

* Holds: announced procurement prices, 6 rows: wheat for the 2024 harvest, the 2025 harvest and two 2026 announcements; sugar beet for the 2024 to 2025 and 2025 to 2026 seasons.
* Sources: Ministry of Supply and Internal Trade announcement of April 2025 and Ministerial Decree 46 of 2025 in the official gazette; USDA Foreign Agricultural Service Cairo report EG2025 to 0009 of 27 March 2025; FAO GIEWS country brief of 1 December 2025; Sugar and Integrated Industries Company announcement for the 2024 to 2025 beet season and Cabinet reporting.
* Units: pounds per ardab of 150 kilograms for wheat, converted to pounds per tonne by division by 0.15; pounds per tonne for beet at 16 percent sugar content, before bonuses.
* Checksum: ca972a92fe6df7904b0c74c66900b17df8085ef4548c95f35431d0092e4d6fe5
* Used by: no code reads it. The beet factory price of 2,400 pounds per tonne in the model is a constant that agrees with this file.

### 17. production_costs_egypt.csv

* Holds: production cost per feddan for 2015 to 2016 and 2016 to 2017, 14 rows, plus two later wheat rows (an observed 2022 to 2023 figure of about 17,000 pounds per feddan and a 2023 to 2024 forecast of about 22,000 inside the same government report), 16 rows in total.
* Source: CAPMAS, Annual Bulletin of Estimates of Income from the Agricultural Sector, Tables 15 to 17 of each edition; the bulletin names the Ministry Economic Affairs Sector as its data source, and its footnote states that cost includes rent. The two wheat rows come from a government report republished on 30 May 2024.
* Units: pounds per feddan as published; pounds per hectare by division by 0.42.
* Provenance caution: the download address for the 2016 to 2017 edition could not be reopened in the first foundation skeptic pass, so this file rests on the research pass record until the address is reopened in a full browser.
* Checksum: d1b77642225e62be5e3a05f3affde71b352eb0cd649f494618a59b9429983f01
* Used by: no current code. This is the earlier cost basis, superseded for the model by entry 11.

### 18. wapor_aeti_governorate_2018_2025.csv

* Holds: measured actual evapotranspiration and interception (AETI) by governorate and year, 2018 to 2025, 72 rows: eight governorates plus one Delta total row per year, with annual and season split volumes.
* Source: FAO WaPOR version 3, Level 2 (100 metre pixels), mapsets L2-AETI-A (annual) and L2-AETI-M (monthly), read through the FAO GISMGR 2.0 catalogue API at data.apps.fao.org on 14 November 2026. Boundaries: Egypt Subnational Administrative Boundaries (COD AB) from the Humanitarian Data Exchange, publisher OCHA with boundaries sourced from CAPMAS.
* Extraction: computed by the project script data/raw/wapor_work/wapor_zonal.py, kept with its checkpoints and run log in data/raw/wapor_work. Stored pixel values were multiplied by the catalogue scale factor of 0.1 to give millimetres. Volumes are mean depth times polygon area, with 1 millimetre over 1 hectare equal to 10 cubic metres. No cropland mask exists in the WaPOR version 3 catalogue for Egypt, so the figures are whole governorate consumption over every surface, not cropland consumption. Method and limitations in data/external/WAPOR_METHODS.md.
* Units: millimetres per year as computed; billion cubic metres as converted.
* Checksum: 638d40891e75dbbb0eacde697ea9847885780dce0bc600c06dedb9f2ecc88fd4
* Used by: src/allocation_model_v4_1.py reads it only to print a comparison table in the run header. No model parameter is derived from it. See the data quality report, finding 3.

### 19. Documentation files in data/external

* EXTRACTIONS_1B.md: extraction record for entries 11, 13 and 15, with the Arabic label fault and every named gap in those files.
* faostat_crops_egypt_PROVENANCE.md: provenance for entry 9, including the comparison against the retired mirror and the two flagged outlier years.
* WAPOR_METHODS.md: method, season convention, coverage check and limitations for entry 18.
* research_notes_capmas.md, research_notes_prices.md, research_notes_hydrology.md: the full research record of the first foundation pass, including routes tried and dead ends. These are evidence for the register entries above, not data.

## Part 2. Files in data/processed

These files are outputs, not sources. Each is registered with the code that produced it so a reader can tell a result record from an input.

* forecast_prices_yields_v4.csv: output of src/forecasting.py, 10 rows: one price forecast and one yield forecast per crop, with selected model, band and backtest errors. Run log at run_forecasting_v4.txt in the same folder. Checksum: 6a24554e9e0154b49c0a0a4a6ba6b4fc4ca4aa6ad676769623b2a7565f37c7d1. This file is a model input: src/allocation_model_v4_1.py reads it.
* backtest_scores_v4.csv: output of the same forecasting run, 100 rows of rolling origin backtest scores by crop, target, model and origin. Checksum: a6d4f61f69f9989f9cadb896e377cc68ce04acd3dbf1e50cb3c896bcef12828c
* plan_v4_1_floor50.csv, plan_v4_1_floor60.csv, plan_v4_1_floor70.csv, plan_v4_1_floor75.csv, plan_v4_1_floor80.csv: saved plans from the main run of src/allocation_model_v4_1.py, 184 rows each, areas at full precision. Checksums: 1e28478342be5ba2870b4043356e91bb89bccb7571f91ed3c0d1b16c2f970e49; 137c0b4d3d6595994a2c01257f82ec40a723055773efef187ef5c8e6c0a63633; ecbba0460b73f866b613ba460435076ccecb7276dc26478039071cab57f11f35; e55b91097a2f7719f20847039f69ba36363e86bd6b5c39184d90556e83220a3c; c2b831b1179377c95f088fb934e97e77f40a16918e817e17fd105d40fa47847a
* plan_v4_1_robust_plan.csv: the robustness plan of the same run. Its checksum, c2b831b1179377c95f088fb934e97e77f40a16918e817e17fd105d40fa47847a, is identical to plan_v4_1_floor80.csv, because the robustness plan is the floor 80 plan. The two files are byte for byte the same plan under two names.
* plan_v4_robust_plan.csv: the version 4 robustness plan, kept as the audited record of that build. Checksum: 9667827b4a96f2869db900f31276aca9de8a752613b7fdca089cd0f2970f5731
* robustness_samples_v4_1.csv: output of the robust run of src/allocation_model_v4_1.py, 100 rows, one per sampled budget, seed 20261114. Checksum: 5e83a5314aa7a76bcff45c1890a163f4452ab5b9038efb74d29acf4992d2bdeb
* plan_precision_recovery.py: the script that resaved the version 4.1 plans at full precision after the first save rounded them.
* Run logs: run_v1_output.txt, run_v2_output.txt, run_v3_beet795_output.txt, run_v3_beet2400_output.txt, run_v4_main.txt, run_v4_caps.txt, run_v4_beet2400.txt, run_v4_robust.txt, run_v4_1_main.txt, run_v4_1_caps.txt, run_v4_1_beet2400.txt, run_v4_1_robust.txt and run_forecasting_v4.txt. Each log is the printed record of one run of the matching code version.
* audit_v4_work and audit_v4_1_work: audit scripts and their JSON outputs from the two independent audits of versions 4 and 4.1. Registered here for completeness; their content belongs to stage S4.

## Part 3. Files in data/raw

* Ten Our World in Data grapher files, two per crop (yields and production), pulled 12 November 2026 as a mirror of the FAOSTAT crops domain when the FAOSTAT site itself failed. Status: retired. The direct pull of entry 9 was compared against them value by value in the provenance note and agrees to within representation rounding, so nothing in the current build reads them. They are kept as the comparison record.
* data/raw/wapor_work: the WaPOR computation record: wapor_zonal.py (the script), egy_admin1.geojson (the boundary file), annual_results.json and monthly_results.json (checkpoints), run.log. This is the reproducibility record for entry 18.

## Part 4. What the generating code actually reads

So that no reader has to guess the lineage: src/allocation_model_v4_1.py, the code that produced the paper, reads entries 1, 3, 4, 13, 15 and 12 from data/external, entry 18 for a printed comparison only, and forecast_prices_yields_v4.csv from data/processed. src/forecasting.py reads entries 9, 10 and 14. Every other file in this register is evidence, context or a superseded basis. Costs, water duties, response factors and cap shares enter the model as constants inside the code, transcribed from entries 11, 6, 8 and 16; S2 verified each constant against its file.
