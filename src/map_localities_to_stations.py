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
    / "locality_station_mapping.csv"
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


stations = {}


for record in hyderabad_records:
    station_name = record.get("station", "").strip()
    latitude = record.get("latitude", "").strip()
    longitude = record.get("longitude", "").strip()

    if not station_name or not latitude or not longitude:
        continue

    try:
        latitude = float(latitude)
        longitude = float(longitude)

    except ValueError:
        continue

    stations[station_name] = {
        "station": station_name,
        "latitude": latitude,
        "longitude": longitude,
    }


mapping_records = []


for locality in localities:
    locality_latitude = float(locality["latitude"])
    locality_longitude = float(locality["longitude"])

    nearest_station = None
    nearest_distance = float("inf")


    for station in stations.values():
        distance = haversine_distance(
            locality_latitude,
            locality_longitude,
            station["latitude"],
            station["longitude"],
        )

        if distance < nearest_distance:
            nearest_distance = distance
            nearest_station = station


    if nearest_station is None:
        continue


    mapping_records.append(
        {
            "locality_id": locality["locality_id"],
            "locality_name": locality["locality_name"],
            "locality_latitude": locality["latitude"],
            "locality_longitude": locality["longitude"],
            "area_group": locality["area_group"],
            "station_name": nearest_station["station"],
            "station_latitude": nearest_station["latitude"],
            "station_longitude": nearest_station["longitude"],
            "distance_km": round(nearest_distance, 2),
            "coverage_label": get_coverage_label(
                nearest_distance
            ),
        }
    )


fieldnames = [
    "locality_id",
    "locality_name",
    "locality_latitude",
    "locality_longitude",
    "area_group",
    "station_name",
    "station_latitude",
    "station_longitude",
    "distance_km",
    "coverage_label",
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
    writer.writerows(mapping_records)


print("CityPulse Hyderabad - Locality Station Mapping")
print("-" * 60)

print(f"Localities loaded: {len(localities)}")
print(f"Unique AQI stations: {len(stations)}")
print(f"Mappings created: {len(mapping_records)}")

print(
    "\nProcessed mapping saved to:"
    f"\n{output_file}"
)


print("\nMapping summary:")


for record in mapping_records:
    print(
        f"{record['locality_name']} -> "
        f"{record['station_name']} | "
        f"{record['distance_km']} km | "
        f"{record['coverage_label']}"
    )