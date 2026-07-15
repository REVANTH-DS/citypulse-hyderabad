# CityPulse Hyderabad - Data Sources

## Environmental Data

### Source

Government of India Open Government Data Platform

### Data Provider

Central Pollution Control Board (CPCB)

### Dataset

Real-Time Air Quality Index from Various Locations

### Planned Use

CityPulse V1 will use available air-quality monitoring observations to derive a locality-level environmental indicator.

### Important Limitation

Air-quality observations are collected at monitoring-station locations.

A selected CityPulse locality may not contain an air-quality monitoring station.

CityPulse must therefore evaluate monitoring-station coverage before assigning an environmental indicator to a locality.

The V1 methodology may use the nearest available monitoring station, subject to a documented distance and data-availability rule.

CityPulse will not claim that a station observation perfectly represents air quality across an entire locality.

### Validation Questions

Before integrating environmental data, the project will evaluate:

1. Which monitoring stations are available for Hyderabad?
2. Which pollutants are reported?
3. What location fields are available?
4. What observation timestamps are available?
5. Are values missing?
6. Are duplicate observations present?
7. How close is the nearest available station to each selected locality?
8. What distance threshold should be used for acceptable environmental coverage?

## Urban Services Data

### Planned Source

OpenStreetMap-derived geospatial data

### Planned Use

CityPulse V1 plans to analyse selected:

- Healthcare services
- Educational services
- Metro or rapid-transit access
- Essential urban services

Detailed extraction and scoring methodology will be documented after the environmental data pipeline is established.ss