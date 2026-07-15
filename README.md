## LIVE DEMO 
EXPLORE CITY PULSE HYDERABAD :
** LIVE APPLICATION :* 
https://citypulse-hyderabad.streamlit.app/
Select a Hyderabad locality to explore estimated AQI dominant pollutant , locality-level air quality insights and contextual guidance ...


# 🌆 CityPulse Hyderabad

### Locality-Level Air Quality Intelligence for Hyderabad

CityPulse Hyderabad is a data-driven air quality intelligence project that transforms available monitoring-station observations into understandable locality-level AQI estimates for Hyderabad.

Instead of presenting only station-level pollution records, CityPulse maps selected Hyderabad localities to nearby monitoring stations, processes pollutant observations, calculates pollutant sub-indices using AQI breakpoint interpolation, and presents the resulting locality-level estimates through an interactive Streamlit dashboard.

> **Our Hyderabad. Our Air Quality.**

---

## 🚀 Project Overview

Official air-quality datasets commonly provide observations from monitoring stations.

For a normal user, however, a more natural question is:

> "What does the available air-quality data indicate for my locality?"

CityPulse Hyderabad explores this problem through a transparent estimation pipeline.

The project:

- loads Hyderabad locality information
- processes an official AQI data snapshot
- identifies Hyderabad monitoring stations
- maps localities to nearby stations using geographic distance
- prepares locality-level pollutant observations
- calculates pollutant AQI sub-indices
- estimates locality-level AQI
- identifies the dominant pollutant
- validates processed outputs
- presents the results in an interactive dashboard

---

## ✨ Key Features

### 📍 Locality-Based Air Quality Exploration

Users can select a supported Hyderabad locality and explore its estimated air-quality conditions.

### 🛰️ Nearest Monitoring Station Mapping

CityPulse uses locality and station coordinates to identify nearby monitoring-station observations.

### 🧪 Pollutant-Level Processing

The pipeline processes available pollutant observations such as:

- PM2.5
- PM10
- NO2
- SO2
- CO
- OZONE
- NH3

### 🧮 AQI Sub-Index Calculation

Pollutant concentrations are converted into AQI sub-indices using breakpoint-based linear interpolation.

### 🏭 Dominant Pollutant Identification

The pollutant producing the highest calculated sub-index is identified as the dominant pollutant for the locality estimate.

### 📊 Interactive Streamlit Dashboard

The dashboard provides:

- locality selection
- estimated AQI
- AQI category
- dominant pollutant information
- pollutant analysis
- monitoring-station context
- estimation methodology
- limitations and interpretation guidance

### ✅ Data Validation and Project Audit

Validation scripts inspect processed datasets and verify important project outputs before release.

---

## 🧠 How CityPulse Works

The CityPulse data pipeline follows this architecture:

```text
Official AQI Snapshot
        |
        v
Hyderabad Monitoring Station Filtering
        |
        v
Locality Coordinate Dataset
        |
        v
Locality-to-Station Distance Calculation
        |
        v
Nearest Monitoring Station Mapping
        |
        v
Locality Pollutant Dataset
        |
        v
Pollutant AQI Sub-Index Calculation
        |
        v
Locality AQI Estimation
        |
        v
Validation and Project Audit
        |
        v
Streamlit CityPulse Dashboard


For official air-quality reporting and public-health guidance, users should refer to the relevant government and environmental authorities.
