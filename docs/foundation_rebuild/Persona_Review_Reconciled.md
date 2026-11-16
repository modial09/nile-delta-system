# Persona review, reconciled note

Two independent reviewers built the same persona separately: an expert data analyst who has worked on Delta farms and inside the Ministry of Agriculture. Their full reviews are Persona_Review_A.md and Persona_Review_B.md in this folder. This note records where they agree, where one of them missed a file, and the joint verdict.

## Where both agree

1. The water geography is constructed, not measured. The 11.00 BCM anchor is split across governorates by land share, so every district holds the same water per hectare by construction. Canal releases, drainage reuse and groundwater do not enter. The governorate water value table therefore ranks the split rule, not scarcity.

2. The scenario probabilities describe the river before the High Dam. The inflow weights are frequencies of the gauged Aswan record of 1871 to 1970. Since the dam, annual water is a release decision buffered by Lake Nasser storage, and the live risk is a run of dry years against storage. The model holds no storage variable.

3. Rice and berseem are the two crops the model understands least. Rice area is fixed by the state each year and rice washes salt in the northern Delta; the model floats it under an invented cap. Berseem, the largest winter planting and the real rival to wheat, is not a crop in the model; it sits inside a reserve formula.

4. The headline question is not one an Egyptian decision maker can act on. No institution can set, buy or enforce a guarantee on aggregate tonnes of mixed crops, with paddy counted unmilled and feed maize counted as food. The state keeps its food promise through imports and strategic stocks, measured in months of consumption cover. The model prices only the field leg and omits the instrument the state uses first, so the guarantee cost is overstated by that omission.

5. The money basis is mixed and the weights are weak. Prices are a 2025 forecast, costs are official 2022, across a large devaluation, bridged only by assumed multipliers. Measured price band coverage runs from 0.0 percent to 22.2 percent against a 50 percent construction value, so the expected figures rest on weights the work itself refutes.

6. What survives in both readings: the seasonal land accounting, the abandonment structure, the corrected finding that the current planting pattern holds 65 percent, and the Arabic source work underneath the data.

## Where one review missed a file

Review A states the capped ladder was never repriced at the lower water anchors. That run exists: results_v5_2_capped_scaled.json holds the capped ladder at scale 0.90 and scale 0.80, and its finding is that the capped 75 percent guarantee survives neither cut. The point that stands is narrower: those capped scaled results are computed but are not printed in the memo.

## Joint verdict

Fit to send to a professor as a numerically verified exploratory study. Not fit to present to an Egyptian decision maker as a price list. The three demanded repairs, in order: rebuild the water side in objects that exist (managed releases with storage, district supply split into canal, reuse and groundwater, or work at Delta level and cut the governorate water value table); put the real instruments in (the rice decree as the rice bound, berseem as a winter crop, wheat split between procurement and market prices) and price the import leg beside the field leg; restate money on one year, round memo figures, and reframe the headline in wheat self sufficiency and months of consumption cover.
