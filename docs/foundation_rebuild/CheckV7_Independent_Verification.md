# Check V7: Independent Verification of the Procurement Price Extension

Date: 17 November 2026
Code checked: src/allocation_model_v7.py, src/methods_v7.py
Check code: src/check_v7.py, written separately from the build
Run record: data/processed/run_v7_check.txt

## What the check does

The check recomputes the version 7 headline numbers by paths the build did not use. The delivery response fit is recomputed with numpy polyfit against the build lstsq call. The grid arithmetic at three prices is recomputed from the saved inputs with plain arithmetic. The two announced price plans are rebuilt and replayed under HiGHS, a different solver from the CBC the build used, and their margins and expected wheat production are compared with the saved values. The saved floor plan is read from its file and its rice area is checked against the state decree directly. The Monte Carlo shares at the announced price are recomputed from the saved sample file. One break even price is recomputed directly from the parameter values.

## Verdicts, 13 of 13 pass

1. Response fit recomputed. PASS. Polyfit gives an intercept of 0.261064 and a slope of 0.168235, identical to the build values.
2. Response fit R squared. PASS. Recomputed 0.865938 against the saved 0.865938.
3. Validation 2026 underprediction stands as reported. PASS. The fitted share at the 2026 ratio is 0.4178 against an actual share of 0.4804. The check confirms the direction and size of the miss rather than hiding it; the evidence note reports the same miss.
4. Grid arithmetic at 2,200, 2,650 and 3,500 pounds per ardeb. PASS. Deliveries, bill, gap cost, carrying and total all recompute from the saved inputs.
5. Deliveries non decreasing in price. PASS. Deliveries rise at every grid step, from 4.070 million tonnes at 2,200 to 4.901 million tonnes at 3,500.
6. Bill strictly increasing in price. PASS. The bill rises at every step even though the delivered share also rises.
7. Cover and months conversion. PASS. Months equal cover times twelve at every grid row.
8. HiGHS replay of the announced price free plan. PASS. HiGHS margin 221,699,178,210 pounds against the CBC saved 221,699,177,650; expected wheat 0 tonnes under both solvers.
9. HiGHS replay of the announced price floor plan. PASS. HiGHS margin 197,007,449,422 pounds against the CBC saved 197,007,448,659; expected wheat 4,654,407 tonnes under both solvers.
10. Announced price floor plan inside the rice decree. PASS, with a note. The largest state rice area in the saved plan is 0.0 hectares against the decree bound of 451,164 hectares. The check passes with the whole bound to spare because these optimised plans plant no rice at all: at the model prices, rice earns the least per unit of water of the summer crops, so the margin seeking plans drop it. The decree binds the observed pattern, which plants 447,153 hectares; it does not bind these plans. The pass is therefore a weak test for version 7, and it is recorded as one.
11. Monte Carlo target share recomputed at the announced price. PASS. Recomputed 0.00 percent against the saved 0.00 percent over 2,000 draws.
12. Monte Carlo worst quarter cost recomputed at the announced price. PASS. Recomputed 100,533,845,324 pounds against the saved figure, exact.
13. Break even spot check, Sharkia, full delivery reading. PASS. Direct recomputation gives 4,321.21 pounds per ardeb against the saved 4,321.21.

## What the check does not establish

The check verifies arithmetic, solver agreement and internal consistency. It does not verify the delivery response against the world: that response rests on six fit seasons from a policy heavy record, and its two out of sample seasons both came in above the fitted line, as the evidence note and verdict 3 record. It does not verify the labelled assumptions (holding period, storage cost, shipping lag), which no public source prices. And it inherits every limitation of version 6, including district water split by land share and price layers with weak measured coverage. The label of version 6 stands for version 7: a numerically verified exploratory model study on a stated basis, not validated empirical evidence.
