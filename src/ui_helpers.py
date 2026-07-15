AQI_CATEGORY_STYLES = {
    "Good": {
        "emoji": "🟢",
        "label": "Good",
        "background": "#E8F5E9",
        "border": "#2E7D32",
        "text": "#1B5E20",
    },
    "Satisfactory": {
        "emoji": "🟡",
        "label": "Satisfactory",
        "background": "#FFFDE7",
        "border": "#F9A825",
        "text": "#795548",
    },
    "Moderately Polluted": {
        "emoji": "🟠",
        "label": "Moderately Polluted",
        "background": "#FFF3E0",
        "border": "#EF6C00",
        "text": "#E65100",
    },
    "Poor": {
        "emoji": "🔴",
        "label": "Poor",
        "background": "#FFEBEE",
        "border": "#C62828",
        "text": "#B71C1C",
    },
    "Very Poor": {
        "emoji": "🟣",
        "label": "Very Poor",
        "background": "#F3E5F5",
        "border": "#7B1FA2",
        "text": "#4A148C",
    },
    "Severe": {
        "emoji": "🟤",
        "label": "Severe",
        "background": "#EFEBE9",
        "border": "#5D4037",
        "text": "#3E2723",
    },
}


DEFAULT_AQI_STYLE = {
    "emoji": "⚪",
    "label": "Unknown",
    "background": "#F5F5F5",
    "border": "#616161",
    "text": "#212121",
}


def get_aqi_style(category):
    return AQI_CATEGORY_STYLES.get(
        category,
        DEFAULT_AQI_STYLE,
    )