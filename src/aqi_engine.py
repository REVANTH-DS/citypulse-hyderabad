AQI_BREAKPOINTS = {
    "PM10": [
        (0, 50, 0, 50),
        (51, 100, 51, 100),
        (101, 250, 101, 200),
        (251, 350, 201, 300),
        (351, 430, 301, 400),
        (431, float("inf"), 401, 500),
    ],
    "PM2.5": [
        (0, 30, 0, 50),
        (31, 60, 51, 100),
        (61, 90, 101, 200),
        (91, 120, 201, 300),
        (121, 250, 301, 400),
        (251, float("inf"), 401, 500),
    ],
    "NO2": [
        (0, 40, 0, 50),
        (41, 80, 51, 100),
        (81, 180, 101, 200),
        (181, 280, 201, 300),
        (281, 400, 301, 400),
        (401, float("inf"), 401, 500),
    ],
    "OZONE": [
        (0, 50, 0, 50),
        (51, 100, 51, 100),
        (101, 168, 101, 200),
        (169, 208, 201, 300),
        (209, 748, 301, 400),
        (749, float("inf"), 401, 500),
    ],
    "CO": [
        (0, 1.0, 0, 50),
        (1.1, 2.0, 51, 100),
        (2.1, 10, 101, 200),
        (10.1, 17, 201, 300),
        (17.1, 34, 301, 400),
        (34.1, float("inf"), 401, 500),
    ],
    "SO2": [
        (0, 40, 0, 50),
        (41, 80, 51, 100),
        (81, 380, 101, 200),
        (381, 800, 201, 300),
        (801, 1600, 301, 400),
        (1601, float("inf"), 401, 500),
    ],
    "NH3": [
        (0, 200, 0, 50),
        (201, 400, 51, 100),
        (401, 800, 101, 200),
        (801, 1200, 201, 300),
        (1201, 1800, 301, 400),
        (1801, float("inf"), 401, 500),
    ],
}


def calculate_sub_index(
    pollutant_id,
    concentration,
):
    if pollutant_id not in AQI_BREAKPOINTS:
        return None

    try:
        concentration = float(concentration)

    except (TypeError, ValueError):
        return None

    if concentration < 0:
        return None

    breakpoints = AQI_BREAKPOINTS[pollutant_id]

    for (
        concentration_low,
        concentration_high,
        index_low,
        index_high,
    ) in breakpoints:

        if concentration < concentration_low:
            continue

        if concentration_high == float("inf"):
            return 500

        if concentration <= concentration_high:
            sub_index = (
                (
                    index_high - index_low
                )
                / (
                    concentration_high
                    - concentration_low
                )
                * (
                    concentration
                    - concentration_low
                )
                + index_low
            )

            return round(sub_index)

    return None


def get_aqi_category(aqi_value):
    if aqi_value is None:
        return None

    if aqi_value <= 50:
        return "Good"

    if aqi_value <= 100:
        return "Satisfactory"

    if aqi_value <= 200:
        return "Moderately Polluted"

    if aqi_value <= 300:
        return "Poor"

    if aqi_value <= 400:
        return "Very Poor"

    return "Severe"