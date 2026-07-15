import csv
import math
from pathlib import Path


project_root = Path(__file__).resolve().parent.parent

localities_file = (
    project_root
    / "data"
    / "raw"
    / "localities.csv"
)

aqi_file = (
    project_root
    / "data"
    / "raw"
    / "aqi_official_snapshot.csv"
)

output_file = (
    project_root
    / "data"
    / "processed"
    / "locality_pollutant_data.csv"
)


def haversine_distance(
    latitude_1,
    longitude_1,
    latitude_2,
    longitude_2,
):
    earth_radius_km = 6371.0

    latitude_1 = math.radians(latitude_1)
    longitude_1 = math.radians(longitude_1)
    latitude_2 = math.radians(latitude_2)
    longitude_2 = math.radians(longitude_2)

    latitude_difference = latitude_2 - latitude_1
    longitude_difference = longitude_2 - longitude_1

    a = (
        math.sin(latitude_difference / 2) ** 2
        + math.cos(latitude_1)
        * math.cos(latitude_2)
        * math.sin(longitude_difference / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a),
    )

    return earth_radius_km * c


def get_coverage_label(distance_km):
    if distance_km <= 5:
        return "nearby"

    if distance_km <= 10:
        return "extended"

    return "limited"


def is_valid_pollutant_value(value):
    if value is None:
        return False

    cleaned_value = value.strip()

    if not cleaned_value:
        return False

    if cleaned_value.upper() in {
        "NA",
        "N/A",
        "NULL",
        "NONE",
        "-",
    }:
        return False

    try:
        float(cleaned_value)
        return True

    except ValueError:
        return False


with localities_file.open(
    mode="r",
    encoding="utf-8",
    newline="",
) as file:
    localities = list(csv.DictReader(file))


with aqi_file.open(
    mode="r",
    encoding="utf-8-sig",
    newline="",
) as file:
    aqi_records = list(csv.DictReader(file))


hyderabad_records = [
    record
    for record in aqi_records
    if record.get("state", "").strip().lower() == "telangana"
    and record.get("city", "").strip().lower() == "hyderabad"
]


valid_pollutant_records = []


for record in hyderabad_records:
    station_name = record.get("station", "").strip()
    pollutant_id = record.get("pollutant_id", "").strip()

    latitude = record.get("latitude", "").strip()
    longitude = record.get("longitude", "").strip()

    pollutant_avg = record.get("pollutant_avg", "")

    if not station_name or not pollutant_id:
        continue

    if not latitude or not longitude:
        continue

    if not is_valid_pollutant_value(pollutant_avg):
        continue

    try:
        latitude = float(latitude)
        longitude = float(longitude)
        pollutant_avg = float(pollutant_avg)

    except ValueError:
        continue


    valid_pollutant_records.append(
        {
            "station_name": station_name,
            "station_latitude": latitude,
            "station_longitude": longitude,
            "last_update": record.get(
                "last_update",
                "",
            ).strip(),
            "pollutant_id": pollutant_id,
            "pollutant_min": record.get(
                "pollutant_min",
                "",
            ).strip(),
            "pollutant_max": record.get(
                "pollutant_max",
                "",
            ).strip(),
            "pollutant_avg": pollutant_avg,
        }
    )


pollutants = sorted(
    {
        record["pollutant_id"]
        for record in valid_pollutant_records
    }
)


output_records = []


for locality in localities:
    locality_latitude = float(
        locality["latitude"]
    )

    locality_longitude = float(
        locality["longitude"]
    )


    for pollutant in pollutants:
        pollutant_records = [
            record
            for record in valid_pollutant_records
            if record["pollutant_id"] == pollutant
        ]


        nearest_record = None
        nearest_distance = float("inf")


        for record in pollutant_records:
            distance = haversine_distance(
                locality_latitude,
                locality_longitude,
                record["station_latitude"],
                record["station_longitude"],
            )


            if distance < nearest_distance:
                nearest_distance = distance
                nearest_record = record


        if nearest_record is None:
            continue


        output_records.append(
            {
                "locality_id": locality["locality_id"],
                "locality_name": locality["locality_name"],
                "area_group": locality["area_group"],
                "pollutant_id": pollutant,
                "pollutant_avg": nearest_record[
                    "pollutant_avg"
                ],
                "pollutant_min": nearest_record[
                    "pollutant_min"
                ],
                "pollutant_max": nearest_record[
                    "pollutant_max"
                ],
                "source_station": nearest_record[
                    "station_name"
                ],
                "station_distance_km": round(
                    nearest_distance,
                    2,
                ),
                "coverage_label": get_coverage_label(
                    nearest_distance
                ),
                "last_update": nearest_record[
                    "last_update"
                ],
            }
        )


fieldnames = [
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
]


output_file.parent.mkdir(
    parents=True,
    exist_ok=True,
)


with output_file.open(
    mode="w",
    encoding="utf-8",
    newline="",
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames,
    )

    writer.writeheader()
    writer.writerows(output_records)


print(
    "CityPulse Hyderabad - "
    "Pollutant Availability Mapping"
)

print("-" * 60)

print(
    f"Localities loaded: {len(localities)}"
)

print(
    "Valid Hyderabad pollutant records: "
    f"{len(valid_pollutant_records)}"
)

print(
    f"Pollutants detected: {len(pollutants)}"
)

print(
    f"Output records created: {len(output_records)}"
)


print("\nPollutants:")

for pollutant in pollutants:
    print(f"- {pollutant}")


print(
    "\nProcessed pollutant dataset saved to:"
)

print(output_file)


print("\nLocality pollutant summary:")


for locality in localities:
    locality_name = locality["locality_name"]

    locality_output = [
        record
        for record in output_records
        if record["locality_name"] == locality_name
    ]

    print(f"\n{locality_name}")

    for record in locality_output:
        print(
            f"  {record['pollutant_id']} -> "
            f"{record['pollutant_avg']} | "
            f"{record['source_station']} | "
            f"{record['station_distance_km']} km | "
            f"{record['coverage_label']}"
        )