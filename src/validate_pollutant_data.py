import csv
from collections import Counter
from pathlib import Path


project_root = Path(__file__).resolve().parent.parent

input_file = (
    project_root
    / "data"
    / "processed"
    / "locality_pollutant_data.csv"
)


expected_columns = {
    "locality_id",
    "locality_name",
    "area_group",
    "pollutant_id",
    "pollutant_avg",
    "pollutant_min",
    "pollutant_max",
    "source_station",
    "station_distance_km",
    "coverage_label",
    "last_update",
}


expected_pollutants = {
    "CO",
    "NH3",
    "NO2",
    "OZONE",
    "PM10",
    "PM2.5",
    "SO2",
}


allowed_coverage_labels = {
    "nearby",
    "extended",
    "limited",
}


errors = []


print(
    "CityPulse Hyderabad - "
    "Processed Data Validation"
)

print("-" * 60)


if not input_file.exists():
    raise FileNotFoundError(
        f"Processed dataset not found: {input_file}"
    )


with input_file.open(
    mode="r",
    encoding="utf-8",
    newline="",
) as file:
    reader = csv.DictReader(file)

    actual_columns = set(
        reader.fieldnames or []
    )

    records = list(reader)


print(f"Records loaded: {len(records)}")


missing_columns = (
    expected_columns - actual_columns
)


if missing_columns:
    errors.append(
        "Missing columns: "
        + ", ".join(
            sorted(missing_columns)
        )
    )

else:
    print(
        "PASS: Required columns are present"
    )


if len(records) == 70:
    print(
        "PASS: Expected 70 records found"
    )

else:
    errors.append(
        "Expected 70 records, "
        f"found {len(records)}"
    )


locality_pollutant_pairs = [
    (
        record["locality_id"],
        record["pollutant_id"],
    )
    for record in records
]


pair_counts = Counter(
    locality_pollutant_pairs
)


duplicate_pairs = [
    pair
    for pair, count in pair_counts.items()
    if count > 1
]


if duplicate_pairs:
    errors.append(
        "Duplicate locality-pollutant "
        f"pairs found: {duplicate_pairs}"
    )

else:
    print(
        "PASS: No duplicate "
        "locality-pollutant pairs"
    )


invalid_average_records = []


for record in records:
    try:
        float(record["pollutant_avg"])

    except (
        TypeError,
        ValueError,
    ):
        invalid_average_records.append(
            (
                record["locality_name"],
                record["pollutant_id"],
                record["pollutant_avg"],
            )
        )


if invalid_average_records:
    errors.append(
        "Invalid pollutant_avg values found: "
        f"{invalid_average_records}"
    )

else:
    print(
        "PASS: All pollutant averages "
        "are numeric"
    )


invalid_distance_records = []


for record in records:
    try:
        distance = float(
            record["station_distance_km"]
        )

        if distance < 0:
            raise ValueError

    except (
        TypeError,
        ValueError,
    ):
        invalid_distance_records.append(
            (
                record["locality_name"],
                record["station_distance_km"],
            )
        )


if invalid_distance_records:
    errors.append(
        "Invalid station distances found: "
        f"{invalid_distance_records}"
    )

else:
    print(
        "PASS: All station distances "
        "are valid"
    )


invalid_coverage_records = [
    (
        record["locality_name"],
        record["coverage_label"],
    )
    for record in records
    if record["coverage_label"]
    not in allowed_coverage_labels
]


if invalid_coverage_records:
    errors.append(
        "Invalid coverage labels found: "
        f"{invalid_coverage_records}"
    )

else:
    print(
        "PASS: All coverage labels are valid"
    )


locality_pollutants = {}


for record in records:
    locality_id = record["locality_id"]

    locality_pollutants.setdefault(
        locality_id,
        set(),
    )

    locality_pollutants[
        locality_id
    ].add(
        record["pollutant_id"]
    )


incomplete_localities = []


for locality_id, pollutants in (
    locality_pollutants.items()
):
    if pollutants != expected_pollutants:
        missing_pollutants = (
            expected_pollutants - pollutants
        )

        extra_pollutants = (
            pollutants - expected_pollutants
        )

        incomplete_localities.append(
            {
                "locality_id": locality_id,
                "missing": sorted(
                    missing_pollutants
                ),
                "extra": sorted(
                    extra_pollutants
                ),
            }
        )


if incomplete_localities:
    errors.append(
        "Incomplete pollutant coverage: "
        f"{incomplete_localities}"
    )

else:
    print(
        "PASS: Every locality has "
        "all 7 expected pollutants"
    )


empty_source_stations = [
    (
        record["locality_name"],
        record["pollutant_id"],
    )
    for record in records
    if not record["source_station"].strip()
]


if empty_source_stations:
    errors.append(
        "Empty source stations found: "
        f"{empty_source_stations}"
    )

else:
    print(
        "PASS: Every record has "
        "a source station"
    )


print("-" * 60)


if errors:
    print("VALIDATION FAILED")

    print(
        f"Total validation errors: "
        f"{len(errors)}"
    )

    for error_number, error in enumerate(
        errors,
        start=1,
    ):
        print(
            f"\n{error_number}. {error}"
        )

    raise SystemExit(1)


print("VALIDATION PASSED")

print(
    "CityPulse processed pollutant "
    "dataset passed all quality checks."
)

print(
    f"Validated {len(records)} records."
)