# Problem statement

## The decision

Every season, the people who manage farming in the Nile Delta make one decision under a hard limit: how to divide a fixed water budget, and the land it serves, among competing crops and districts. A second decision follows immediately: how to move the fertilizer those plantings require from depots to the districts that need it. Today both decisions run on habit, history, and negotiation. Neither is priced.

## What it costs when it goes wrong

Water given to a low return crop in one district is water denied to a high return crop in another. The loss never appears on an invoice, so nobody is accountable for it. Fertilizer delivery repeats the pattern in money: routes follow routine, not cost, and the waste is paid in diesel and time on every trip.

## What I build

I build a system of two chained optimization models, fed by one forecasting module.

The first model allocates land and water by crop and district under three Nile inflow scenarios, low, expected, and high, using a two stage stochastic linear program. It maximises expected farm margin subject to the water budget, land limits, and minimum food production. Its dual variables state the money value of one more cubic metre of water in each district, which turns an argument about fairness into a table of values.

The forecasting module estimates next season crop prices and yields from historical series, using a regularized regression baseline against tree based models, scored by rolling backtests. Its outputs set the scenario parameters of the allocation model, and its accuracy is reported as part of the results, not hidden.

The second model takes the planting pattern the first model produces, converts it to fertilizer demand by district through published application rates, and plans delivery routes on the real road network, with distances computed through SCGraph, the MIT CTL open source logistics library. It reports cost per ton delivered against a nearest depot baseline.

## The data I use

All data is public and citable: FAOSTAT for yields, production, producer prices, and fertilizer use; Egyptian official statistics for cropped area and the water quota; published hydrology for inflow ranges; agronomy extension guidance for application rates; OpenStreetMap for the road network. Money parameters such as fuel price and truck cost per kilometre are declared as assumptions and stress tested.

## What I will report

The allocation plan and its margin against the real current pattern. The water value map. The effect of a 10 percent and a 20 percent water cut. Fertilizer demand by district and routed delivery cost per ton against baseline. Forecast accuracy from backtesting. And the limits of every claim, stated in the paper itself.

## The test that would prove me wrong

If, on historical data, the optimized allocation does not beat the actual cropping pattern in margin per unit of water by a meaningful margin, the central claim fails, and the paper says so.
