# Numerical Analysis and Plotting

How can we apply the same calculation to hundreds of measurements?
How can we turn the results into a figure that communicates something useful?

This lesson introduces two libraries:

- **NumPy** organises numerical values into arrays and performs calculations
  on them.
- **Matplotlib** creates figures for exploring and communicating data.

We will use a small, fictional dataset describing electricity demand
in three buildings.

## Before starting

Complete [Python Fundamentals](python.md), then create a notebook called
`03-numpy-matplotlib.ipynb`.

NumPy and Matplotlib were installed when we created the course environment.
Import them in the first code cell:

```python
import numpy as np
import matplotlib.pyplot as plt
```

The aliases `np` and `plt` are conventions that make the code shorter
and easier for other Python users to recognise.

Import the libraries again whenever you start a new kernel session.

If an import fails, check that your notebook is using the course
environment before installing anything again.

## Our example dataset

Suppose we have the average electricity demand of three buildings
during four consecutive one-hour intervals.

Each row represents a building. Each column represents an interval.

| Building | Interval 1 | Interval 2 | Interval 3 | Interval 4 |
|---|---:|---:|---:|---:|
| A | 2 | 3 | 5 | 4 |
| B | 4 | 4 | 6 | 6 |
| C | 1 | 2 | 2 | 3 |

All values are average power in **kW**. These are invented measurements
for learning purposes.

Create the dataset:

```python
building_names = ["A", "B", "C"]

demand_kw = np.array(
    [
        [2.0, 3.0, 5.0, 4.0],
        [4.0, 4.0, 6.0, 6.0],
        [1.0, 2.0, 2.0, 3.0],
    ]
)

interval_hours = 1.0
interval_number = np.arange(1, 5)
```

## Understand NumPy arrays

A NumPy array is a collection of values organised along one or more
dimensions.

- A one-dimensional array can represent one building's demand over time.
- A two-dimensional array can represent several buildings over time.
- Additional dimensions can represent scenarios, years, or other categories.

Python lists can also contain nested lists. NumPy adds explicit shape
information and operations designed for numerical arrays.

### Shape, dimensions, size, and type

Inspect the dataset:

```python
print("Shape:", demand_kw.shape)
print("Dimensions:", demand_kw.ndim)
print("Number of values:", demand_kw.size)
print("Data type:", demand_kw.dtype)
```

The shape is `(3, 4)`: three rows and four columns.

| Attribute | What it tells us |
|---|---|
| `.shape` | Length of each dimension |
| `.ndim` | Number of dimensions |
| `.size` | Total number of elements |
| `.dtype` | Data type used to store the elements |

An ordinary numerical array uses one data type for all its elements.
Choosing an appropriate type matters: integer arrays cannot preserve
fractional values when those values are assigned to them.

For example:

```python
integer_values = np.array([1, 2, 3], dtype=int)
integer_values[0] = 1.8

print(integer_values)
```

The first value becomes `1`, not `1.8`.

For measurements that may contain decimals, use a floating-point array:

```python
decimal_values = np.array([1, 2, 3], dtype=float)
decimal_values[0] = 1.8

print(decimal_values)
```

Converting text to numbers also requires checking that the text contains
valid numerical values. Changing a data type does not automatically
correct invalid or inconsistent data.

## Create arrays

Several functions help construct arrays without entering every value.

```python
# Four zeros
empty_profile = np.zeros(4)

# A three-row, four-column array of ones
scaling_template = np.ones((3, 4))

# Four entries containing the same electricity price
constant_price = np.full(4, 0.25)

# Interval numbers: the stopping value is excluded
intervals = np.arange(1, 5)

# Five values, including both endpoints
capacity_options_kw = np.linspace(0, 10, 5)
```

`np.arange()` is convenient when you know the step size.
`np.linspace()` is convenient when you know the number of values.

### Reproducible random values

Random numbers can help create practice datasets:

```python
rng = np.random.default_rng(42)

practice_values = rng.uniform(0, 10, size=(3, 4))

print(practice_values)
```

The seed, `42`, makes the sequence reproducible when the generator is
created again in the same software setup.

These values are synthetic. Randomly generated data should not be
presented as observed measurements.

## Select values with indexing and slicing

For a two-dimensional array, use:

```python
array[row, column]
```

Indices start at zero:

```python
# Building B, interval 3
print(demand_kw[1, 2])
```

The result is `6.0`.

A colon selects all entries along a dimension:

```python
# All intervals for building A
print(demand_kw[0, :])

# All buildings during interval 2
print(demand_kw[:, 1])
```

Select a smaller block with slices:

```python
# Buildings A and B, first two intervals
print(demand_kw[:2, :2])
```

The stopping index is excluded.

### Views and copies

Basic slicing usually creates a view into the original array.
Changing the view can therefore change the original data.

Use `.copy()` when you need an independent selection:

```python
building_a_copy = demand_kw[0, :].copy()
building_a_copy[0] = 99

print(demand_kw[0, 0])
```

The original value remains `2.0`.

This distinction matters when preserving raw measurements.

## Vectorised operations

A vectorised operation applies a calculation to an array without requiring
you to write a Python loop for each element.

For example, suppose we have average electricity demand for four
one-hour intervals:

```python
power_kw = np.array([2.0, 3.0, 5.0, 4.0])
```

To calculate a scenario with 10% lower demand, we could process each
value separately using a loop:

```python
reduced_values = []

for value in power_kw:
    reduced_values.append(value * 0.90)

print(reduced_values)
```

With NumPy, we can express the same calculation directly:

```python
reduced_power_kw = power_kw * 0.90

print(reduced_power_kw)
```

The result is:

```text
[1.8 2.7 4.5 3.6]
```

NumPy multiplies each element by `0.90` and returns a new array.
The original `power_kw` array remains unchanged.

### Why use vectorised operations?

Vectorisation makes numerical code more concise and often easier to
read: the instruction expresses the calculation for the whole dataset.

For numerical arrays, NumPy performs many operations using compiled
implementations rather than repeatedly executing a loop in Python.
This often improves performance, particularly for large datasets.
However, performance still depends on the operation, data types,
and memory required.

Vectorisation does not mean that no iteration happens internally.
It means that NumPy handles the element-by-element work for us.

### Operations between arrays

We can also calculate with corresponding elements of two arrays:

```python
generation_kw = np.array([1.0, 4.0, 3.0, 6.0])

balance_kw = generation_kw - power_kw

print(balance_kw)
```

The result is:

```text
[-1.  1. -2.  2.]
```

Each position compares generation and demand for the same interval:

- A positive balance indicates a surplus.
- A negative balance indicates a deficit.
- Zero indicates that generation matches demand.

The arrays must have compatible shapes. Their entries must also
represent matching observations: NumPy matches positions, not timestamps
or building identifiers.

### Functions can also be vectorised

Many NumPy functions operate element by element:

```python
absolute_balance_kw = np.abs(balance_kw)

print(absolute_balance_kw)
```

This returns the magnitude of each imbalance:

```text
[1. 1. 2. 2.]
```

We can also prevent negative values in a calculated series:

```python
surplus_kw = np.maximum(balance_kw, 0)

print(surplus_kw)
```

The result is:

```text
[0. 1. 0. 2.]
```

`np.maximum()` compares corresponding values and selects the larger one.
Here, every negative balance is replaced with zero, leaving only surpluses.

### NumPy arrays behave differently from lists

The same operator can have different meanings depending on the data type:

```python
print([2, 3] * 2)
print(np.array([2, 3]) * 2)
```

The list repeats its contents:

```text
[2, 3, 2, 3]
```

The NumPy array multiplies its numerical values:

```text
[4 6]
```

This is another reason to check data types before applying calculations.

The examples below apply vectorised operations to our two-dimensional
building-demand dataset.

### Convert power to energy

Average power multiplied by interval duration gives energy:

```python
energy_kwh = demand_kw * interval_hours

print(energy_kwh)
```

Because each interval lasts one hour, the numerical values are unchanged.
The units have changed from kW to kWh.

For 15-minute intervals, the duration would be `0.25` hours.
Always check the time resolution before calculating energy.

### Compare a demand-reduction scenario

Suppose every value is reduced by 10%:

```python
reduced_demand_kw = demand_kw * 0.90

savings_kw = demand_kw - reduced_demand_kw

print(savings_kw)
```

The original array is unchanged because we assigned the calculation
to a new variable.

### Element-wise and matrix multiplication

For arrays, `*` multiplies corresponding elements.

The operator `@` performs matrix multiplication. It represents a different
calculation and requires compatible matrix dimensions.

In this lesson, our demand, price, and scaling calculations use
element-wise multiplication.

## Summarise data along an axis

A reduction combines values using an operation such as a sum,
mean, minimum, or maximum.

For our array:

- **Axis 0 represents buildings.**
- **Axis 1 represents time intervals.**

Reducing an axis combines values along that dimension.

### Total demand during each interval

Sum over buildings:

```python
total_demand_kw = demand_kw.sum(axis=0)

print(total_demand_kw)
```

The result is:

```text
[ 7.  9. 13. 13.]
```

The building dimension has been combined, leaving one value per interval.

### Energy consumed by each building

Sum energy over time:

```python
building_energy_kwh = energy_kwh.sum(axis=1)

print(building_energy_kwh)
```

The result is:

```text
[14. 20.  8.]
```

### Other summaries

```python
print("Mean power per building:", demand_kw.mean(axis=1))
print("Peak power per building:", demand_kw.max(axis=1))
print("Total energy:", energy_kwh.sum())
print("Peak combined demand:", total_demand_kw.max())
```

Be careful when describing a peak. The maximum of the combined profile
represents simultaneous demand. Adding individual building peaks can
give a different result if those peaks occur at different times.

## Broadcasting: match calculations to dimensions

Broadcasting allows certain differently shaped arrays to work together.

Suppose electricity prices vary across our four intervals:

```python
price_eur_per_kwh = np.array([0.20, 0.25, 0.40, 0.30])
```

The energy array has shape `(3, 4)`. The price array has shape `(4,)`.

```python
cost_eur = energy_kwh * price_eur_per_kwh

print(cost_eur)
```

Each column is multiplied by its corresponding interval price.
The same price schedule applies to every building.

```python
building_cost_eur = cost_eur.sum(axis=1)

print(building_cost_eur)
```

### Apply one factor per building

Now suppose each building has its own scenario factor:

```python
building_factors = np.array([0.90, 1.10, 1.00])
```

We want one factor per row. Add a dimension so its shape becomes `(3, 1)`:

```python
scenario_demand_kw = demand_kw * building_factors[:, np.newaxis]

print(scenario_demand_kw)
```

Each factor now applies across all four intervals of its building.

### Check compatibility

Broadcasting compares dimensions from right to left.
Dimensions are compatible when their lengths match or one has length one.

| Shapes | Compatible? | Interpretation |
|---|---|---|
| `(3, 4)` and `(4,)` | Yes | One value per interval |
| `(3, 4)` and `(3, 1)` | Yes | One value per building |
| `(3, 4)` and `(3,)` | No | Last dimensions differ: 4 and 3 |

A compatible shape does not guarantee a meaningful calculation.
You must also check what each axis and value represents.

Read more in the
[official broadcasting guide](https://numpy.org/doc/stable/user/basics.broadcasting.html).

## Filter values with Boolean masks

A comparison applied to an array produces an array of Boolean values:

```python
high_demand_mask = total_demand_kw > 10

print(high_demand_mask)
```

Use the mask to select the matching values:

```python
print(total_demand_kw[high_demand_mask])
print(interval_number[high_demand_mask])
```

Count matching intervals:

```python
print(np.count_nonzero(high_demand_mask))
```

Combine array conditions using `&`, `|`, and `~`:

```python
selected_intervals = (
    (total_demand_kw > 8)
    & (price_eur_per_kwh < 0.35)
)

print(interval_number[selected_intervals])
```

Use parentheses around each comparison. The scalar operators `and`
and `or` do not perform these element-wise array comparisons.

### Missing measurements

Numerical arrays often use `np.nan` for a missing floating-point value:

```python
incomplete_measurements = np.array([2.0, np.nan, 4.0])

print(np.isnan(incomplete_measurements))
print(np.mean(incomplete_measurements))
print(np.nanmean(incomplete_measurements))
```

`mean()` propagates the missing value here. `nanmean()` calculates
the mean using the available values.

Ignoring missing values changes the data supporting your result.
Record how missing observations were handled, and do not automatically
replace them with zero.

## Start plotting: Figure and Axes

Matplotlib separates the overall figure from its plotting areas:

- A **Figure** contains the whole graphic.
- An **Axes** is a plotting area containing data, labels, and other elements.

Create both with:

```python
fig, ax = plt.subplots()
```

Despite its name, one `Axes` object represents one plotting area.
It contains an x-axis and a y-axis.

We will use explicit `fig` and `ax` objects so it is clear which plot
each instruction changes.

## Plot a demand profile

A line plot helps show changes across ordered time intervals.

```python
fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")

ax.plot(
    interval_number,
    total_demand_kw,
    marker="o",
    color="tab:blue",
    label="Combined demand",
)

ax.set(
    title="Electricity demand across three buildings",
    xlabel="One-hour interval",
    ylabel="Average power (kW)",
    xticks=interval_number,
)

ax.set_ylim(bottom=0)
ax.grid(alpha=0.3)
ax.legend()

plt.show()
```

Here:

- `figsize` sets width and height in inches.
- `marker` makes the individual observations visible.
- Axis labels identify the quantities and units.
- `label` supplies the text used by the legend.
- `layout="constrained"` helps prevent overlapping labels.

The connecting lines guide the eye between interval averages.
They do not provide additional measurements within each interval.

## Compare profiles in one plot

Plot each building on the same Axes:

```python
fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")

for name, profile in zip(building_names, demand_kw):
    ax.plot(
        interval_number,
        profile,
        marker="o",
        label=f"Building {name}",
    )

ax.set(
    title="Demand profiles by building",
    xlabel="One-hour interval",
    ylabel="Average power (kW)",
    xticks=interval_number,
)

ax.set_ylim(bottom=0)
ax.grid(alpha=0.3)
ax.legend()

plt.show()
```

`zip()` pairs each building name with its corresponding row.

## Compare totals with a bar chart

A bar chart is useful for comparing separate categories.

```python
fig, ax = plt.subplots(figsize=(6, 4), layout="constrained")

ax.bar(
    building_names,
    building_energy_kwh,
    color="tab:green",
)

ax.set(
    title="Electricity consumed during the four-hour period",
    xlabel="Building",
    ylabel="Energy (kWh)",
)

ax.set_ylim(bottom=0)
ax.grid(axis="y", alpha=0.3)
ax.set_axisbelow(True)

plt.show()
```

Distinguish the quantities: this chart shows **energy in kWh**,
whereas the previous charts show **power in kW**.

## Examine a relationship with a scatter plot

A scatter plot displays pairs of observations without connecting them.

```python
fig, ax = plt.subplots(figsize=(6, 4), layout="constrained")

ax.scatter(
    total_demand_kw,
    price_eur_per_kwh,
    color="tab:purple",
    s=60,
)

ax.set(
    title="Demand and price in the example dataset",
    xlabel="Combined average power (kW)",
    ylabel="Electricity price (EUR/kWh)",
)

ax.grid(alpha=0.3)

plt.show()
```

Each point corresponds to one interval.

These four fictional observations cannot establish a general
relationship between electricity prices and demand, or demonstrate
that one causes the other.

## Create multiple subplots

Use separate plotting areas when quantities have different units.

```python
fig, axes = plt.subplots(
    2,
    1,
    figsize=(7, 6),
    sharex=True,
    layout="constrained",
)

axes[0].plot(
    interval_number,
    total_demand_kw,
    marker="o",
    color="tab:blue",
)

axes[0].set(
    title="Demand and electricity prices",
    ylabel="Average power (kW)",
)

axes[1].plot(
    interval_number,
    price_eur_per_kwh,
    marker="s",
    color="tab:orange",
)

axes[1].set(
    xlabel="One-hour interval",
    ylabel="Price (EUR/kWh)",
    xticks=interval_number,
)

for ax in axes:
    ax.grid(alpha=0.3)

plt.show()
```

`axes[0]` refers to the upper plotting area.
`axes[1]` refers to the lower one.

## Display a two-dimensional array

A heatmap represents array values using colour.

```python
fig, ax = plt.subplots(figsize=(7, 3.5), layout="constrained")

image = ax.imshow(
    demand_kw,
    aspect="auto",
    cmap="viridis",
    vmin=0,
)

ax.set_xticks(np.arange(demand_kw.shape[1]))
ax.set_xticklabels(interval_number)

ax.set_yticks(np.arange(demand_kw.shape[0]))
ax.set_yticklabels(building_names)

ax.set(
    title="Demand by building and interval",
    xlabel="One-hour interval",
    ylabel="Building",
)

fig.colorbar(image, ax=ax, label="Average power (kW)")

plt.show()
```

The colour bar explains the numerical meaning of the colours.

When comparing several heatmaps, use the same colour limits if you
want equal colours to represent equal values.

## Optional extension: a grid of scenarios

A heatmap can also display a calculated quantity for combinations
of two inputs.

For a device operating at constant power:

```python
power_options_kw = np.linspace(0, 5, 51)
duration_options_h = np.linspace(0, 8, 41)

power_grid_kw, duration_grid_h = np.meshgrid(
    power_options_kw,
    duration_options_h,
)

energy_grid_kwh = power_grid_kw * duration_grid_h
```

`meshgrid()` constructs coordinate arrays containing all combinations
of the power and duration values.

```python
fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")

image = ax.pcolormesh(
    power_grid_kw,
    duration_grid_h,
    energy_grid_kwh,
    shading="auto",
    cmap="viridis",
)

ax.set(
    title="Energy consumption at constant power",
    xlabel="Power (kW)",
    ylabel="Operating duration (h)",
)

fig.colorbar(image, ax=ax, label="Energy (kWh)")

plt.show()
```

This figure shows a calculation across hypothetical scenarios,
rather than measured data.

## Save a figure

Save through the Figure object:

```python
fig.savefig("energy_scenarios.png", dpi=300, bbox_inches="tight")
fig.savefig("energy_scenarios.svg", bbox_inches="tight")
```

These commands save the most recently assigned `fig`, which is the
scenario figure above.

- PNG is a raster image, useful for many documents and presentations.
- SVG preserves vector elements, allowing lines and text to scale clearly.

The files are saved relative to the notebook's working directory.
Use a different filename for each figure you want to preserve.

## Optional practice exercises

Create a notebook named `04-array-and-plotting-practice.ipynb`.
Use fictional data unless you explicitly identify a real data source.

### Exercise 1: Describe your array

Create an array containing:

```python
power_kw = np.array([1.5, 2.0, 3.5, 2.5, 1.0, 4.0])
```

1. Print its shape, number of dimensions, and data type.
2. Select its first two and last two values.
3. Calculate its mean and maximum.

### Exercise 2: Calculate energy correctly

Assume the values in Exercise 1 are average powers for consecutive
30-minute intervals.

1. Convert each power value into energy in kWh.
2. Calculate total energy.
3. Explain why simply summing the power values does not directly
   give energy in kWh.

### Exercise 3: Combine two buildings

Create a second six-interval demand profile.

1. Combine both profiles into an array of shape `(2, 6)`.
2. Calculate combined power for each interval.
3. Calculate total energy for each building.
4. Explain your choice of `axis` in each calculation.

### Exercise 4: Apply time-varying prices

Create six electricity prices in EUR/kWh.

1. Calculate interval costs for both buildings using broadcasting.
2. Sum costs separately for each building.
3. Check that your resulting cost array has shape `(2, 6)`.

### Exercise 5: Select constrained intervals

For the combined profile:

1. Create a mask identifying intervals above a threshold you choose.
2. Print the matching interval numbers.
3. Count those intervals.
4. Calculate their total duration in hours.

### Exercise 6: Create an informative figure

Plot both building profiles on one Axes.

Include:

- A descriptive title.
- Labels with units.
- A legend.
- Visible observation markers.
- An appropriate y-axis range.

Save the figure as a PNG.

### Exercise 7: Compare power and energy

Create a figure with two subplots:

1. A line plot of combined demand over the six intervals.
2. A bar chart of total energy consumed by each building.

Give each subplot the correct units.

### Exercise 8: Explore missing data

Replace one measurement with `np.nan` in a copy of your array.

1. Compare `mean()` and `nanmean()`.
2. Count the missing entries with `np.isnan()`.
3. Explain why ignoring a missing demand measurement may affect
   an energy total.

### Exercise 9: Explore a scenario

Assume building 1 reduces every demand value by 15%, while building 2
reduces every value by 5%.

1. Apply the factors using an array of shape `(2, 1)`.
2. Calculate energy savings for each building.
3. Plot the original and modified combined demand profiles.
4. State that the reductions are assumptions, rather than observations.

## Learn more from the libraries

For explanations and additional examples:

- [NumPy beginner guide](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [NumPy broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- [NumPy reference](https://numpy.org/doc/stable/reference/)
- [Matplotlib quick start](https://matplotlib.org/stable/users/explain/quick_start.html)
- [Matplotlib example gallery](https://matplotlib.org/stable/gallery/index.html)
- [Matplotlib documentation](https://matplotlib.org/stable/)

When exploring the Matplotlib gallery, open an example to inspect
the code and try adapting one feature at a time.