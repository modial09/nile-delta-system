# Allocating Water and Routing Fertilizer in the Nile Delta

An integrated stochastic optimization study, with a forecasting module, built on public data.

## The problem I am solving

Egypt farms the Nile Delta with a fixed and shrinking water budget, yet water and fertilizer are still allocated by habit and history rather than by value. Scarce water flows to low return crops while high return districts go short, and fertilizer delivery adds wasted cost on top of wasted water.

## The system I am building

The system answers that problem with two chained optimization models and one forecasting module.

1. Problem One, allocation. A two stage stochastic linear program that decides how much land to plant to each crop in each district and how much water each planting receives, under low, expected, and high Nile inflow scenarios. Its objective is total farm margin, subject to the water budget, land limits, and minimum food production. Its dual solution prices water by district, in money per cubic metre.
2. Problem Two, distribution. The planting pattern from Problem One implies fertilizer demand by district, using published application rates per crop. A routing model then plans delivery from depots to district collection points at the lowest travel cost, with real road distances computed through SCGraph, the open source logistics library from MIT CTL.
3. The forecasting module. A machine learning layer that forecasts next season crop prices and yields from historical series, and reports its own accuracy honestly through backtesting. Its forecast means and spreads generate the scenario parameters that Problem One consumes, so prediction supports prescription instead of replacing it.

## What the system outputs

1. An allocation plan: hectares by crop and district, with water per district under each inflow scenario
2. A water value map: the shadow price of water by district
3. A stress answer: what a 10 percent and a 20 percent water cut does to margin and food output, and which districts absorb the shock
4. Fertilizer demand by district, in tons by nutrient
5. Delivery routes with cost per ton, compared against a nearest depot baseline
6. A working paper for SSRN, this open code, and a one page plain English brief

## How I test it

1. Baseline comparison against the actual current cropping pattern in the same data
2. Backtesting on earlier years of prices and yields
3. Stress testing at reduced water budgets
4. Sensitivity analysis on prices and on the water shadow prices
5. Routing validation against known road distances on sample routes

The falsification rule is fixed in advance: if the optimized allocation cannot beat the real pattern on historical data by a meaningful margin, the thesis fails and the paper reports that.

## Repository map

* `docs/problem_statement.md` holds the one page problem statement
* `docs/design.md` holds the full design: formulations, data, testing, stakeholder plan, and timeline
* `data/SOURCES.md` lists every data source, what it provides, and its pull status
* `src/` holds the model code: `allocation_model.py`, `routing_model.py`, `forecasting.py`, `data_loading.py`
* `notebooks/` holds the working notebooks, starting with `01_first_look.ipynb`
* `paper/` holds the working paper outline and drafts

## How to run

1. Create a Python environment with Python 3.11 or later
2. Install the packages listed in `requirements.txt`
3. Pull the data files listed in `data/SOURCES.md` into `data/raw/`
4. Open `notebooks/01_first_look.ipynb` and work through the project in notebook order

## Status

Week one: repository scaffolded, design frozen, data pull in progress. Nothing in this repository is published yet. A public release with a Zenodo DOI is planned for December 2026, ahead of the January application deadline.
