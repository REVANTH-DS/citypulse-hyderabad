import csv
from pathlib import Path
from collections import defaultdict

from aqi_engine import (
    calculate_sub_index,
    get_aqi_category,
)


# --------------------------------------------------
# Project paths
# --------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

input_file = (
    project_root
    / "data"
    / "processed"
    / "locality_pollutants.csv"
)

output_file = (
    project_root
    / "data"
    / "processed"
    / "locality_aqi.csv"
)


# --------------------------------------------------
# Load locality pollutant records
# --------------------------------------------------

locality_records = defaultdict(list)


with input_file.open(
    "r",
    encoding="utf-8-sig",
    newline="",
) as file:

    reader = csv.DictReader(file)

    for record in reader:

        locality_name = record["locality_name"]

        locality_records[locality_name].append(
            record
        )


# --------------------------------------------------
# Start AQI processing
# --------------------------------------------------

print(
    "CityPulse Hyderabad - "
    "Building Locality AQI Estimates"
)

print("-" * 70)

print(
    f"Localities loaded: "
    f"{len(locality_records)}"
)


aqi_summaries = []


# --------------------------------------------------
# Calculate AQI for every locality
# --------------------------------------------------

for (
    locality_name,
    records,
) in locality_records.items():

    pollutant_sub_indices = []


    # ----------------------------------------------
    # Calculate pollutant sub-indices
    # ----------------------------------------------

    for record in records:

        pollutant_id = record[
            "pollutant_id"
        ]

        concentration = record[
            "pollutant_avg"
        ]


        sub_index = calculate_sub_index(
            pollutant_id,
            concentration,
        )


        if sub_index is not None:

            pollutant_sub_indices.append(
                {
                    "pollutant_id": pollutant_id,
                    "sub_index": sub_index,
                }
            )


    # ----------------------------------------------
    # Skip locality if no valid pollutant data
    # ----------------------------------------------

    if not pollutant_sub_indices:

        print(
            f"Skipping {locality_name}: "
            "no valid pollutant sub-indices"
        )

        continue


    # ----------------------------------------------
    # Find dominant pollutant
    # ----------------------------------------------

    dominant_record = max(
        pollutant_sub_indices,
        key=lambda item: item["sub_index"],
    )


    estimated_aqi = dominant_record[
        "sub_index"
    ]

    dominant_pollutant = dominant_record[
        "pollutant_id"
    ]


    # ----------------------------------------------
    # Get AQI category
    # ----------------------------------------------

    category = get_aqi_category(
        estimated_aqi
    )


    # ----------------------------------------------
    # Get locality metadata
    # ----------------------------------------------

    first_record = records[0]


    # ----------------------------------------------
    # Build locality AQI summary
    # ----------------------------------------------

    summary = {

        "locality_id": first_record[
            "locality_id"
        ],

        "locality_name": locality_name,

        "area_group": first_record[
            "area_group"
        ],

        "estimated_aqi": estimated_aqi,

        "aqi_category": category,

        "dominant_pollutant": (
            dominant_pollutant
        ),

        "pollutants_used": len(
            pollutant_sub_indices
        ),

        "nearest_station": first_record[
            "source_station"
        ],

        "station_distance_km": first_record[
            "station_distance_km"
        ],

        "coverage_label": first_record[
            "coverage_label"
        ],

        "last_update": first_record[
            "last_update"
        ],
    }


    aqi_summaries.append(
        summary
    )


    # ----------------------------------------------
    # Print locality result
    # ----------------------------------------------

    print()

    print(
        f"Locality: {locality_name}"
    )

    print(
        f"Estimated AQI: {estimated_aqi}"
    )

    print(
        f"Category: {category}"
    )

    print(
        "Dominant pollutant: "
        f"{dominant_pollutant}"
    )

    print(
        "Pollutants used: "
        f"{len(pollutant_sub_indices)}"
    )

    print(
        "Nearest station: "
        f"{first_record['source_station']}"
    )

    print(
        "Station distance: "
        f"{first_record['station_distance_km']} km"
    )

    print(
        "Coverage: "
        f"{first_record['coverage_label']}"
    )


# --------------------------------------------------
# Output CSV columns
# --------------------------------------------------

fieldnames = [

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


# --------------------------------------------------
# Write locality AQI CSV
# --------------------------------------------------

with output_file.open(
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
        aqi_summaries
    )


# --------------------------------------------------
# Final summary
# --------------------------------------------------

print()

print("-" * 70)

print(
    f"Created {len(aqi_summaries)} "
    "locality AQI summaries"
)

print(
    f"Output: {output_file}"
)