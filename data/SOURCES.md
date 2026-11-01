# Data sources

Every entry states the source, what it provides, where it lives, and its pull status. Status values: to pull, pulled, cleaned.

1. FAOSTAT, Crops and Livestock Products domain. Provides Egyptian production, area harvested, and yield by crop and year. Status: to pull.
2. FAOSTAT, Prices domain, producer prices. Provides annual producer prices by crop for Egypt. Status: to pull.
3. FAOSTAT, Fertilizers by Nutrient domain. Provides fertilizer use by nutrient for Egypt. Status: to pull.
4. CAPMAS Egypt, agricultural statistics releases. Provides cropped area by governorate and crop, the district land base of the model. Status: to pull.
5. Ministry of Water Resources and Irrigation, Egypt, published figures. Provides the Nile water quota and Delta irrigation context. Status: to pull.
6. Published hydrology literature on Nile inflow variability. Provides the historical inflow range used to set the low, expected, and high scenarios. Status: to pull, candidate papers listed in the first data notebook.
7. Egyptian agronomy extension guidance and FAO publications. Provides fertilizer application rates per crop, the bridge from planted hectares to fertilizer demand. Status: to pull.
8. OpenStreetMap through the SCGraph world highways geograph. Provides the road network and pairwise distances for the routing layer. Status: available through the SCGraph package, no separate pull.
9. Egyptian fuel price, official announcements. Provides the diesel price parameter for delivery cost. Status: to pull at modelling time, with the announcement date recorded.
10. Truck operating cost per kilometre, published logistics sources. Provides the delivery cost parameter, declared as an assumption and stress tested. Status: to pull.

Rules: files land in `data/raw/` exactly as downloaded; cleaning happens only in code; if a source cannot be pulled, the gap is recorded here with the fallback the design names.
