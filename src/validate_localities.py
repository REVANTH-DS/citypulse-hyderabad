import csv
from pathlib import Path


project_root = Path(__file__).resolve().parent.parent
localities_file = project_root / "data" / "raw" / "localities.csv"


required_columns = {
    "locality_id",
    "locality_name",
    "latitude",
    "longitude",
    "area_group",
}


with localities_file.open(mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    columns = set(reader.fieldnames or [])
    localities = list(reader)


errors = []


# Check 1: Required columns
missing_columns = required_columns - columns

if missing_columns:
    errors.append(
        f"Missing required columns: {sorted(missing_columns)}"
    )


# Check 2: Expected number of locality records
if len(localities) != 10:
    errors.append(
        f"Expected 10 localities, found {len(localities)}"
    )


# Check 3: Missing required values
for row_number, locality in enumerate(localities, start=2):
    for column in required_columns:
        value = locality.get(column)

        if value is None or value.strip() == "":
            errors.append(
                f"Row {row_number}: missing value in '{column}'"
            )


# Check 4: Duplicate locality IDs
locality_ids = [
    locality["locality_id"]
    for locality in localities
    if locality.get("locality_id")
]

if len(locality_ids) != len(set(locality_ids)):
    errors.append("Duplicate locality_id values found")


# Check 5: Duplicate locality names
locality_names = [
    locality["locality_name"].strip().lower()
    for locality in localities
    if locality.get("locality_name")
]

if len(locality_names) != len(set(locality_names)):
    errors.append("Duplicate locality names found")


# Check 6: Coordinate values
for row_number, locality in enumerate(localities, start=2):
    try:
        latitude = float(locality["latitude"])
        longitude = float(locality["longitude"])

        if not 17.0 <= latitude <= 18.0:
            errors.append(
                f"Row {row_number}: latitude outside expected range"
            )

        if not 78.0 <= longitude <= 79.0:
            errors.append(
                f"Row {row_number}: longitude outside expected range"
            )

    except (ValueError, TypeError):
        errors.append(
            f"Row {row_number}: invalid latitude or longitude"
        )


print("CityPulse Hyderabad - Locality Data Validation")
print("-" * 50)

if errors:
    print("VALIDATION FAILED")

    for error in errors:
        print(f"- {error}")

else:
    print("VALIDATION PASSED")
    print(f"Validated {len(localities)} locality records")