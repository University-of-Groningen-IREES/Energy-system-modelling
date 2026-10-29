# Python Fundamentals

Python helps us turn data and mathematical relationships into calculations
that can be repeated, checked, and extended. In energy analysis, we might
use it to calculate electricity consumption, organise technology data,
or compare different operating scenarios.

This lesson introduces the main building blocks of Python. No additional
packages are required for the examples.

Complete [Getting Ready: Miniforge](miniforge.md) and
[Python and Jupyter Basics](basics.md) before starting.

## Running Python

You can run Python in several ways:

- **A script:** save instructions in a `.py` file and execute it from a terminal.
- **An interactive interpreter:** enter instructions and immediately inspect results.
- **A Jupyter notebook:** combine executable code, explanations, and outputs in an
  `.ipynb` document.

For this lesson, create a notebook named `02-python-fundamentals.ipynb`
in Jupyter, JupyterLab or Google Colab.

Copy the examples into code cells and run them from top to bottom.
Variables remain available in the current kernel session after a cell runs.
Restarting the kernel clears those variables.

To run a script named `energy_calculation.py`, you would instead enter
this command in a terminal:

```bash
python energy_calculation.py
```

## Variables and basic types

A variable is a name referring to an object, such as a number or a piece
of text. Assignment uses a single equals sign:

```python
number_of_buildings = 12
electricity_price = 0.28
city = "Groningen"
has_heat_pump = True
```

These values have different types:

| Type | Description | Example |
|---|---|---|
| `int` | Whole number | `12` |
| `float` | Floating-point number | `0.28` |
| `str` | Text | `"Groningen"` |
| `bool` | Logical value | `True` |
| `NoneType` | The type of `None`, often used for a missing or unset value | `None` |

Inspect values and types with:

```python
print(city)
print(type(city))
print(type(electricity_price))
```

Understanding data types is essential when working with datasets because the type determines which operations are available and how they behave. For example, `12 + 3` produces `15`, whereas `"12" + "3"` produces `"123"` by joining two strings. If numerical measurements are stored as text, calculations, comparisons, and filters may fail or behave differently from what you intended. Checking data types before processing a dataset helps prevent errors and incorrect or inconsistent results.


Use `isinstance()` to check whether an object belongs to a type:

```python
isinstance(city, str)
```

The result is `True`.

### Names and comments

Choose names that describe what a value represents:

```python
annual_heat_demand_mwh = 18.5
```

Names are case-sensitive. `city` and `City` are different names.
Names cannot contain spaces or begin with a number.

Python reserves words such as `if`, `for`, and `return` for its syntax.
Also avoid assigning values to built-in names such as `print`, `list`,
or `sum`, because doing so hides those useful functions.

Comments begin with `#`:

```python
# Estimated annual electricity demand
annual_electricity_kwh = 3200
```

### Missing or unset values

Use `None` when a value has not yet been provided:

```python
installation_year = None

print(installation_year is None)
```

This prints `True`. `None` is different from zero and from an empty string.

### Attributes and methods

Objects can provide attributes and methods. An attribute gives access to
information; a method is an operation associated with an object.

For example, strings have a method that converts text to uppercase:

```python
city.upper()
```

Parentheses call the method. Writing `city.upper` without parentheses
refers to the method without executing it.

## Working with strings

Strings contain text enclosed in single or double quotes:

```python
technology = "heat pump"
```

### Clean and transform text

Methods help standardise labels before analysing data:

```python
label = "  Rooftop Solar  "

clean_label = label.strip().lower()

print(clean_label)
```

The result is:

```text
rooftop solar
```

Here, `strip()` removes leading and trailing whitespace, while `lower()`
changes letters to lowercase.

Strings are immutable: these methods return new strings rather than
changing the original one.

### Split and join text

Use `split()` to separate a string into parts:

```python
record = "building_07;residential;electricity"

fields = record.split(";")

print(fields)
```

The result is:

```text
['building_07', 'residential', 'electricity']
```

Use `join()` to combine strings with a chosen separator:

```python
description = " | ".join(fields)

print(description)
```

### Format results

An f-string inserts values into text:

```python
technology = "solar PV"
capacity_kw = 7.456

message = f"The {technology} installation has a capacity of {capacity_kw:.2f} kW."

print(message)
```

The expression `:.2f` displays the number with two decimal places.
It changes the displayed text, not the stored value of `capacity_kw`.

## Arithmetic

Python supports the following arithmetic operators:

| Operator | Operation | Example | Result |
|---|---|---|---|
| `+` | Addition | `8 + 3` | `11` |
| `-` | Subtraction | `8 - 3` | `5` |
| `*` | Multiplication | `8 * 3` | `24` |
| `/` | Division | `8 / 3` | Approximately `2.667` |
| `//` | Floor division | `8 // 3` | `2` |
| `%` | Remainder | `8 % 3` | `2` |
| `**` | Exponentiation | `8 ** 2` | `64` |

Parentheses make the intended calculation explicit:

```python
print(4 + 2 * 3)
print((4 + 2) * 3)
```

The results are `10` and `18`.

### Example: energy and cost

For a device operating at constant power:

```python
power_kw = 1.8
operating_hours = 5
price_eur_per_kwh = 0.25

energy_kwh = power_kw * operating_hours
cost_eur = energy_kwh * price_eur_per_kwh

print(f"Energy consumption: {energy_kwh:.1f} kWh")
print(f"Electricity cost: {cost_eur:.2f} EUR")
```

Python does not automatically track physical units. Here, multiplying
kW by hours produces kWh.

### Useful numerical functions

```python
print(abs(-6))
print(round(2.71828, 3))
print(min(4, 9, 2))
print(max(4, 9, 2))
```

Floating-point calculations can produce small representation errors:

```python
print(0.1 + 0.2)
```

For comparisons of calculated decimal values, a tolerance-based check
can be more appropriate than exact equality:

```python
import math

print(math.isclose(0.1 + 0.2, 0.3))
```

`math` is part of Python's standard library, so no separate installation
is needed.

## Comparisons

Comparison operators check relationships between values.

| Operator | Meaning |
|---|---|
| `==` | Equal to |
| `!=` | Not equal to |
| `<` | Less than |
| `<=` | Less than or equal to |
| `>` | Greater than |
| `>=` | Greater than or equal to |

For example:

```python
demand_kw = 6
available_power_kw = 8

print(demand_kw <= available_power_kw)
print(demand_kw == available_power_kw)
```

The results are `True` and `False`.

Assignment and comparison are different:

```python
demand_kw = 6       # Assign a value
demand_kw == 6      # Compare values
```

### Equality and identity

`==` compares values. `is` checks whether two references point to the
same object:

```python
first = [2, 4]
second = [2, 4]

print(first == second)
print(first is second)
```

The results are `True` and `False`: the lists contain equal values,
but they are separate objects.

Use `==` to compare values. Use `is None` to check whether a value
has not been provided or a result is unavailable.

For example, a building dataset may contain an unknown construction year.
We need to check for this before attempting a calculation:

```python
construction_year = None
reference_year = 2026

if construction_year is None:
    print("Building age cannot be calculated: construction year is missing.")
else:
    building_age = reference_year - construction_year
    print(f"Building age: {building_age} years")
```

Without this check, subtracting `None` from a number would raise a
`TypeError` and interrupt execution.

Checking explicitly for `None` also distinguishes an unavailable value
from valid values such as `0`, `False`, or an empty string. For example,
zero electricity consumption is different from unknown consumption.

We use `is None` because `None` is a single, special object in Python:
we are checking whether the variable refers to that object.

To check that a value is available, use `is not None`.

Later, when working with pandas, we will use its missing-data tools,
because datasets can represent missing values as `NaN` or `pd.NA`
as well as `None`.

## Boolean logic

Combine conditions using `and`, `or`, and `not`.

| Operator | Meaning for Boolean conditions |
|---|---|
| `and` | Both conditions must be true |
| `or` | At least one condition must be true |
| `not` | Reverse the truth value |

For example:

```python
battery_charge_kwh = 6
electricity_price = 0.32

can_discharge = battery_charge_kwh > 0
price_is_high = electricity_price > 0.30

print(can_discharge and price_is_high)
print(can_discharge or price_is_high)
print(not can_discharge)
```

Parentheses can make longer expressions easier to read:

```python
operate_battery = (
    (battery_charge_kwh > 0)
    and (electricity_price > 0.30)
)
```

These examples use individual values. Arrays and pandas objects require
different conventions for combining conditions, which we will introduce
in later lessons.

## Conditionals

A conditional chooses which instructions to execute.

```python
generation_kw = 9
demand_kw = 7

balance_kw = generation_kw - demand_kw

if balance_kw > 0:
    print("Generation exceeds demand.")
elif balance_kw < 0:
    print("Additional supply is needed.")
else:
    print("Generation matches demand.")
```

Python checks the conditions in order and executes the first matching
branch.

The colon starts a block. Indentation identifies which instructions
belong to that block. Use four spaces consistently.

For a simple choice, a conditional expression can fit on one line:

```python
status = "surplus" if balance_kw > 0 else "no surplus"
```

## Lists

A list stores an ordered collection of items:

```python
technologies = ["solar", "wind", "battery"]
hourly_demand_kwh = [3.0, 4.5, 2.5, 6.0]
```

### Access items

List indexing starts at zero:

```python
print(technologies[0])
print(technologies[-1])
```

These expressions return the first and last items.

A slice selects a portion of a list:

```python
print(hourly_demand_kwh[0:2])
```

The starting position is included; the stopping position is excluded.
The result is `[3.0, 4.5]`.

### Modify a list

Lists are mutable: their contents can change.

```python
technologies.append("heat pump")
technologies[0] = "rooftop solar"

print(technologies)
```

Some useful operations are:

| Expression | Purpose |
|---|---|
| `len(values)` | Count items |
| `sum(values)` | Sum numerical items |
| `values.append(item)` | Add one item |
| `values.extend(other_values)` | Add items from another iterable |
| `values.remove(item)` | Remove the first matching item |
| `values.pop()` | Remove and return the last item |
| `sorted(values)` | Return a new sorted list |
| `values.sort()` | Sort the existing list in place |
| `item in values` | Check membership |

For example:

```python
print(sum(hourly_demand_kwh))
print("wind" in technologies)
```

Avoid writing `values = values.sort()`: `sort()` modifies the list
and returns `None`.

## Loops

Loops repeat instructions.

### A for loop

A `for` loop processes items from an iterable, such as a list:

```python
for demand in hourly_demand_kwh:
    print(f"Demand: {demand:.1f} kWh")
```

Use `enumerate()` when you also need a counter:

```python
for hour, demand in enumerate(hourly_demand_kwh, start=1):
    print(f"Hour {hour}: {demand:.1f} kWh")
```

Here, we explicitly start the counter at one. List indexing still
starts at zero.

### Repeat with range

```python
for step in range(3):
    print(step)
```

This prints `0`, `1`, and `2`. The stopping value is excluded.

### A while loop

A `while` loop repeats as long as its condition is true:

```python
stored_energy_kwh = 0

while stored_energy_kwh < 6:
    stored_energy_kwh += 2

print(stored_energy_kwh)
```

The expression `+= 2` increases the current value by two.

Make sure the loop can eventually stop. If the condition remains
true indefinitely, the loop will continue until interrupted.

### List comprehensions

A list comprehension creates a list from an expression:

```python
hourly_costs_eur = [
    demand * 0.25
    for demand in hourly_demand_kwh
]

print(hourly_costs_eur)
```

It can also filter values:

```python
high_demand_values = [
    demand
    for demand in hourly_demand_kwh
    if demand > 4
]
```

## Dictionaries

A dictionary associates keys with values. It is useful for grouping
labelled information about an object:

```python
building = {
    "identifier": "B014",
    "use": "residential",
    "floor_area_m2": 125,
    "heat_demand_kwh": 14000,
}
```

Access a value using its key:

```python
print(building["floor_area_m2"])
```

Add or update entries:

```python
building["heating_system"] = "heat pump"
building["floor_area_m2"] = 130
```

### Missing keys

Accessing an absent key with square brackets raises a `KeyError`.

Use `get()` when an absent value is expected:

```python
construction_year = building.get("construction_year", None)

print(construction_year)
```

The default is returned without adding the key to the dictionary.
Avoid replacing unknown data with a plausible-looking value unless
you intend to make and document that assumption.

Check whether a key exists:

```python
print("construction_year" in building)
```

Membership checks on a dictionary examine its keys.

If you need to handle a missing key explicitly, catch the specific error:

```python
try:
    print(building["construction_year"])
except KeyError:
    print("Construction year is unavailable.")
```

### Iterate over entries

```python
for key, value in building.items():
    print(key, value)
```

## Functions

A function packages a calculation or task into reusable code.
It can accept inputs and return a result.

```python
def calculate_energy(power_kw, duration_hours):
    """Return energy in kWh for constant power in kW and time in hours."""
    return power_kw * duration_hours
```

Call the function and store its result:

```python
energy_kwh = calculate_energy(2.5, 4)

print(energy_kwh)
```

The result is `10.0`.

The names in the definition are parameters. The values supplied in
a call are arguments.

### Positional and keyword arguments

Arguments can be supplied by position:

```python
calculate_energy(2.5, 4)
```

Or by parameter name:

```python
calculate_energy(duration_hours=4, power_kw=2.5)
```

Both calls return the same result.

### Default values

A default makes an argument optional:

```python
def calculate_cost(energy_kwh, price_eur_per_kwh=0.25):
    """Return electricity cost in euros."""
    return energy_kwh * price_eur_per_kwh
```

```python
print(calculate_cost(10))
print(calculate_cost(10, price_eur_per_kwh=0.30))
```

These calls return `2.5` and `3.0`.

Keyword arguments are not automatically optional. Optionality comes
from having a default value.

### Return and print

`return` passes a value back to the caller. `print()` displays text.

```python
def display_energy(power_kw, duration_hours):
    print(power_kw * duration_hours)
```

This function displays a result but has no explicit `return`, so its
return value is `None`.

For calculations that will feed into further analysis, returning the
result is usually more useful.

## Pure functions and side effects

A pure function returns the same result for the same inputs and does
not change external state.

Our `calculate_energy()` function is pure: its result depends only
on its arguments.

A side effect changes something beyond the returned result. Examples
include modifying an input list, writing a file, or printing output.

### A function that modifies its input

```python
def add_measurement_in_place(values, new_value):
    values.append(new_value)
```

```python
measurements = [3.0, 4.5]

add_measurement_in_place(measurements, 5.0)

print(measurements)
```

The original list has changed to `[3.0, 4.5, 5.0]`.

Running the function call again adds another item. This matters in
notebooks, where cells may be executed repeatedly.

### A function that returns a new list

```python
def with_added_measurement(values, new_value):
    return values + [new_value]
```

```python
measurements = [3.0, 4.5]

updated_measurements = with_added_measurement(measurements, 5.0)

print(measurements)
print(updated_measurements)
```

The original list remains unchanged.

Both approaches can be useful. Make changes to shared data deliberate,
and prefer functions with explicit inputs and returned outputs when
writing calculations.

## Optional practice exercises

Use a separate notebook for these exercises. Add Markdown cells to
explain your reasoning and code cells to perform the calculations.

### Exercise 1: Electricity consumption

A device operates at 1.2 kW for 3.5 hours. Electricity costs
0.27 EUR/kWh.

1. Store the three inputs in variables.
2. Calculate consumption and cost.
3. Display the cost with two decimal places.
4. Check whether consumption exceeds 4 kWh.

### Exercise 2: Clean a label

Start with:

```python
label = "  Building 18; HEAT PUMP; Groningen  "
```

1. Remove leading and trailing whitespace.
2. Split the string at each semicolon.
3. Remove whitespace from each resulting field.
4. Convert the heating-system label to lowercase.

### Exercise 3: Analyse a list

Use these energy demands for six one-hour periods:

```python
demand_kwh = [2.4, 3.1, 5.6, 4.8, 2.9, 6.2]
```

1. Calculate total and average consumption.
2. Find the largest value.
3. Select the first three values.
4. Create a new list containing only values above 4 kWh.
5. Print each period number together with its consumption.

### Exercise 4: Classify a power balance

Create variables for demand and generation in kW.

Use `if`, `elif`, and `else` to report:

- A surplus when generation exceeds demand.
- A deficit when demand exceeds generation.
- A balanced system when they are equal.

Test all three cases using whole-number inputs.

### Exercise 5: Describe a building

Create a dictionary containing:

- A building identifier.
- Floor area in square metres.
- Annual heat demand in kWh.
- Heating-system type.

Calculate heat demand per square metre and store it as another entry.
Then retrieve a missing construction year using `get()`.

### Exercise 6: Write a conversion function

Write a function that converts energy from MWh to kWh.

Check that:

- `0` MWh becomes `0` kWh.
- `1` MWh becomes `1000` kWh.
- `2.75` MWh becomes `2750` kWh.

### Exercise 7: Generalise the conversion

Write a function with these parameters:

```python
convert_energy(value, source_unit, target_unit="kWh")
```

Support `Wh`, `kWh`, and `MWh`.

Hint: use a dictionary containing the number of Wh represented by
one unit of each type.

Test conversions in both directions. As an additional challenge,
raise a `ValueError` if a unit is unsupported.