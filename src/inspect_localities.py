import csv
from pathlib import Path


project_root = Path(__file__).resolve().parent.parent

localities_file = project_root / "data" / "raw" / "localities.csv"


with localities_file.open(mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    localities = list(reader)


print("CityPulse Hyderabad - Locality Data Inspection")
print("-" * 50)

print(f"Total localities: {len(localities)}")

print("\nLocality records:")

for locality in localities:
    print(
        locality["locality_id"],
        locality["locality_name"],
        locality["area_group"],
    )
    