# Groningen case: preparing the inputs

This case is pending the instructor's Groningen datasets. The Seville notebook is a separate example and must not be interpreted as a Groningen result.

## What we will need

| Input | Required information |
|---|---|
| Demand | Timestamp, demand value, unit (MW or kW), interval duration, time zone, and data source |
| Renewable availability | Timestamp, solar/wind per-unit availability, weather year, and conversion assumptions |
| Technologies | Existing capacity, investment options, costs, lifetimes, efficiencies, and limits |
| Grid | Import/export permissions, rating, price series, and any network constraints |
| Spatial data, if used | Geometry, CRS, identifiers linking locations to network buses, source, and licence |

Demand and renewable series must cover the same intervals without duplicated timestamps or unexplained gaps. A leap year has 8,784 hourly intervals rather than 8,760. Daylight-saving transitions must be handled explicitly, for example by aligning in UTC.

Once the files are supplied, we will validate them, build a documented baseline, and choose controlled scenarios. No Groningen generation capacities or optimisation results are asserted at this stage.
