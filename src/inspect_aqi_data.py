import csv
from collections import Counter
from pathlib import Path


project_root = Path(__file__).resolve().parent.parent

aqi_file = (
    project_root
    / "data"
    / "raw"
    / "aqi_official_snapshot.csv"
)


with aqi_file.open(
    mode="r",
    encoding="utf-8-sig",
    newline="",
) as file:
    reader = csv.DictReader(file)

    columns = reader.fieldnames or []
    records = list(reader)


print("CityPulse Hyderabad - Official AQI Snapshot Inspection")
print("-" * 60)

print(f"Total records: {len(records)}")


print("\nColumns:")

for column in columns:
    print(f"- {column}")


states = Counter(
    record.get("state", "").strip()
    for record in records
    if record.get("state", "").strip()
)


cities = Counter(
    record.get("city", "").strip()
    for record in records
    if record.get("city", "").strip()
)


pollutants = Counter(
    record.get("pollutant_id", "").strip()
    for record in records
    if record.get("pollutant_id", "").strip()
)


telangana_records = [
    record
    for record in records
    if record.get("state", "").strip().lower() == "telangana"
]


hyderabad_records = [
    record
    for record in telangana_records
    if record.get("city", "").strip().lower() == "hyderabad"
]


hyderabad_stations = sorted(
    {
        record.get("station", "").strip()
        for record in hyderabad_records
        if record.get("station", "").strip()
    }
)


hyderabad_pollutants = Counter(
    record.get("pollutant_id", "").strip()
    for record in hyderabad_records
    if record.get("pollutant_id", "").strip()
)


print("\nDataset coverage:")
print(f"Unique states: {len(states)}")
print(f"Unique cities: {len(cities)}")


print("\nPollutants in full snapshot:")

for pollutant, count in sorted(pollutants.items()):
    print(f"- {pollutant}: {count} records")


print("\nHyderabad coverage:")
print(f"Telangana records: {len(telangana_records)}")
print(f"Hyderabad records: {len(hyderabad_records)}")
print(f"Unique Hyderabad stations: {len(hyderabad_stations)}")


print("\nHyderabad monitoring stations:")

for station in hyderabad_stations:
    print(f"- {station}")


print("\nPollutants available for Hyderabad:")

for pollutant, count in sorted(hyderabad_pollutants.items()):
    print(f"- {pollutant}: {count} records")


if hyderabad_records:
    print("\nFirst Hyderabad record:")

    first_record = hyderabad_records[0]

    for column in columns:
        print(f"{column}: {first_record.get(column)}")