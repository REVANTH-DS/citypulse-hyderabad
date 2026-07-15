import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "locality_advisories.csv"
)


EXPECTED_COLUMNS = {
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
    "health_message",
    "outdoor_guidance",
    "sensitive_group_guidance",
    "pollutant_insight",
}


EXPECTED_CATEGORIES = {
    "Good",
    "Satisfactory",
    "Moderately Polluted",
    "Poor",
    "Very Poor",
    "Severe",
}


EXPECTED_POLLUTANTS = {
    "CO",
    "NH3",
    "NO2",
    "OZONE",
    "PM10",
    "PM2.5",
    "SO2",
}


EXPECTED_COVERAGE_LABELS = {
    "nearby",
    "extended",
    "limited",
}


print(
    "CityPulse Hyderabad - "
    "Final Product Data Validation"
)

print("-" * 70)


if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Product dataset not found: {INPUT_FILE}"
    )


with INPUT_FILE.open(
    "r",
    encoding="utf-8-sig",
    newline="",
) as file:

    reader = csv.DictReader(file)

    actual_columns = set(
        reader.fieldnames or []
    )

    records = list(reader)


errors = []


print(
    f"Product records loaded: "
    f"{len(records)}"
)


# --------------------------------------------------
# Schema validation
# --------------------------------------------------

missing_columns = (
    EXPECTED_COLUMNS - actual_columns
)


if missing_columns:

    errors.append(
        "Missing product columns: "
        + ", ".join(
            sorted(missing_columns)
        )
    )

else:

    print(
        "PASS: Product schema is complete"
    )


# --------------------------------------------------
# Record count validation
# --------------------------------------------------

if len(records) == 10:

    print(
        "PASS: Expected 10 locality records found"
    )

else:

    errors.append(
        "Expected 10 locality records, "
        f"found {len(records)}"
    )


# --------------------------------------------------
# Duplicate locality validation
# --------------------------------------------------

locality_ids = [
    record["locality_id"]
    for record in records
]


if len(locality_ids) == len(set(locality_ids)):

    print(
        "PASS: Locality IDs are unique"
    )

else:

    errors.append(
        "Duplicate locality IDs found"
    )


# --------------------------------------------------
# Validate individual product records
# --------------------------------------------------

for record in records:

    locality_name = record[
        "locality_name"
    ]


    # AQI value
    try:

        estimated_aqi = int(
            record["estimated_aqi"]
        )

        if not 0 <= estimated_aqi <= 500:

            errors.append(
                f"{locality_name}: "
                "estimated_aqi outside 0-500"
            )

    except (
        TypeError,
        ValueError,
    ):

        errors.append(
            f"{locality_name}: "
            "estimated_aqi is invalid"
        )


    # AQI category
    if record["aqi_category"] not in (
        EXPECTED_CATEGORIES
    ):

        errors.append(
            f"{locality_name}: "
            "invalid AQI category "
            f"{record['aqi_category']}"
        )


    # Dominant pollutant
    if record[
        "dominant_pollutant"
    ] not in EXPECTED_POLLUTANTS:

        errors.append(
            f"{locality_name}: "
            "invalid dominant pollutant "
            f"{record['dominant_pollutant']}"
        )


    # Pollutants used
    try:

        pollutants_used = int(
            record["pollutants_used"]
        )

        if pollutants_used < 3:

            errors.append(
                f"{locality_name}: "
                "fewer than 3 pollutants used"
            )

    except (
        TypeError,
        ValueError,
    ):

        errors.append(
            f"{locality_name}: "
            "pollutants_used is invalid"
        )


    # Nearest station
    if not record[
        "nearest_station"
    ].strip():

        errors.append(
            f"{locality_name}: "
            "nearest station is missing"
        )


    # Station distance
    try:

        station_distance = float(
            record["station_distance_km"]
        )

        if station_distance < 0:

            errors.append(
                f"{locality_name}: "
                "negative station distance"
            )

    except (
        TypeError,
        ValueError,
    ):

        errors.append(
            f"{locality_name}: "
            "station distance is invalid"
        )


    # Coverage label
    if record[
        "coverage_label"
    ] not in EXPECTED_COVERAGE_LABELS:

        errors.append(
            f"{locality_name}: "
            "invalid coverage label "
            f"{record['coverage_label']}"
        )


    # Last update
    if not record[
        "last_update"
    ].strip():

        errors.append(
            f"{locality_name}: "
            "last update is missing"
        )


    # Health message
    if not record[
        "health_message"
    ].strip():

        errors.append(
            f"{locality_name}: "
            "health message is missing"
        )


    # Outdoor guidance
    if not record[
        "outdoor_guidance"
    ].strip():

        errors.append(
            f"{locality_name}: "
            "outdoor guidance is missing"
        )


    # Sensitive group guidance
    if not record[
        "sensitive_group_guidance"
    ].strip():

        errors.append(
            f"{locality_name}: "
            "sensitive group guidance is missing"
        )


    # Pollutant insight
    if not record[
        "pollutant_insight"
    ].strip():

        errors.append(
            f"{locality_name}: "
            "pollutant insight is missing"
        )


print("-" * 70)


# --------------------------------------------------
# Final result
# --------------------------------------------------

if errors:

    print("VALIDATION FAILED")

    print(
        f"Total product data errors: "
        f"{len(errors)}"
    )


    for error_number, error in enumerate(
        errors,
        start=1,
    ):

        print()

        print(
            f"{error_number}. {error}"
        )


    raise SystemExit(1)


print("VALIDATION PASSED")

print()

print(
    "CityPulse final product dataset "
    "passed all quality checks."
)

print(
    f"Validated {len(records)} "
    "product-ready locality records."
)