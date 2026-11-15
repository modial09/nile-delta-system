# Pricing the Food Guarantee: A Stochastic Water Allocation Model for the Nile Delta

I am Mohamed Diallo. This repository holds my applied project for graduate study in business analytics: a two stage stochastic water allocation model for eight Nile Delta governorates and five crops, built to price a staple food guarantee level by level.

## The question

Egypt divides a fixed share of Nile water among districts and crops every season. I ask what it costs, in expected farm margin, to promise that aggregate wheat, paddy rice and summer maize tonnage holds at a stated share of its current level in every water and price state the model represents, and what one more cubic metre of water earns in each governorate at the margin.

## What the model does

Planting is decided at two points. Winter planting is fixed before the inflow state is known. Summer and Nili planting respond to the observed state. Land binds by season against physical cultivated area, with a reserve held for crops outside the model. A planted crop may be abandoned in a bad state, taking no water and no output, with its cost already sunk. The guarantee is a hard floor in every scenario. A forecasting module supplies prices and yields: ridge, random forest and gradient boosting models raced against simple baselines on rolling backtests, with every error printed. On prices, no learning model beat the drift line, and the paper says so.

## Data

Ministry of Agriculture bulletins for land, cropping pattern and district yields, read first hand in Arabic. The ministry cost bulletin through 2022 for costs. FAOSTAT for prices, with observed 2024 values for wheat, maize and potatoes. The gauged Aswan inflow record, 1871 to 1970, for water states. FAO WaPOR satellite consumption as a validation comparison only. Every input carries its source, year and unit in the data appendix of the paper and in docs/foundation_rebuild/S2_Parameter_Dictionary.md.

## What version 5 found

These are verified model results on a stated basis: forecast 2025 prices, official 2022 costs, a calibrated water anchor of 11.00 billion cubic metres for the model area. They are not measurements of Egypt.

The highest guarantee the model holds in every scenario is 82.41 percent of the reference tonnage. The 80 percent level costs 268,610,886,052 pounds of expected margin against the same model left free. The pattern Egypt actually plants holds the 65 percent level and fails from 70. Under market sanity caps on crop areas, the 75 percent guarantee costs 32,666,817,585 pounds and the capped ceiling is 79.50 percent. A tenth less water deletes the 80 percent rung entirely. Full results sit in paper/Results_Note_v5.md and the addendum runs in data/processed/.

## Verification

This project has been audited four times: an internal audit, an independent audit brief I commissioned, and in November 2026 two blind independent checks run for the foundation rebuild, one numerical and one a domain critique, followed by a blind verification of the repaired build. The checks killed real claims. The earlier statement that the historical pattern holds no guarantee at any level was false and is corrected above. The full record, including every failure, is in docs/foundation_rebuild/ and paper/.

## What is not here

An earlier design chained a fertilizer routing model on top of the allocation model. I cut it to protect the core, and it is not in this repository as working code. No interface has been built. The paper in paper/ is the November 2026 version whose numbers version 5 supersedes; the results note and the research memo are the current documents.

## Limits I state wherever the numbers travel

The water anchor is a calibration, not a published release series. Prices and costs stand on different years, bridged in sensitivity runs by labelled assumed factors. The low and high price and yield layers carry nominal probabilities; their measured coverage is weaker than their construction. The uncapped optima plant potatoes far beyond any market, so the capped ladder is the implementable price list. No Egyptian irrigation specialist has reviewed the work yet; Professor Anusha of Hult reviews it next, before it goes anywhere else.

## Reproduce

Install the requirements in requirements.txt, then run src/forecasting_v5.py and src/allocation_model_v5.py. The runs regenerate the saved result files exactly, which the independent verification confirmed.
