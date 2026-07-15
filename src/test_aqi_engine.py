from aqi_engine import (
    calculate_sub_index,
    get_aqi_category,
)


test_cases = [
    ("PM2.5", 20),
    ("PM2.5", 45),
    ("PM2.5", 75),
    ("PM10", 75),
    ("NO2", 120),
    ("SO2", 50),
    ("NH3", 300),
]


print("CityPulse Hyderabad - AQI Engine Test")
print("-" * 60)


for pollutant_id, concentration in test_cases:
    sub_index = calculate_sub_index(
        pollutant_id,
        concentration,
    )

    category = get_aqi_category(
        sub_index
    )

    print(
        f"{pollutant_id} | "
        f"Concentration: {concentration} | "
        f"Sub-index: {sub_index} | "
        f"Category: {category}"
    )