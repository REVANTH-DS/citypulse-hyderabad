from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "locality_advisories.csv"
)


# ============================================================
# EXPECTED PRODUCT SCHEMA
# ============================================================

REQUIRED_COLUMNS = [
    "locality_id",
    "locality_name",
    "area_group",
    "estimated_aqi",
    "aqi_category",
    "dominant_pollutant",
    "pollutants_used",
    "nearest_station",
    "station_distance_km",
    "coverage_label",
    "last_update",
    "pollutant_insight",
    "health_message",
    "outdoor_guidance",
    "sensitive_group_guidance",
]


VALID_AQI_CATEGORIES = {
    "Good",
    "Satisfactory",
    "Moderately Polluted",
    "Poor",
    "Very Poor",
    "Severe",
}


VALID_COVERAGE_LABELS = {
    "direct",
    "nearby",
    "extended",
}


# ============================================================
# START VALIDATION
# ============================================================

print(
    "CityPulse Hyderabad - "
    "Final Product Validation"
)

print("=" * 70)


# ============================================================
# FILE VALIDATION
# ============================================================

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Product dataset not found: {DATA_FILE}"
    )


print(
    f"Product dataset found: {DATA_FILE.name}"
)


# ============================================================
# LOAD DATA
# ============================================================

data = pd.read_csv(DATA_FILE)


print(
    f"Records loaded: {len(data)}"
)


if data.empty:
    raise ValueError(
        "Product dataset is empty"
    )


# ============================================================
# RECORD COUNT
# ============================================================

EXPECTED_LOCALITIES = 10


if len(data) != EXPECTED_LOCALITIES:
    raise ValueError(
        "Expected "
        f"{EXPECTED_LOCALITIES} localities, "
        f"found {len(data)}"
    )


print(
    f"Locality count valid: {len(data)}"
)


# ============================================================
# COLUMN VALIDATION
# ============================================================

missing_columns = [
    column
    for column in REQUIRED_COLUMNS
    if column not in data.columns
]


if missing_columns:
    raise ValueError(
        "Missing required columns: "
        f"{missing_columns}"
    )


print(
    "Required columns validated"
)


# ============================================================
# LOCALITY VALIDATION
# ============================================================

if data["locality_id"].isna().any():
    raise ValueError(
        "Missing locality IDs detected"
    )


if data["locality_name"].isna().any():
    raise ValueError(
        "Missing locality names detected"
    )


if data["locality_id"].duplicated().any():
    duplicates = data.loc[
        data["locality_id"].duplicated(),
        "locality_id",
    ].tolist()

    raise ValueError(
        "Duplicate locality IDs detected: "
        f"{duplicates}"
    )


if data["locality_name"].duplicated().any():
    duplicates = data.loc[
        data["locality_name"].duplicated(),
        "locality_name",
    ].tolist()

    raise ValueError(
        "Duplicate locality names detected: "
        f"{duplicates}"
    )


print(
    "Locality identity validated"
)


# ============================================================
# AQI VALIDATION
# ============================================================

aqi_values = pd.to_numeric(
    data["estimated_aqi"],
    errors="coerce",
)


if aqi_values.isna().any():
    raise ValueError(
        "Invalid estimated AQI values detected"
    )


if (
    (aqi_values < 0)
    | (aqi_values > 500)
).any():
    invalid_rows = data.loc[
        (aqi_values < 0)
        | (aqi_values > 500),
        [
            "locality_name",
            "estimated_aqi",
        ],
    ]

    raise ValueError(
        "AQI outside valid range:\n"
        f"{invalid_rows}"
    )


print(
    "AQI values validated"
)


# ============================================================
# AQI CATEGORY VALIDATION
# ============================================================

invalid_categories = set(
    data["aqi_category"].dropna()
) - VALID_AQI_CATEGORIES


if invalid_categories:
    raise ValueError(
        "Invalid AQI categories detected: "
        f"{invalid_categories}"
    )


if data["aqi_category"].isna().any():
    raise ValueError(
        "Missing AQI categories detected"
    )


print(
    "AQI categories validated"
)


# ============================================================
# DOMINANT POLLUTANT VALIDATION
# ============================================================

if (
    data["dominant_pollutant"]
    .isna()
    .any()
):
    raise ValueError(
        "Missing dominant pollutants detected"
    )


if (
    data["dominant_pollutant"]
    .astype(str)
    .str.strip()
    .eq("")
    .any()
):
    raise ValueError(
        "Empty dominant pollutants detected"
    )


print(
    "Dominant pollutants validated"
)


# ============================================================
# POLLUTANTS USED VALIDATION
# ============================================================

pollutants_used = pd.to_numeric(
    data["pollutants_used"],
    errors="coerce",
)


if pollutants_used.isna().any():
    raise ValueError(
        "Invalid pollutants_used values detected"
    )


if (pollutants_used <= 0).any():
    raise ValueError(
        "Every locality must use "
        "at least one pollutant"
    )


print(
    "Pollutant coverage validated"
)


# ============================================================
# STATION VALIDATION
# ============================================================

if data["nearest_station"].isna().any():
    raise ValueError(
        "Missing monitoring stations detected"
    )


if (
    data["nearest_station"]
    .astype(str)
    .str.strip()
    .eq("")
    .any()
):
    raise ValueError(
        "Empty monitoring station names detected"
    )


print(
    "Monitoring stations validated"
)


# ============================================================
# DISTANCE VALIDATION
# ============================================================

station_distance = pd.to_numeric(
    data["station_distance_km"],
    errors="coerce",
)


if station_distance.isna().any():
    raise ValueError(
        "Invalid station distances detected"
    )


if (station_distance < 0).any():
    raise ValueError(
        "Negative station distance detected"
    )


print(
    "Station distances validated"
)


# ============================================================
# COVERAGE VALIDATION
# ============================================================

coverage_values = (
    data["coverage_label"]
    .astype(str)
    .str.strip()
    .str.lower()
)


invalid_coverage = set(
    coverage_values
) - VALID_COVERAGE_LABELS


if invalid_coverage:
    raise ValueError(
        "Invalid coverage labels detected: "
        f"{invalid_coverage}"
    )


print(
    "Coverage labels validated"
)


# ============================================================
# TIMESTAMP VALIDATION
# ============================================================

timestamps = pd.to_datetime(
    data["last_update"],
    errors="coerce",
    dayfirst=True,
)


if timestamps.isna().any():
    invalid_rows = data.loc[
        timestamps.isna(),
        [
            "locality_name",
            "last_update",
        ],
    ]

    raise ValueError(
        "Invalid observation timestamps:\n"
        f"{invalid_rows}"
    )


print(
    "Observation timestamps validated"
)


# ============================================================
# ADVISORY CONTENT VALIDATION
# ============================================================

ADVISORY_COLUMNS = [
    "pollutant_insight",
    "health_message",
    "outdoor_guidance",
    "sensitive_group_guidance",
]


for column in ADVISORY_COLUMNS:

    if data[column].isna().any():
        raise ValueError(
            f"Missing advisory content in {column}"
        )

    short_content = (
        data[column]
        .astype(str)
        .str.strip()
        .str.len()
        < 10
    )

    if short_content.any():
        invalid_localities = data.loc[
            short_content,
            "locality_name",
        ].tolist()

        raise ValueError(
            f"Advisory content too short "
            f"in {column}: "
            f"{invalid_localities}"
        )


print(
    "Advisory content validated"
)


# ============================================================
# FINAL PRODUCT SUMMARY
# ============================================================

print()
print(
    "CityPulse Product Summary"
)

print("-" * 70)


print(
    f"Localities: {len(data)}"
)

print(
    "AQI range: "
    f"{int(aqi_values.min())} - "
    f"{int(aqi_values.max())}"
)

print(
    "AQI categories: "
    f"{data['aqi_category'].nunique()}"
)

print(
    "Monitoring stations used: "
    f"{data['nearest_station'].nunique()}"
)

print(
    "Dominant pollutants: "
    f"{data['dominant_pollutant'].nunique()}"
)


print()
print("=" * 70)

print(
    "FINAL VALIDATION PASSED"
)

print(
    "CityPulse Hyderabad product data "
    "is ready for deployment."
)

print("=" * 70)