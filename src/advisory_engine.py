AQI_ADVISORIES = {

    "Good": {
        "health_message": (
            "Air quality is considered good "
            "with minimal expected health impact."
        ),
        "outdoor_guidance": (
            "Normal outdoor activities can "
            "generally continue."
        ),
        "sensitive_group_guidance": (
            "No special air-quality precautions "
            "are generally required."
        ),
    },

    "Satisfactory": {
        "health_message": (
            "Air quality is generally acceptable, "
            "but minor breathing discomfort may "
            "occur in sensitive people."
        ),
        "outdoor_guidance": (
            "Normal outdoor activities can "
            "generally continue."
        ),
        "sensitive_group_guidance": (
            "Sensitive people should pay attention "
            "to unusual breathing discomfort."
        ),
    },

    "Moderately Polluted": {
        "health_message": (
            "Air quality may cause breathing "
            "discomfort in people with lung, "
            "asthma, or heart conditions."
        ),
        "outdoor_guidance": (
            "Consider reducing prolonged or heavy "
            "outdoor activity if discomfort occurs."
        ),
        "sensitive_group_guidance": (
            "Sensitive groups should consider "
            "limiting prolonged outdoor exertion."
        ),
    },

    "Poor": {
        "health_message": (
            "Air quality may cause breathing "
            "discomfort to many people during "
            "prolonged exposure."
        ),
        "outdoor_guidance": (
            "Consider reducing prolonged and "
            "heavy outdoor activity."
        ),
        "sensitive_group_guidance": (
            "Sensitive groups should limit "
            "prolonged outdoor exertion."
        ),
    },

    "Very Poor": {
        "health_message": (
            "Air quality may cause respiratory "
            "illness or increased discomfort "
            "during prolonged exposure."
        ),
        "outdoor_guidance": (
            "Avoid prolonged or heavy outdoor "
            "activity when possible."
        ),
        "sensitive_group_guidance": (
            "Sensitive groups should minimize "
            "outdoor exertion."
        ),
    },

    "Severe": {
        "health_message": (
            "Air quality may affect healthy people "
            "and seriously impact people with "
            "existing respiratory or heart conditions."
        ),
        "outdoor_guidance": (
            "Avoid heavy outdoor activity and "
            "reduce outdoor exposure when possible."
        ),
        "sensitive_group_guidance": (
            "Sensitive groups should avoid outdoor "
            "exertion when possible."
        ),
    },
}


POLLUTANT_INSIGHTS = {

    "PM2.5": (
        "Fine particulate matter is the dominant "
        "pollutant in this locality estimate."
    ),

    "PM10": (
        "Coarse particulate matter is the dominant "
        "pollutant in this locality estimate."
    ),

    "NO2": (
        "Nitrogen dioxide is the dominant pollutant "
        "in this locality estimate."
    ),

    "SO2": (
        "Sulfur dioxide is the dominant pollutant "
        "in this locality estimate."
    ),

    "CO": (
        "Carbon monoxide is the dominant pollutant "
        "in this locality estimate."
    ),

    "OZONE": (
        "Ground-level ozone is the dominant "
        "pollutant in this locality estimate."
    ),

    "NH3": (
        "Ammonia is the dominant pollutant "
        "in this locality estimate."
    ),
}


def get_advisory(
    aqi_category,
    dominant_pollutant,
):

    advisory = AQI_ADVISORIES.get(
        aqi_category
    )


    if advisory is None:

        advisory = {
            "health_message": (
                "Air-quality guidance is "
                "currently unavailable."
            ),
            "outdoor_guidance": (
                "Check official local air-quality "
                "information before planning "
                "outdoor activity."
            ),
            "sensitive_group_guidance": (
                "Sensitive people should use "
                "appropriate caution."
            ),
        }


    pollutant_insight = (
        POLLUTANT_INSIGHTS.get(
            dominant_pollutant,
            (
                "Dominant pollutant information "
                "is available in the AQI estimate."
            ),
        )
    )


    return {
        "health_message": advisory[
            "health_message"
        ],
        "outdoor_guidance": advisory[
            "outdoor_guidance"
        ],
        "sensitive_group_guidance": advisory[
            "sensitive_group_guidance"
        ],
        "pollutant_insight": pollutant_insight,
    }