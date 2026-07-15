# CityPulse Hyderabad V1 - Project Charter

## Project Name

CityPulse Hyderabad

## Project Type

End-to-End Urban Data Analytics and Decision-Support Platform

## Problem Statement

Urban information related to environmental conditions and access to essential services is often distributed across multiple data sources.

Users who want to compare localities may need to separately examine air-quality information, healthcare facilities, educational services, transport accessibility, and essential urban services.

CityPulse Hyderabad aims to integrate selected urban datasets, transform them into comparable locality-level indicators, and provide a transparent decision-support platform for comparing selected Hyderabad localities.

## Target Users

CityPulse V1 is designed for:

- Students comparing localities
- Working professionals exploring areas
- Families evaluating urban-service accessibility
- Researchers and data enthusiasts exploring locality-level indicators

## V1 Core Features

1. Select a Hyderabad locality
2. Compare two localities
3. Analyse an environmental indicator
4. Analyse urban-service accessibility
5. Adjust indicator weights
6. Calculate a weighted CityPulse Score
7. Explore locality metrics using an interactive application
8. Analyse aggregated urban indicators using a Power BI dashboard

## V1 Indicators

CityPulse V1 will initially analyse:

- Air quality
- Healthcare accessibility
- Education accessibility
- Metro accessibility
- Essential-services accessibility

## V1 Geographic Scope

The first version will focus on a selected set of Hyderabad localities.

The initial target is 10 localities representing different parts of the Hyderabad urban area.

## V1 Data Sources

Planned data sources include:

- Government open data for environmental observations
- OpenStreetMap-derived geospatial data for selected urban services and transport features

All data sources will be documented with their limitations and refresh characteristics.

## V1 Technology Stack

- Python
- Pandas
- NumPy
- PostgreSQL
- SQL
- Power BI
- Streamlit
- Git
- GitHub

Additional geospatial Python libraries may be introduced when required.

## Success Criteria

CityPulse V1 will be considered complete when:

- Data for the selected localities can be collected and processed
- Locality-level indicators can be calculated
- The scoring methodology is documented
- Two localities can be compared
- Users can adjust indicator weights
- CityPulse Scores can be calculated transparently
- A Power BI analytics dashboard is completed
- A Streamlit application is deployed
- The GitHub repository contains clear documentation
- The project can be explained and defended in a technical interview

## Out of Scope for V1

The following features are not part of Version 1:

- User accounts
- Payments
- Mobile application
- Chatbot
- Large language model integration
- Deep learning
- Real-estate listing recommendations
- Crime prediction
- Automatic claims about the best place to live
- Full coverage of every Hyderabad locality

These features may be evaluated in future versions based on data availability and project requirements.

## Project Status

V1 - In Development