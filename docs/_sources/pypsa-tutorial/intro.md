# PyPSA Tutorial

Use Python to describe a small electricity system, optimise its operation, and explore investment choices. Complete the Python, NumPy, pandas, and Matplotlib lessons first.

## Your task

Install the PyPSA course environment and work through the two notebooks. Before changing a parameter, predict its effect. After solving, support your explanation with both a numerical table and an operational figure.

## Learning objectives

- Relate model inputs to physical components and units.
- Read dispatch, capacity, costs, and prices without confusing them.
- Test one changed assumption against a fixed baseline.
- Identify conclusions that depend on the model boundary and time resolution.

## How to work through this tutorial

Start by setting up your Python environment. Then complete the three exercises in order: 1\) Simple dispatch problem, 2\) ELectricity markets, and 3\) Investment and storage. 

1. [Installation](installation.md) — Set up the environment and check that PyPSA
   and the solver work.
2. [Simple dispatch problem: Groningen city](01-simple-dispatch-problem-groningen-city.ipynb)
   — Meet demand at one bus using generators with fixed capacities.
3. [Electricity markets](02-electricity-markets.ipynb)
   — Connect two zones and explore how a transmission limit affects dispatch,
   electricity prices, and congestion rent.
4. [Investments and storage](03-investments-and-storage.ipynb)
   — Choose solar and battery capacities for a data centre, then compare how
   cheaper grid electricity and cheaper batteries change the result.

The two notebooks contain saved figures. Use the download menu on their pages to obtain a notebook and run it with **Python (pypsa-course)**. The website is a readable, static version; it does not execute edits made in your browser.
