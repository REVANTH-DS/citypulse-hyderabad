from pathlib import Path
import csv


PROJECT_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "app.py",
    "README.md",
    ".gitignore",
    "data/raw/localities.csv",
    "data/raw/aqi_official_snapshot.csv",
    "data/processed/locality_pollutants.csv",
    "data/processed/locality_aqi.csv",
    "src/aqi_engine.py",
    "src/build_locality_aqi.py",
    "src/build_locality_pollutant_data.py",
    "src/map_localities_to_stations.py",
]


def check_required_files():
    print("\n[1] REQUIRED FILE AUDIT")
    print("-" * 70)

    missing_files = []

    for relative_path in REQUIRED_FILES:
        file_path = PROJECT_ROOT / relative_path

        if file_path.exists():
            print(f"PASS | {relative_path}")
        else:
            print(f"FAIL | {relative_path}")
            missing_files.append(relative_path)

    return missing_files


def inspect_csv(relative_path):
    file_path = PROJECT_ROOT / relative_path

    if not file_path.exists():
        return {
            "file": relative_path,
            "exists": False,
            "rows": 0,
            "columns": [],
        }

    with file_path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        rows = list(reader)
        columns = reader.fieldnames or []

    return {
        "file": relative_path,
        "exists": True,
        "rows": len(rows),
        "columns": columns,
    }


def check_processed_data():
    print("\n[2] PROCESSED DATA AUDIT")
    print("-" * 70)

    csv_files = [
        "data/processed/locality_pollutants.csv",
        "data/processed/locality_aqi.csv",
    ]

    results = []

    for relative_path in csv_files:
        result = inspect_csv(relative_path)
        results.append(result)

        if not result["exists"]:
            print(f"FAIL | {relative_path} | FILE NOT FOUND")
            continue

        print(
            f"PASS | {relative_path} | "
            f"{result['rows']} rows | "
            f"{len(result['columns'])} columns"
        )

        print(
            "       Columns: "
            + ", ".join(result["columns"])
        )

    return results


def check_locality_aqi():
    print("\n[3] LOCALITY AQI QUALITY AUDIT")
    print("-" * 70)

    file_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "locality_aqi.csv"
    )

    if not file_path.exists():
        print("FAIL | locality_aqi.csv not found")
        return ["locality_aqi.csv missing"]

    with file_path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:
        reader = csv.DictReader(csv_file)
        records = list(reader)

    issues = []

    if not records:
        issues.append("No AQI records found")
        print("FAIL | No AQI records found")
        return issues

    locality_names = set()
    categories = set()

    for row_number, record in enumerate(records, start=2):
        locality_name = (
            record.get("locality_name", "")
            .strip()
        )

        category = (
            record.get("aqi_category", "")
            .strip()
        )

        estimated_aqi = (
            record.get("estimated_aqi", "")
            .strip()
        )

        if not locality_name:
            issues.append(
                f"Row {row_number}: missing locality_name"
            )

        if locality_name in locality_names:
            issues.append(
                f"Row {row_number}: duplicate locality "
                f"{locality_name}"
            )

        locality_names.add(locality_name)

        if category:
            categories.add(category)

        try:
            aqi_value = float(estimated_aqi)

            if aqi_value < 0 or aqi_value > 500:
                issues.append(
                    f"Row {row_number}: AQI outside 0-500"
                )

        except ValueError:
            issues.append(
                f"Row {row_number}: invalid estimated_aqi"
            )

    print(f"Localities audited: {len(records)}")
    print(f"Unique localities: {len(locality_names)}")
    print(f"AQI categories found: {len(categories)}")

    if categories:
        for category in sorted(categories):
            print(f"  - {category}")

    if issues:
        print("\nQUALITY ISSUES:")

        for issue in issues:
            print(f"FAIL | {issue}")

    else:
        print(
            "PASS | Locality AQI dataset passed "
            "quality checks"
        )

    return issues


def print_final_result(missing_files, data_results, quality_issues):
    print("\n[4] FINAL PROJECT AUDIT RESULT")
    print("=" * 70)

    missing_processed_data = any(
        not result["exists"] or result["rows"] == 0
        for result in data_results
    )

    if (
        not missing_files
        and not missing_processed_data
        and not quality_issues
    ):
        print("CITYPULSE PROJECT AUDIT PASSED")
        print(
            "Core files, processed datasets and "
            "locality AQI quality checks are valid."
        )

    else:
        print("CITYPULSE PROJECT AUDIT FAILED")

        print(
            f"Missing files: {len(missing_files)}"
        )

        print(
            f"AQI quality issues: "
            f"{len(quality_issues)}"
        )


if __name__ == "__main__":
    print("=" * 70)
    print("CityPulse Hyderabad - Final Project Audit")
    print("=" * 70)

    missing_files = check_required_files()

    data_results = check_processed_data()

    quality_issues = check_locality_aqi()

    print_final_result(
        missing_files,
        data_results,
        quality_issues,
    )