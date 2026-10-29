# pandas: From Weather Data to Energy Indicators

Weather datasets contain more than numbers. Each observation has a time,
a variable name, a unit, and a geographical context.

**pandas** helps us preserve these relationships while selecting,
cleaning, combining, and analysing data.

In this lesson, we download weather data for Groningen, estimate wind
and solar generation, and calculate capacity factors. Along the way,
we learn how to work with labelled tables and time series.

The generation models are simplified teaching examples. They are not
validated models of particular installations.

## Before starting

Complete the Python and NumPy lessons, then create a notebook called
`pandas-weather.ipynb`.

Run the examples in order:

```python
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

The download tools belong to Python's standard library. No additional
download package is required.

## Series: values with labels

A pandas **Series** is a one-dimensional collection of values with
associated index labels.

Consider the capacities of three hypothetical PV installations:

```python
capacity_kwp = pd.Series(
    {
        "Library": 45.0,
        "Sports centre": 120.0,
        "School": 75.0,
    },
    name="capacity_kwp",
)

capacity_kwp
```

Each installation name is an index label. Each associated value is a
capacity in kWp.

Select a value by label with `.loc`:

```python
capacity_kwp.loc["School"]
```

Select by position with `.iloc`:

```python
capacity_kwp.iloc[0]
```

Positions start at zero.

Calculations preserve the labels:

```python
expanded_capacity_kwp = capacity_kwp * 1.20

expanded_capacity_kwp
```

### Label alignment

When combining Series, pandas matches their index labels rather than
assuming their positions correspond.

```python
expansion_kwp = pd.Series(
    {
        "School": 10.0,
        "Library": 5.0,
        "Sports centre": 20.0,
    }
)

capacity_kwp + expansion_kwp
```

The values are matched by installation name despite the different order.

This helps combine independently organised datasets. However, labels
that do not match can introduce missing values.

Use `.to_numpy()` if you explicitly need the underlying values without
their pandas labels:

```python
capacity_kwp.to_numpy()
```

## DataFrames: labelled tables

A **DataFrame** contains columns sharing a row index. Different columns
can contain different data types.

```python
installations = pd.DataFrame(
    {
        "site": ["Library", "Sports centre", "School"],
        "capacity_kwp": [45.0, 120.0, 75.0],
        "district": ["Centre", "North", "North"],
        "commissioning_year": [2021, 2023, None],
    }
).set_index("site")

installations
```

Inspect the table:

```python
installations.info()
installations.describe()
```

Select one column to obtain a Series:

```python
installations["capacity_kwp"]
```

Select several columns to obtain a DataFrame:

```python
installations[["capacity_kwp", "district"]]
```

Select particular rows and columns:

```python
installations.loc[
    ["Library", "School"],
    ["capacity_kwp", "district"],
]
```

Transpose the table to exchange rows and columns:

```python
installations.T
```

## Download weather data for Groningen

We will request historical weather for **2025** at a point near
Groningen's city centre:

- Latitude: `53.2194`
- Longitude: `6.5665`

We use the
[Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
with the ERA5 weather model.

These are gridded historical weather estimates, not observations from
a station at the exact coordinates. A single point does not represent
all spatial variation across the municipality.

### Weather variables and units

| API variable | Meaning | Requested unit |
|---|---|---|
| `temperature_2m` | Air temperature at 2 m | °C |
| `wind_speed_100m` | Wind speed at 100 m | m/s |
| `shortwave_radiation` | Global horizontal irradiance | W/m² |
| `global_tilted_irradiance` | Irradiance on the selected panel surface | W/m² |

For the solar example, we assume a fixed panel tilt of **35°** with
a south-facing orientation.

In Open-Meteo's convention, azimuth `0°` means south. Always check this:
other libraries can use different orientation conventions.

### Build the request

```python
data_directory = Path("data")
data_directory.mkdir(exist_ok=True)

parameters = {
    "latitude": 53.2194,
    "longitude": 6.5665,
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "hourly": ",".join(
        [
            "temperature_2m",
            "wind_speed_100m",
            "shortwave_radiation",
            "global_tilted_irradiance",
        ]
    ),
    "models": "era5",
    "wind_speed_unit": "ms",
    "timezone": "GMT",
    "tilt": 35,
    "azimuth": 0,
}

url = (
    "https://archive-api.open-meteo.com/v1/archive?"
    + urlencode(parameters)
)

print(url)
```

We explicitly request wind in m/s. Supplying km/h to a model expecting
m/s would produce incorrect generation estimates.

We request UTC timestamps to avoid daylight-saving changes in the
downloaded time index.

### Download and preserve the response

```python
raw_file = data_directory / "groningen_2025_weather.json"

if raw_file.exists():
    payload = json.loads(raw_file.read_text(encoding="utf-8"))
else:
    with urlopen(url, timeout=120) as response:
        payload = json.load(response)

    raw_file.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

request_file = data_directory / "groningen_2025_request.json"

request_file.write_text(
    json.dumps(
        {"url": url, "parameters": parameters},
        indent=2,
    ),
    encoding="utf-8",
)
```

The saved response is reused when the cell runs again. This avoids
repeated downloads.

Change the cache filename if you change the location, year, or request
settings.

Inspect the metadata:

```python
print("Returned coordinates:", payload["latitude"], payload["longitude"])
print("Units:", payload["hourly_units"])
```

The returned coordinates can differ from those requested because the
data represent a weather-model grid.

## Convert the response into a DataFrame

The hourly response contains a dictionary of arrays:

```python
weather = pd.DataFrame(payload["hourly"])

weather.head()
```

Rename the columns to make their meanings and units explicit:

```python
weather = weather.rename(
    columns={
        "time": "timestamp",
        "temperature_2m": "temperature_c",
        "wind_speed_100m": "wind_100m_ms",
        "shortwave_radiation": "ghi_wm2",
        "global_tilted_irradiance": "poa_wm2",
    }
)
```

Here:

- `ghi` means global horizontal irradiance.
- `poa` means plane-of-array irradiance: radiation on the assumed
  panel surface.

### Create a time index

```python
weather["timestamp"] = pd.to_datetime(
    weather["timestamp"],
    utc=True,
)

weather = weather.set_index("timestamp").sort_index()

weather.head()
```

The rows now have a `DatetimeIndex`, supporting time-based selection,
grouping, and aggregation.

## Inspect data before calculating

Check the table's structure:

```python
print(weather.shape)
print(weather.dtypes)

weather.info()
```

Inspect summary statistics:

```python
weather.describe()
```

Count missing entries:

```python
weather.isna().sum()
```

### Check data types

A column containing `"10"` stores text, whereas one containing `10.0`
stores a number.

Calculations, sorting, and filtering depend on these types. A calculation
can fail or behave unexpectedly if numerical measurements are stored
as text.

Require numerical values:

```python
for column in weather.columns:
    weather[column] = pd.to_numeric(
        weather[column],
        errors="raise",
    )
```

`errors="raise"` stops when a value cannot be converted.

Using `errors="coerce"` would replace unconvertible entries with missing
values. If you use that option, inspect which entries were affected.

### Check timestamps and completeness

```python
expected_index = pd.date_range(
    "2025-01-01",
    "2026-01-01",
    freq="h",
    inclusive="left",
    tz="UTC",
)

if not weather.index.is_unique:
    raise ValueError("Duplicate timestamps found.")

if not weather.index.equals(expected_index):
    raise ValueError("Unexpected or missing hourly timestamps.")

if weather.isna().any().any():
    raise ValueError("Investigate missing weather values before continuing.")

nonnegative_columns = ["wind_100m_ms", "ghi_wm2", "poa_wm2"]

if weather[nonnegative_columns].lt(0).any().any():
    raise ValueError("Unexpected negative wind speed or irradiance.")

print("Hourly records:", len(weather))
```

A complete non-leap year contains 8,760 hourly records.

Zero irradiance at night is expected. Missing irradiance is a different
condition and should not automatically be replaced with zero.

### Understand interval timing

The API's radiation variables are averages over the preceding hour.
Wind speed and temperature are supplied at the indicated timestamp.

For this introductory model, we treat each wind observation as
representative of the corresponding hourly interval.

Our analysis follows the API's timestamp labels. A strict calendar-boundary
radiation total would require an additional boundary record and explicit
alignment of interval starts or ends.

## Handle missing data deliberately

Missing data indicate that information is unavailable. They do not
automatically represent zero.

For example:

```python
installations["commissioning_year"].isna()
```

An unknown commissioning year does not mean that the installation
was commissioned in year zero.

Create a subset containing known years:

```python
known_years = installations.dropna(
    subset=["commissioning_year"]
)
```

This returns a new table without changing `installations`.

For text labels, a descriptive replacement can sometimes be appropriate:

```python
display_table = installations.copy()

display_table["district"] = (
    display_table["district"].fillna("Unknown")
)
```

### Forward filling

Forward filling carries the previous available value into a missing entry:

```python
example = pd.Series([5.0, np.nan, 7.0])

example.ffill()
```

This assumes that carrying a previous value forward is reasonable.
That assumption is not automatically valid for changing weather conditions.

Interpolation also introduces estimated values rather than recovering
the original observations. Document any treatment of missing data.

## Select, sort, and filter observations

Select January:

```python
january = weather.loc["2025-01"]
```

Select a date range and particular columns:

```python
summer_week = weather.loc[
    "2025-06-01":"2025-06-07",
    ["temperature_c", "wind_100m_ms", "poa_wm2"],
]
```

Select by position:

```python
weather.iloc[:24, :2]
```

Find the five highest wind-speed records:

```python
weather.nlargest(5, "wind_100m_ms")
```

Sort explicitly:

```python
weather.sort_values(
    "wind_100m_ms",
    ascending=False,
).head()
```

### Combine filtering conditions

```python
selected_hours = weather.loc[
    (weather["wind_100m_ms"] >= 8)
    & (weather["ghi_wm2"] >= 250)
]
```

Use parentheses around each comparison.

- `&` combines conditions using “and”.
- `|` combines them using “or”.
- `~` reverses a Boolean condition.

An alternative is `query()`:

```python
wind_threshold = 8

weather.query(
    "wind_100m_ms >= @wind_threshold and ghi_wm2 >= 250"
)
```

The `@` symbol refers to a Python variable outside the table.

## Vectorised operations with columns

A vectorised expression performs a calculation on a whole Series
without requiring an explicit Python loop over its values.

Convert wind speed to km/h:

```python
weather["wind_100m_kmh"] = weather["wind_100m_ms"] * 3.6
```

Each observation is multiplied by the same conversion factor,
while its timestamp is preserved.

### Irradiance and irradiation

These quantities have different units:

- **Irradiance:** power per area, measured in W/m².
- **Irradiation:** energy per area over a period, measured in Wh/m²
  or kWh/m².

Convert hourly mean irradiance into interval irradiation:

```python
interval_hours = 1.0

weather["ghi_kwh_m2"] = (
    weather["ghi_wm2"] * interval_hours / 1000
)

weather["poa_kwh_m2"] = (
    weather["poa_wm2"] * interval_hours / 1000
)
```

The multiplication by hours converts power per area into energy per area.
Dividing by 1,000 converts Wh/m² into kWh/m².

Remove a derived column when it is no longer needed:

```python
weather = weather.drop(columns=["wind_100m_kmh"])
```

## Estimate normalised wind generation

Wind speed must be translated into electrical output through a turbine
power curve.

We use an illustrative model with:

| Parameter | Assumption |
|---|---:|
| Hub height | 100 m |
| Cut-in speed | 3 m/s |
| Rated speed | 12 m/s |
| Cut-out speed | 25 m/s |

The model produces:

- Zero output below cut-in.
- Increasing output between cut-in and rated speed.
- Rated output between rated speed and cut-out.
- Zero output at and above cut-out.

```python
cut_in_ms = 3.0
rated_ms = 12.0
cut_out_ms = 25.0

speed = weather["wind_100m_ms"]

weather["wind_cf"] = 0.0

rising = (speed >= cut_in_ms) & (speed < rated_ms)

weather.loc[rising, "wind_cf"] = (
    (speed.loc[rising] ** 3 - cut_in_ms ** 3)
    / (rated_ms ** 3 - cut_in_ms ** 3)
)

rated = (speed >= rated_ms) & (speed < cut_out_ms)

weather.loc[rated, "wind_cf"] = 1.0
```

`wind_cf` represents estimated output divided by nominal power at
each timestep.

The calculation excludes wakes, air-density effects, electrical losses,
availability, curtailment, and variability within each hour.

For detailed applications, use a specified turbine power curve and
consider [windpowerlib](https://windpowerlib.readthedocs.io/).

## Estimate normalised solar PV generation

We use irradiance on the tilted panel surface rather than assuming
horizontal irradiance equals panel irradiance.

Assume a reference irradiance of 1,000 W/m² and a fixed overall
performance factor of 0.85:

```python
performance_factor = 0.85
reference_irradiance_wm2 = 1000.0

weather["solar_cf"] = (
    weather["poa_wm2"]
    / reference_irradiance_wm2
    * performance_factor
).clip(lower=0, upper=1)
```

The factor represents an assumed reduction from idealised output.
It does not explicitly calculate temperature effects, shading,
module behaviour, or individual losses.

Nominal solar capacity here refers to the module rating in kWp.
Inverter AC capacity is not represented separately, so this indicator
should not be interpreted as an AC-rated capacity factor.

For detailed PV modelling, see
[pvlib](https://pvlib-python.readthedocs.io/).

## Apply a custom function

Some tasks are easier to express through a function.

For example, assign a label to each wind observation:

```python
def classify_wind_operation(speed_ms):
    if speed_ms < cut_in_ms:
        return "Below cut-in"
    elif speed_ms < rated_ms:
        return "Partial output"
    elif speed_ms < cut_out_ms:
        return "Rated output"
    else:
        return "Above cut-out"


weather["wind_operating_region"] = (
    weather["wind_100m_ms"].apply(classify_wind_operation)
)
```

Count the resulting categories:

```python
weather["wind_operating_region"].value_counts()
```

`Series.apply()` calls the function on individual values.
For straightforward arithmetic, prefer vectorised expressions:
they are usually clearer and often faster.

## Calculate generation and capacity factors

Assume a hypothetical 3 MW wind installation and 1 MWp of solar modules:

```python
wind_capacity_mw = 3.0
solar_capacity_mwp = 1.0

weather["wind_power_mw"] = (
    weather["wind_cf"] * wind_capacity_mw
)

weather["solar_power_mw"] = (
    weather["solar_cf"] * solar_capacity_mwp
)

weather["wind_energy_mwh"] = (
    weather["wind_power_mw"] * interval_hours
)

weather["solar_energy_mwh"] = (
    weather["solar_power_mw"] * interval_hours
)
```

### What does capacity factor mean?

A generator does not necessarily operate at its nominal power throughout the year. Wind and solar output varies with weather conditions, and generation may also be reduced by maintenance, outages, or curtailment.

The **capacity factor** describes how much electricity a generator produces over a period compared with what it would produce if it operated at its nominal power continuously throughout that same period.

For a year represented by hourly intervals:

$$
CF = \frac{\sum_{t=1}^{8760} P(t)\,\Delta t} 
{P_{\mathrm{nom}}\sum_{t=1}^{8760}\Delta t}
$$

Here, we assume a year containing **8,760 hours**.

| Symbol | Meaning | Unit |
|---|---|---|
| $t$ | Index identifying each hourly interval, from 1 to 8,760 | — |
| $P(t)$ | Average electrical power generated during hour $t$ | MW |
| $\Delta t$ | Duration of each interval: 1 hour in this example | h |
| $P_{\mathrm{nom}}$ | Nominal or rated power of the installation, assumed constant | MW |
| $\sum_{t=1}^{8760}$ | Add the contribution from every hourly interval in the year | — |

It is dimensionless and is often expressed as a percentage.
It is not a conversion efficiency.

With complete, equally spaced hourly observations and constant nominal
capacity, it equals the mean normalised output:

```python
annual_cf = weather[["wind_cf", "solar_cf"]].mean()

print("Estimated annual capacity factors (%)")
print(annual_cf.mul(100).round(1))
```

Verify the wind result from energy:

```python
total_hours = len(weather) * interval_hours

wind_cf_from_energy = (
    weather["wind_energy_mwh"].sum()
    / (wind_capacity_mw * total_hours)
)

print(wind_cf_from_energy)
```

The results depend on the weather year and technology assumptions.
They are not observed capacity factors for Groningen's existing fleet.

## Resample time series

Resampling groups observations into time periods.

Calculate monthly capacity factors:

```python
monthly_cf = (
    weather[["wind_cf", "solar_cf"]]
    .resample("MS")
    .mean()
)
```

`MS` labels each monthly group at the start of the month.

Calculate monthly energy:

```python
monthly_energy = (
    weather[["wind_energy_mwh", "solar_energy_mwh"]]
    .resample("MS")
    .sum(min_count=1)
)
```

Use means for normalised output and sums for interval energy.

`min_count=1` prevents a completely missing group from being reported
as zero. It does not verify that a partly populated month is complete.

Weekly means can be calculated similarly:

```python
weekly_cf = (
    weather[["wind_cf", "solar_cf"]]
    .resample("W")
    .mean()
)
```

The first and last weekly groups may contain partial weeks.

Calculate annual capacity factors directly from the hourly data.
An unweighted average of monthly capacity factors gives equal weight
to months with different durations.

## Group observations by season and hour

`groupby()` collects observations sharing a label and applies a
calculation to each group.

For local clock-hour patterns, convert the time index:

```python
local_weather = weather.tz_convert("Europe/Amsterdam").copy()
```

This conversion handles daylight-saving changes. Some local clock
hours are skipped or repeated during the year.

Assign a season to each month:

```python
season_for_month = {
    12: "Winter", 1: "Winter", 2: "Winter",
    3: "Spring", 4: "Spring", 5: "Spring",
    6: "Summer", 7: "Summer", 8: "Summer",
    9: "Autumn", 10: "Autumn", 11: "Autumn",
}

local_weather["season"] = (
    local_weather.index.month.map(season_for_month)
)

local_weather["hour"] = local_weather.index.hour
```

Calculate mean solar output by season and local clock hour:

```python
grouped_solar = (
    local_weather
    .groupby(["season", "hour"])["solar_cf"]
    .mean()
)

grouped_solar.head()
```

The result has a **MultiIndex**, with levels for season and hour.

These seasons group observations within the downloaded period.
They do not represent complete meteorological seasons spanning two years.

## Reshape grouped results

Use `unstack()` to move an index level into columns:

```python
seasonal_daily_solar = (
    grouped_solar
    .unstack("season")
    .reindex(columns=["Winter", "Spring", "Summer", "Autumn"])
)

seasonal_daily_solar.head()
```

The resulting table has one row per clock hour and one column per season.
This layout is convenient for comparing seasonal profiles.

## Combine tables

### Combine results by their time index

Calculate monthly irradiation:

```python
monthly_irradiation = (
    weather[["ghi_kwh_m2", "poa_kwh_m2"]]
    .resample("MS")
    .sum(min_count=1)
)
```

Combine the monthly indicators:

```python
monthly_summary = pd.concat(
    [monthly_cf, monthly_energy, monthly_irradiation],
    axis=1,
)

monthly_summary
```

With `axis=1`, `concat()` places columns side by side and aligns their
index labels.

With `axis=0`, it stacks rows. When stacking time series, check for
overlapping timestamps.

### Merge metadata using a shared identifier

Create another table for our hypothetical installations:

```python
site_details = pd.DataFrame(
    {
        "site": ["Library", "Sports centre", "School"],
        "roof_type": ["Flat", "Flat", "Pitched"],
    }
)
```

Merge it with the installation table:

```python
installation_details = (
    installations
    .reset_index()
    .merge(
        site_details,
        on="site",
        how="left",
        validate="one_to_one",
    )
)

installation_details
```

The left merge retains all installations from the left-hand table.

`validate="one_to_one"` checks that each site occurs at most once in
each input, helping prevent unintended row duplication.

## Visualise the results

### Monthly capacity factors

```python
fig, ax = plt.subplots(
    figsize=(8, 4),
    layout="constrained",
)

monthly_cf.rename(
    columns={
        "wind_cf": "Wind",
        "solar_cf": "Solar PV",
    }
).mul(100).plot(
    ax=ax,
    marker="o",
)

ax.set(
    title="Estimated monthly capacity factors — Groningen, 2025",
    xlabel="Month (UTC)",
    ylabel="Capacity factor (%)",
)

ax.set_ylim(0, 100)
ax.grid(alpha=0.3)

plt.show()
```

### Seasonal solar profiles

```python
fig, ax = plt.subplots(
    figsize=(8, 4),
    layout="constrained",
)

seasonal_daily_solar.plot(ax=ax)

ax.set(
    title="Average solar profile by season",
    xlabel="Local clock hour",
    ylabel="Normalised solar output",
)

ax.set_xlim(0, 23)
ax.set_ylim(0, 1)
ax.grid(alpha=0.3)

plt.show()
```

These figures illustrate the modelled profiles. They do not validate
the generation estimates against measured electricity production.

## Save and reload results

Export the hourly analysis:

```python
hourly_file = data_directory / "groningen_2025_analysis.csv"

weather.to_csv(
    hourly_file,
    index_label="timestamp",
)
```

Export the monthly summary:

```python
monthly_summary.to_csv(
    data_directory / "groningen_2025_monthly_summary.csv",
    index_label="month",
)
```

Reload the hourly CSV:

```python
loaded = pd.read_csv(hourly_file)

loaded["timestamp"] = pd.to_datetime(
    loaded["timestamp"],
    utc=True,
)

loaded = loaded.set_index("timestamp")

loaded.info()
```

CSV files do not preserve all pandas metadata and data types.
Check the index, types, and missing values after loading.

## Optional practice exercises

### Inspect and select weather observations

- Report the number of records and the units returned by the API.
- Select the first 48 records using `.iloc`.
- Select July using `.loc`.
- Identify the ten highest wind-speed records.

### Investigate missing values

Make a copy of the wind-speed Series and replace one value with `np.nan`.

- Count the missing values.
- Compare the original and incomplete Series means.
- Try forward filling the missing entry.
- Explain how filling could affect estimated generation.

Keep the original weather table unchanged.

### Compare irradiation indicators

- Calculate monthly horizontal irradiation in kWh/m².
- Identify the month with the largest total.
- Compare it with the month having the largest mean irradiance.
- Explain why totals and means answer different questions.

### Explore turbine assumptions

Repeat the wind calculation using a rated speed of 10 m/s.

- Preserve the original estimate.
- Compare annual and monthly capacity factors.
- Explain why weather alone does not determine capacity factor.

### Explore solar assumptions

Calculate solar profiles using performance factors of 0.80, 0.85, and 0.90.

Compare annual capacity factors while keeping the panel tilt and
orientation unchanged.

### Group and reshape

- Group wind capacity factors by season and local clock hour.
- Reshape the result into one column per season.
- Plot the resulting profiles.
- Explain which observations contribute to each plotted mean.

### Combine installation data

Create a metadata table containing capacities for hypothetical wind
and solar installations.

Combine it with their estimated normalised annual yields to calculate
annual generation. Check that the merge does not duplicate installations.

### Compare weather years

Repeat the download for another complete year using a different cache file.

- Construct the appropriate expected hourly index.
- Apply identical technology assumptions.
- Compare annual capacity factors.
- Explain why a single weather year cannot describe long-term conditions.

### Prepare a short report

Export a monthly results table and two figures. State:

- Weather source, model, location, and year.
- Wind-speed units and height.
- Solar tilt and orientation.
- Generation-model assumptions.
- Treatment of missing data.
- Estimated capacity factors and their limitations.

Restart the kernel and run all cells before sharing your notebook.

## Further learning

### pandas documentation

- [Introductory tutorials](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html)
- [User guide](https://pandas.pydata.org/docs/user_guide/index.html)
- [API reference](https://pandas.pydata.org/docs/reference/index.html)

### Weather data documentation

- [Open-Meteo historical API](https://open-meteo.com/en/docs/historical-weather-api)
- [Open-Meteo terms and attribution](https://open-meteo.com/en/terms)

Acknowledge Open-Meteo and the underlying ERA5 source when sharing
downloaded data or results, following the applicable requirements.

### Detailed generation modelling

- [windpowerlib](https://windpowerlib.readthedocs.io/)
- [pvlib](https://pvlib-python.readthedocs.io/)

These libraries provide more detailed technology representations than
the introductory models used in this lesson.