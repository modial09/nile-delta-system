# Nile Delta wheat study

I am Mohamed Diallo. This repository holds my applied project for graduate study in business analytics. I study wheat in the Nile Delta with two linked models. The first allocates land and water across eight governorates when the season inflow is still uncertain, and asks what it costs to hold wheat production at a promised share of national consumption in every state the model represents. The second treats the state procurement price as a choice and estimates how much wheat farmers deliver to the state at each candidate price, and what the buying programme then costs.

## What is in the folders

- `src/` holds the model code, described below.
- `data/external/` holds the input tables, all from public sources.
- `data/processed/` holds files the runs produce, plus the forecast table the allocation model reads.
- `notebooks/` holds a first look at the data.
- `paper/` holds the written documents and the script that builds them.

## The code

- `forecasting.py` forecasts next season prices and yields from the historical series, scores itself with rolling backtests, and writes the forecast table.
- `allocation_model.py` builds the allocation model, a two stage stochastic linear programme in PuLP. Winter planting is chosen before the inflow state is known, later planting adjusts, and a wheat floor can be imposed in every scenario so its cost in expected farm margin can be read level by level.
- `procurement_model.py` adds the delivery response and the price grid on top of the allocation model.
- `methods.py` runs the Monte Carlo replay, the ten year backtest and the break even sensitivity for the allocation results.
- `procurement_methods.py` runs the same kind of testing for the price results.
- `user_template.py` reads an optional input template, so a reader can supply district figures of their own and rerun with them. With no template supplied, the model runs on the data in `data/external/`.
- `check_v6.py` and `check_v7.py` are the checking routines the papers describe. They reread the saved results and test the headline numbers by separate routes.
- `data_loading.py` and `routing_model.py` are earlier working files I keep for reference.

## How to run

Install the packages in `requirements.txt`, then from the project root:

```
python src/forecasting.py
python src/allocation_model.py
python src/procurement_model.py
```

Results are written to `data/processed/`. The methods and check scripts run the same way, after the models.

## Data

The inputs are public. Egyptian official statistics carry the land, cropping pattern, yield and cost figures: CAPMAS tables and Ministry of Agriculture bulletins, with the cost bulletin running to 2022. FAOSTAT carries the producer price and crop series. The water states come from the gauged Aswan inflow record. FAO WaPOR satellite figures are used as a comparison only. `data/SOURCES.md` lists what came from where, file by file.

## The papers

`paper/Academic_Paper.pdf` is the main paper. `paper/Larson_Paper.pdf` is a shorter account written for a methods reader, `paper/Ministry_Brief.pdf` is a two page brief for a policy reader, and `paper/User_Walkthrough.pdf` explains the project in plain language. The Markdown sources sit beside the PDFs, and `paper/build_papers.py` rebuilds the HTML and PDF files from them.

## A note on status

This is exploratory research. Every number is a model result on stated assumptions and a stated data basis, not a measurement of Egypt, and the papers say plainly where the evidence is thin, including where my own checks failed. I am glad to receive criticism of the model and the data choices.
