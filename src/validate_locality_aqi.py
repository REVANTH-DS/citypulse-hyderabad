import csv
from pathlib import Path


project_root = Path(__file__).resolve().parent.parent

input_file = (
    project_root
    / "data"
    / "processed"
    / "locality_aqi.csv"
)


print(
    "CityPulse Hyderabad - "
    "Locality AQI Validation"
)

print("-" * 70)


required_columns = [
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
]


errors = []

records = []


with input_file.open(
    "r",
    encoding="utf-8-sig",
    newline="",
) as file:

    reader = csv.DictReader(file)

    actual_columns = reader.fieldnames or []


    print("Checking CSV schema...")


    for column in required_columns:

        if column not in actual_columns:

            errors.append(
                f"Missing required column: {column}"
            )


    if not errors:

        print("Schema check: PASSED")


    for record in reader:

        records.append(record)


print()

print(
    f"Locality records found: "
    f"{len(records)}"
)


# --------------------------------------------------
# Validate record count
# --------------------------------------------------

if len(records) != 10:

    errors.append(
        "Expected 10 locality AQI records, "
        f"found {len(records)}"
    )

else:

    print(
        "Locality count check: PASSED"
    )


# --------------------------------------------------
# Check duplicate locality IDs
# --------------------------------------------------

locality_ids = [
    record["locality_id"]
    for record in records
]


if len(locality_ids) != len(set(locality_ids)):

    errors.append(
        "Duplicate locality_id values found"
    )

else:

    print(
        "Duplicate locality check: PASSED"
    )


# --------------------------------------------------
# Validate every locality record
# --------------------------------------------------

for record in records:

    locality_name = record[
        "locality_name"
    ]


    # ----------------------------------------------
    # AQI validation
    # ----------------------------------------------

    try:

        estimated_aqi = int(
            record["estimated_aqi"]
        )

        if estimated_aqi < 0:

            errors.append(
                f"{locality_name}: "
                "estimated_aqi is negative"
            )

    except ValueError:

        errors.append(
            f"{locality_name}: "
            "estimated_aqi is not an integer"
        )


    # ----------------------------------------------
    # AQI category validation
    # ----------------------------------------------

    if not record["aqi_category"].strip():

        errors.append(
            f"{locality_name}: "
            "aqi_category is missing"
        )


    # ----------------------------------------------
    # Dominant pollutant validation
    # ----------------------------------------------

    if not record[
        "dominant_pollutant"
    ].strip():

        errors.append(
            f"{locality_name}: "
            "dominant_pollutant is missing"
        )


    # ----------------------------------------------
    # Pollutant count validation
    # ----------------------------------------------

    try:

        pollutants_used = int(
            record["pollutants_used"]
        )

        if pollutants_used <= 0:

            errors.append(
                f"{locality_name}: "
                "no pollutants used"
            )

    except ValueError:

        errors.append(
            f"{locality_name}: "
            "pollutants_used is invalid"
        )


    # ----------------------------------------------
    # Station validation
    # ----------------------------------------------

    if not record[
        "nearest_station"
    ].strip():

        errors.append(
            f"{locality_name}: "
            "nearest_station is missing"
        )


    # ----------------------------------------------
    # Distance validation
    # ----------------------------------------------

    try:

        station_distance = float(
            record["station_distance_km"]
        )

        if station_distance < 0:

            errors.append(
                f"{locality_name}: "
                "station distance is negative"
            )

    except ValueError:

        errors.append(
            f"{locality_name}: "
            "station_distance_km is invalid"
        )


    # ----------------------------------------------
    # Coverage validation
    # ----------------------------------------------

    if not record[
        "coverage_label"
    ].strip():

        errors.append(
            f"{locality_name}: "
            "coverage_label is missing"
        )


    # ----------------------------------------------
    # Last update validation
    # ----------------------------------------------

    if not record[
        "last_update"
    ].strip():

        errors.append(
            f"{locality_name}: "
            "last_update is missing"
        )


# --------------------------------------------------
# Final validation result
# --------------------------------------------------

print()

print("-" * 70)


if errors:

    print("VALIDATION FAILED")

    print()

    print(
        f"Total errors: {len(errors)}"
    )

    print()

    for error in errors:

        print(
            f"- {error}"
        )


else:

    print("VALIDATION PASSED")

    print()

    print(
        "All 10 locality AQI records "
        "are valid."
    )

    print(
        "CityPulse AQI analytical "
        "output is ready."
    )