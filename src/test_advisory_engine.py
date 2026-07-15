from advisory_engine import get_advisory


test_cases = [

    (
        "Good",
        "PM2.5",
    ),

    (
        "Satisfactory",
        "PM10",
    ),

    (
        "Moderately Polluted",
        "PM2.5",
    ),

    (
        "Poor",
        "NO2",
    ),

    (
        "Very Poor",
        "PM10",
    ),

    (
        "Severe",
        "PM2.5",
    ),
]


print(
    "CityPulse Hyderabad - "
    "Advisory Engine Test"
)

print("-" * 70)


for (
    category,
    pollutant,
) in test_cases:

    advisory = get_advisory(
        category,
        pollutant,
    )


    print()

    print(
        f"AQI Category: {category}"
    )

    print(
        f"Dominant Pollutant: {pollutant}"
    )

    print(
        "Health Message: "
        f"{advisory['health_message']}"
    )

    print(
        "Outdoor Guidance: "
        f"{advisory['outdoor_guidance']}"
    )

    print(
        "Sensitive Group Guidance: "
        f"{advisory['sensitive_group_guidance']}"
    )

    print(
        "Pollutant Insight: "
        f"{advisory['pollutant_insight']}"
    )

    print("-" * 70)