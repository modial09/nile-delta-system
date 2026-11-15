# Research notes: prices and production costs for Egypt

Access date for every source in this file: 14 November 2026.
Rule applied throughout: every number below comes from a real, named, dated source, or is labelled a GAP in plain words. Nothing was invented and nothing was interpolated.

## 1. FAOSTAT producer prices, domain PP (Prices, producer prices)

### Routes tried, in the order tried

1. FAOSTAT API at fenixservices.fao.org. Both the definitions endpoint and a data endpoint for domain PP returned server error 521 on 14 November 2026. The API route failed.
2. FAOSTAT bulk download. The zip file named Prices_E_All_Data_(Normalized).zip was downloaded in full from the FAOSTAT bulk download host on 14 November 2026 (full address in the source list). HTTP status 200, size 11,684,078 bytes, file dated 9 October 2026 inside the archive. This route worked and is the route that carried every FAOSTAT series delivered here. Egypt rows were extracted from the normalised CSV (214,286,652 bytes uncompressed) by area name Egypt, area code 59.
3. Humanitarian Data Exchange mirror of the same FAOSTAT bulk service (dataset title Egypt Food Prices, resource egy_faostat_producer_prices.csv, dataset last modified 3 November 2026). The file was downloaded and compared value by value against the bulk download for all 318 annual rows delivered here. Result: zero differences. The mirror is a faithful copy of the FAOSTAT file, but the bulk download is cited as the source route because it is the publisher original.

### What the delivered file contains

File faostat_producer_prices_egypt.csv holds annual values only (the Months field equals Annual value in the source). Monthly rows exist in the source and were not averaged into annual figures, because an average built by me would be a constructed number, not a published one.
Columns: crop, year, price, unit, element, source route.
Elements delivered for each crop: Producer Price (LCU/tonne), unit Egyptian pounds per tonne; and Producer Price (USD/tonne), unit US dollars per tonne.
Item names in the source: Wheat (item code 15); Rice (item code 27); Maize (corn) (item code 56); Sugar beet (item code 157); Potatoes (item code 116).

### Coverage by crop

1. Wheat: annual producer price in pounds and in dollars, every year from 1991 to 2023, no missing years. 2023 value: 10,000 pounds per tonne; 326.5 dollars per tonne. 2022 value: 5,900 pounds per tonne.
2. Rice: annual producer price in pounds and in dollars, 1991 to 2023 with three missing years: 2019, 2020 and 2021 have no annual value in the source. 2023 value: 18,761 pounds per tonne; 612.6 dollars per tonne. 2022 value: 14,955 pounds per tonne.
3. Maize: annual producer price in pounds and in dollars, every year from 1991 to 2023, no missing years. 2023 value: 14,400 pounds per tonne; 470.2 dollars per tonne.
4. Sugar beet: FAOSTAT does carry an Egypt sugar beet producer price. Annual values in pounds and in dollars, 1991 to 2023 with three missing years: 2019, 2020 and 2021. 2023 value: 795 pounds per tonne; 26.0 dollars per tonne. 2022 value: 795 pounds per tonne. Note that this farm gate series sits far below the announced factory procurement prices in section 3 of these notes; the two series measure different things and must not be mixed.
5. Potatoes: annual producer price in pounds and in dollars, every year from 1991 to 2023, no missing years. 2023 value: 8,160 pounds per tonne; 266.4 dollars per tonne.

No annual producer price for any of the five crops is published in this FAOSTAT vintage for 2024 or 2025. Monthly producer prices in pounds exist in the same file for January to December 2024 for wheat, rice, maize and potatoes, and are recorded here as available but unused. Sugar beet has no monthly or annual price value for 2024 or 2025 in this vintage, only a producer price index value.

### Rice is paddy rice

The model needs paddy rice. The FAOSTAT item named Rice, code 27, is paddy rice: the FAO commodity definition for code 0027, titled Rice Paddy, reads in substance rice grain after threshing and winnowing, also known as rice in the husk and rough rice; and the Central Product Classification subclass 01132 is titled Rice paddy, other (not husked). The delivered rice series is therefore the paddy price and matches the model. It is not a milled rice price.

### Cross validation inside Egyptian official data

The CAPMAS bulletin in section 4 prints farm prices sourced from the Ministry of Agriculture Economic Affairs Sector. Its printed values match the FAOSTAT annual series exactly at the overlapping points checked (for example wheat 3,770 pounds per tonne in 2017, rice 3,503 in 2017, maize 2,857 in 2017, sugar beet 534 in 2017). This supports the reading that the Egyptian official farm price system is the underlying source of the FAOSTAT Egypt series.

## 2. Wheat procurement price verdict

Verdict: CONFIRMED for the 2025 harvest season. The model figure of 2,200 pounds per ardab of 150 kilograms, equal to 14,667 pounds per tonne, is correct for 2025.

Evidence, strongest first:

1. Ministry of Supply and Internal Trade, official site msit.gov.eg, April 2025. Minister Sherif Farouk announced the start of the 2025 local wheat procurement season, 15 April 2025 to 15 August 2025, at 2,200 pounds per ardab at cleanliness grade 23.5 carats, 2,150 pounds at grade 23, and 2,100 pounds at grade 22.5.
2. Ministerial Decree 46 of 2025, published in Al Waqaia Al Masriya (the Egyptian official gazette), issue 88, 19 April 2025, applying the Cabinet decision of session 13 on 2 October 2024. Article two sets the same three grade prices for wheat delivered for the General Authority for Supply Commodities. Text of the decree was republished by Al Masdar and carried by Nabd.
3. FAO GIEWS Country Brief, Egypt, reference date 6 June 2025, states the same figure: the procurement price was set at 2,200 pounds per ardab in October 2024, up from 2,000 pounds per ardab in March 2024.
4. USDA Foreign Agricultural Service, Cairo, Grain and Feed Annual EG2025 to 0009, 27 March 2025, states the same October 2024 increase from 2,100 to 2,200 pounds per ardab. Its grade wording differs slightly from the decree; the decree and the ministry announcement govern.

Neighbouring years, from the same family of sources:

1. 2024 harvest: the preliminary guaranteed price was 2,000 pounds per ardab, set on 14 March 2024 (USDA FAS Cairo, EG2025 to 0009; FAO GIEWS agrees). Equal to 13,333 pounds per tonne.
2. 2026 crop: FAO GIEWS, reference date 1 December 2025, states that in late October 2025 the government announced a procurement price of 2,350 pounds per ardab, about 330 dollars per tonne, ahead of sowing. Equal to 15,667 pounds per tonne. FAO forecast reporting republished by Milling and Baking News MEA in July 2026 states a higher later figure of 2,500 pounds per ardab for the 2026 season, up from the 2,100 to 2,200 range of the previous season. Both figures are recorded with their dates in procurement_prices_egypt.csv; they are announcements at different points of the season, not a contradiction I can resolve from public sources.

## 3. Sugar beet factory procurement price

FAOSTAT carries a farm gate series for sugar beet (section 1), and a separate announced factory procurement price also exists and is solid:

1. Season 2024/2025, deliveries from March 2025: base price 2,400 pounds per tonne of clean beet at 16 percent sugar content, before early delivery, sugar content and cleanliness bonuses. Announced by the Sugar and Integrated Industries Company for its Abu Qurqas factories and reported in Egyptian press; Cabinet price reporting for the same season gives the same 2,400 pounds per tonne. The model placeholder of 2,500 pounds per tonne is therefore close to, but not equal to, the real 2025 procurement price of 2,400.
2. Season 2025/2026: base price cut to 2,000 pounds per tonne by Cabinet decision, announced at the Cabinet press conference in Alamein in 2025 and confirmed in later reporting (Al Manassa, July 2026, describing the August 2025 cut of 16 percent to 2,000 pounds; Al Arabiya Business season reporting carried by EgyIn in 2026, giving 2,000 pounds against about 2,400 pounds in the 2025 season).
3. Supporting company evidence: Delta Sugar Company board report for the financial year ending 31 December 2025 states 2,653,108 tonnes of beet supplied in the 2025 season and a total beet value paid of 8,242 million pounds. Dividing the second by the first gives an average outlay of about 3,107 pounds per supplied tonne. That is my arithmetic on the company totals, not a price the company states; it sits above the 2,400 base price, which is consistent with bonuses being paid on top of the base, but the company does not break the difference down.

## 4. Production costs

### Main series delivered

Publisher: Central Agency for Public Mobilization and Statistics (CAPMAS), Annual Bulletin of Estimates of Income from the Agricultural Sector. The bulletin states its data source as the Ministry of Agriculture and Land Reclamation, Economic Affairs Sector. Tables 15, 16 and 17 of each edition give, per crop, total revenue per feddan, cost per feddan and net return per feddan. In both editions read, footnote 1 to those tables states that the cost includes rent. The arithmetic of every row used here was checked: total revenue minus cost equals the printed net return, exactly, for all fourteen crop and season rows delivered.
Editions read in full: 2015/2016 and 2016/2017. These are the most recent editions whose full per crop cost tables I could retrieve from public sources. Later editions of the same bulletin exist (CAPMAS issued the 2023/2024 edition on 30 November 2025), but the public press release for that edition carries only national totals, and its per crop cost tables were not publicly retrievable. That limitation is stated again in the gap list.

### Figures, as published per feddan and converted per hectare

Conversion required by the project: one feddan equals 0.42 hectares, so the per hectare figure equals the per feddan figure divided by 0.42. Both figures are in production_costs_egypt.csv.

Agricultural year 2016/2017, cost per feddan, then cost per hectare:
1. Wheat (winter): 9,019 pounds per feddan; 21,473.81 pounds per hectare.
2. Sugar beet (winter): 7,395 pounds per feddan; 17,607.14 pounds per hectare.
3. Rice (summer): 8,359 pounds per feddan; 19,902.38 pounds per hectare.
4. Maize (summer): 7,952 pounds per feddan; 18,933.33 pounds per hectare.
5. Maize (nili season): 5,897 pounds per feddan; 14,040.48 pounds per hectare.
6. Potatoes (summer): 20,804 pounds per feddan; 49,533.33 pounds per hectare.
7. Potatoes (nili season): 11,827 pounds per feddan; 28,159.52 pounds per hectare.

Agricultural year 2015/2016, cost per feddan, then cost per hectare:
1. Wheat (winter): 7,054 pounds per feddan; 16,795.24 pounds per hectare.
2. Sugar beet (winter): 6,853 pounds per feddan; 16,316.67 pounds per hectare.
3. Rice (summer): 6,153 pounds per feddan; 14,650.00 pounds per hectare.
4. Maize (summer): 5,609 pounds per feddan; 13,354.76 pounds per hectare.
5. Maize (nili season): 4,112 pounds per feddan; 9,790.48 pounds per hectare.
6. Potatoes (summer): 11,123 pounds per feddan; 26,483.33 pounds per hectare.
7. Potatoes (nili season): 6,779 pounds per feddan; 16,140.48 pounds per hectare.

Components: the CAPMAS tables give one cost figure per crop and do not break it into components. The bulletin defines production inputs in general terms (seed, chemical fertiliser, pesticides, farmyard manure and similar bought inputs) in its methodology chapter, and the footnote establishes that rent is inside the cost figure. No per crop component breakdown is published in these tables, so none is reported here.

### One later wheat figure

A government report republished by Safha1 on 30 May 2024 states that the total production cost of a feddan of wheat rose from about 14,000 pounds in 2021/2022 to about 17,000 pounds in 2022/2023, with land rent of about 4,700 pounds per feddan forming about 27.7 percent of the 2022/2023 total, and labour, machinery services and chemical fertiliser together about 54 percent; and that the 2023/2024 cost was expected to reach about 22,000 pounds per feddan. Converted: 17,000 per feddan equals 40,476.19 per hectare; 22,000 per feddan equals 52,380.95 per hectare. The 2023/2024 figure is a forecast inside that report, not an outturn, and is flagged as such in the CSV. No equivalent recent official figure was found for rice, maize, sugar beet or potatoes.

## 5. World Bank Pink Sheet crosscheck (international prices only)

Source: World Bank Commodities Price Data, the Pink Sheet. Annual averages for 2023, 2024 and 2025 were read from the edition dated 3 November 2026; the 2022 annual averages were read from the edition dated 3 September 2025, and the two editions agree on every overlapping year. Series: Wheat, US number 2 Hard Red Winter, Gulf export price; Rice, Thailand 5 percent broken, milled white rice, fob Bangkok; Maize, US number 2 yellow, fob US Gulf ports. Full values are in pink_sheet_crosscheck.csv. These are international reference prices. They are not Egyptian farm gate prices and must never be used as model prices for Egypt.

Gap check, one line per crop, using the last year in which both series exist, 2023, and converting the Pink Sheet dollar price at the rate implied by the FAOSTAT Egypt pair for 2023 (10,000 pounds divided by 326.5 dollars equals 30.63 pounds per dollar):

1. Wheat: Pink Sheet 340.4 dollars per tonne converts to about 10,426 pounds per tonne, against the FAOSTAT Egypt level of 10,000 pounds. The international level sits about 4.3 percent above the Egyptian farm gate level. Same order of magnitude; the FAOSTAT wheat series passes the sanity check.
2. Rice: Pink Sheet 553.7 dollars per tonne converts to about 16,959 pounds per tonne, against the FAOSTAT Egypt paddy level of 18,761 pounds. The Egyptian paddy level sits about 10.6 percent above the converted world milled rice benchmark, even though milled rice normally carries a milling premium over paddy. Treat the Egypt rice level as high but published; do not adjust it.
3. Maize: Pink Sheet 252.7 dollars per tonne converts to about 7,740 pounds per tonne, against the FAOSTAT Egypt level of 14,400 pounds. The Egyptian farm gate level sits about 86 percent above the converted international level. Egypt is a large maize importer with high domestic prices in 2023, so a wide gap is plausible, but it is wide and is flagged here in plain words.

## 6. Gap list, in plain words, unsoftened

1. GAP: FAOSTAT annual producer prices for Egypt stop at 2023 in the current vintage. There is no published FAOSTAT annual price for 2024 or 2025 for any of the five crops. Any 2025 price parameter in the model that claims to be a FAOSTAT annual producer price would be invented. The honest 2025 anchors that do exist are procurement prices: wheat 2,200 pounds per ardab (14,667 pounds per tonne) and sugar beet 2,400 pounds per tonne, both in procurement_prices_egypt.csv.
2. GAP: FAOSTAT annual values for rice and for sugar beet are missing for 2019, 2020 and 2021. The series has a three year hole and nothing in this research fills it from a named source.
3. GAP: production costs at recent year levels do not exist in the public record I could reach. The complete official per crop cost tables retrieved end at 2016/2017. The invented cost figures in the model (wheat 30,000, rice 42,000, maize 32,000, sugar beet 36,000, potatoes 95,000 pounds per hectare) are not confirmed by any source found, and the official 2016/2017 levels are far below all of them except that the later wheat reports (40,476 pounds per hectare for 2022/2023, and a forecast 52,381 for 2023/2024) bracket the model wheat figure from above. For rice, maize, sugar beet and potatoes there is no official cost figure more recent than 2016/2017 in this delivery. Costs at 2025 levels for all five crops remain a GAP.
4. GAP: no per crop cost component breakdown (seed, fertiliser, labour, machinery, irrigation, rent as separate lines) was found in a public official table. The CAPMAS tables give one rent inclusive total per crop. The single exception is wheat 2022/2023 in the republished government report, which names rent at about 4,700 pounds per feddan and a labour, machinery and fertiliser share of about 54 percent.
5. GAP: the Ministry of Agriculture Economic Affairs Sector cost of production studies themselves (the standalone crop cost studies) were not found as public documents. What is delivered is the same ministry data as republished inside the CAPMAS bulletin, which names the Economic Affairs Sector as its source, plus the republished government report for wheat. Anyone who needs the ministry originals will have to request them from the ministry or read them in the ministry library.
6. NOT A GAP, corrected expectation: sugar beet does have a FAOSTAT Egypt producer price (795 pounds per tonne in 2022 and in 2023), and it also has a solid announced factory procurement price (2,400 pounds per tonne for the 2025 season). The two numbers differ by a factor of three and answer different questions. The model must state which one it uses and why.

## 7. Files delivered

1. faostat_producer_prices_egypt.csv: 318 rows, annual FAOSTAT producer prices, five crops, pounds and dollars, 1991 to 2023 (rice and sugar beet missing 2019 to 2021).
2. production_costs_egypt.csv: 16 rows, CAPMAS cost per feddan as published with per hectare conversions for 2015/2016 and 2016/2017, plus the two later wheat rows.
3. pink_sheet_crosscheck.csv: 12 rows, Pink Sheet annual averages 2022 to 2025 for wheat, rice and maize, with the FAOSTAT Egypt dollar price for 2022 and 2023 alongside.
4. procurement_prices_egypt.csv: 6 rows, wheat procurement 2024, 2025 and 2026 announcements and sugar beet procurement for the 2025 and 2026 seasons, each with its basis and source.

## 8. Source list

Publisher, title, and address, copied exactly as published. Web addresses are identifiers, not prose.

1. FAO, FAOSTAT bulk download, Prices domain: https://bulks-faostat.fao.org/production/Prices_E_All_Data_(Normalized).zip
2. FAO, FAOSTAT API (returned error 521): https://fenixservices.fao.org/faostat/api/en/definitions/domain
3. Humanitarian Data Exchange, Egypt Food Prices (FAOSTAT mirror): https://data.humdata.org/dataset/cf5df9f6-ec62-43c0-942c-03b4b4b1e28b/resource/7527018f-67b5-4336-bb20-91f3ed28c52f/download/egy_faostat_producer_prices.csv
4. Ministry of Supply and Internal Trade, 2025 wheat season announcement: https://www.msit.gov.eg/?p=6360
5. CAPMAS, Annual Bulletin of Estimates of Income from the Agricultural Sector 2016/2017: https://censusinfo.capmas.gov.eg/Metadata-ar-v4.2/index.php/catalog/1527/download/5058
6. CAPMAS, Annual Bulletin of Estimates of Income from the Agricultural Sector 2015/2016: https://metadata.capmas.gov.eg/en/index.php/catalog/269/download/421
7. World Bank, Commodities Price Data (Pink Sheet), 3 November 2026 edition: https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Pink-Sheet-November-2026.pdf
8. World Bank, Commodities Price Data (Pink Sheet), 3 September 2025 edition: https://thedocs.worldbank.org/en/doc/18675f1d1639c7a34d463f59263ba0a2-0050012025/related/CMO-Pink-Sheet-September-2025.pdf
9. USDA Foreign Agricultural Service, Grain and Feed Annual, Cairo, EG2025 to 0009, 27 March 2025, and EG2026 to 0002, 11 March 2026 (apps.fas.usda.gov report downloads).
10. FAO GIEWS Country Brief, Egypt, reference dates 6 June 2025 and 1 December 2025 (cb.apps.fao.org Egypt archive).
11. FAO, Definition and Classification of Commodities, commodity 0027 Rice Paddy (openknowledge.fao.org).
12. Delta Sugar Company, board report for the financial year ending 31 December 2025 (foudalens.com disclosure copy).
13. Al Manassa, reporting on sugar beet contracting and the August 2025 price cut, July 2026 (manassa.news).
14. Safha1, republished government report on wheat costs, 30 May 2024 (safha1.com).
