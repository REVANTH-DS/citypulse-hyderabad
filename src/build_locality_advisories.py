import csv
from pathlib import Path

from advisory_engine import get_advisory


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "locality_aqi.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "locality_advisories.csv"
)


if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Input file not found: {INPUT_FILE}"
    )


with INPUT_FILE.open(
    "r",
    encoding="utf-8-sig",
    newline="",
) as file:

    reader = csv.DictReader(file)

    locality_records = list(reader)


print(
    "CityPulse Hyderabad - "
    "Building Locality Advisories"
)

print("-" * 70)

print(
    f"Locality AQI records loaded: "
    f"{len(locality_records)}"
)


output_records = []


for record in locality_records:

    aqi_category = record[
        "aqi_category"
    ]

    dominant_pollutant = record[
        "dominant_pollutant"
    ]


    advisory = get_advisory(
        aqi_category,
        dominant_pollutant,
    )


    output_record = {
        **record,

        "health_message": advisory[
            "health_message"
        ],

        "outdoor_guidance": advisory[
            "outdoor_guidance"
        ],

        "sensitive_group_guidance": advisory[
            "sensitive_group_guidance"
        ],

        "pollutant_insight": advisory[
            "pollutant_insight"
        ],
    }


    output_records.append(
        output_record
    )


if not output_records:
    raise RuntimeError(
        "No locality advisory records created"
    )


OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)


fieldnames = list(
    output_records[0].keys()
)


with OUTPUT_FILE.open(
    "w",
    encoding="utf-8",
    newline="",
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames,
    )

    writer.writeheader()

    writer.writerows(
        output_records
    )


print()

print(
    f"Advisory records created: "
    f"{len(output_records)}"
)

print()


for record in output_records:

    print(
        f"Locality: "
        f"{record['locality_name']}"
    )

    print(
        f"Estimated AQI: "
        f"{record['estimated_aqi']}"
    )

    print(
        f"AQI Category: "
        f"{record['aqi_category']}"
    )

    print(
        f"Dominant Pollutant: "
        f"{record['dominant_pollutant']}"
    )

    print(
        f"Health Message: "
        f"{record['health_message']}"
    )

    print(
        f"Outdoor Guidance: "
        f"{record['outdoor_guidance']}"
    )

    print(
        "Sensitive Group Guidance: "
        f"{record['sensitive_group_guidance']}"
    )

    print(
        f"Pollutant Insight: "
        f"{record['pollutant_insight']}"
    )

    print("-" * 70)


print()

print(
    "Locality advisory dataset created "
    "successfully"
)

print(
    f"Output: {OUTPUT_FILE}"
)