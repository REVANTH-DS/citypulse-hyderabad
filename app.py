from pathlib import Path
import html

import pandas as pd
import streamlit as st

from src.ui_helpers import get_aqi_style


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CityPulse Hyderabad",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

PRODUCT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "locality_advisories.csv"
)

POLLUTANT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "locality_pollutants.csv"
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 5% 0%,
                rgba(79, 70, 229, 0.10),
                transparent 28%
            ),
            radial-gradient(
                circle at 95% 5%,
                rgba(6, 182, 212, 0.10),
                transparent 25%
            ),
            #f8fafc;
    }

    .block-container {
        max-width: 1320px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }


    /* ======================================================
       HEADER
    ====================================================== */

    .brand-pill {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        background: #ede9fe;
        color: #5b21b6;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    .main-title {
        color: #0f172a;
        font-size: clamp(42px, 6vw, 76px);
        font-weight: 900;
        line-height: 0.98;
        letter-spacing: -0.055em;
        margin-bottom: 22px;
    }

    .title-accent {
        color: #4f46e5;
    }

    .main-subtitle {
        color: #64748b;
        font-size: 18px;
        line-height: 1.7;
        max-width: 780px;
        margin-bottom: 30px;
    }


    /* ======================================================
       LOCATION
    ====================================================== */

    .locality-header {
        margin-top: 38px;
        margin-bottom: 20px;
    }

    .eyebrow {
        color: #6366f1;
        font-size: 12px;
        font-weight: 850;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .locality-name {
        color: #0f172a;
        font-size: clamp(36px, 5vw, 58px);
        font-weight: 900;
        letter-spacing: -0.05em;
        line-height: 1;
        margin-top: 10px;
    }

    .locality-area {
        color: #64748b;
        font-size: 16px;
        margin-top: 12px;
    }


    /* ======================================================
       HERO
    ====================================================== */

    .aqi-hero {
        position: relative;
        overflow: hidden;
        padding: 45px;
        border-radius: 32px;
        border: 1px solid rgba(15, 23, 42, 0.08);
        box-shadow: 0 25px 70px rgba(15, 23, 42, 0.12);
        margin-bottom: 25px;
    }

    .aqi-hero::before {
        content: "";
        position: absolute;
        width: 420px;
        height: 420px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.30);
        right: -170px;
        top: -220px;
    }

    .aqi-layout {
        position: relative;
        z-index: 2;
        display: grid;
        grid-template-columns: 0.8fr 1.2fr;
        gap: 55px;
        align-items: center;
    }

    .aqi-label {
        font-size: 12px;
        font-weight: 850;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        opacity: 0.72;
    }

    .aqi-value {
        font-size: clamp(90px, 12vw, 155px);
        font-weight: 950;
        line-height: 0.85;
        letter-spacing: -0.08em;
        margin-top: 28px;
    }

    .aqi-badge {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 11px 18px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.62);
        font-size: 20px;
        font-weight: 850;
        margin-top: 30px;
    }

    .aqi-explanation-title {
        font-size: 28px;
        font-weight: 900;
        letter-spacing: -0.03em;
        line-height: 1.2;
    }

    .aqi-explanation {
        font-size: 16px;
        line-height: 1.8;
        margin-top: 16px;
        max-width: 550px;
        opacity: 0.85;
    }

    .aqi-action {
        margin-top: 22px;
        padding: 16px 18px;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.52);
        font-size: 15px;
        line-height: 1.6;
        font-weight: 700;
    }


    /* ======================================================
       QUICK METRICS
    ====================================================== */

    .metric-card {
        min-height: 190px;
        padding: 27px;
        border-radius: 23px;
        background: rgba(255, 255, 255, 0.90);
        border: 1px solid #e2e8f0;
        box-shadow: 0 12px 35px rgba(15, 23, 42, 0.055);
    }

    .metric-icon {
        font-size: 31px;
        margin-bottom: 18px;
    }

    .metric-label {
        color: #64748b;
        font-size: 11px;
        font-weight: 850;
        letter-spacing: 0.10em;
        text-transform: uppercase;
    }

    .metric-value {
        color: #0f172a;
        font-size: 26px;
        font-weight: 900;
        letter-spacing: -0.035em;
        margin-top: 8px;
    }

    .metric-description {
        color: #64748b;
        font-size: 13px;
        line-height: 1.6;
        margin-top: 10px;
    }


    /* ======================================================
       SECTION
    ====================================================== */

    .section {
        margin-top: 65px;
    }

    .section-label {
        color: #4f46e5;
        font-size: 12px;
        font-weight: 850;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .section-title {
        color: #0f172a;
        font-size: clamp(30px, 4vw, 45px);
        font-weight: 900;
        letter-spacing: -0.045em;
        line-height: 1.1;
        margin-top: 9px;
        margin-bottom: 25px;
    }

    .section-description {
        color: #64748b;
        font-size: 16px;
        line-height: 1.7;
        max-width: 760px;
        margin-top: -10px;
        margin-bottom: 28px;
    }


    /* ======================================================
       INSIGHTS
    ====================================================== */

    .insight-card {
        min-height: 310px;
        padding: 31px;
        border-radius: 25px;
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid #e2e8f0;
        box-shadow: 0 14px 40px rgba(15, 23, 42, 0.055);
        margin-bottom: 18px;
    }

    .insight-icon {
        font-size: 38px;
    }

    .insight-title {
        color: #0f172a;
        font-size: 22px;
        font-weight: 900;
        letter-spacing: -0.025em;
        margin-top: 19px;
    }

    .insight-text {
        color: #475569;
        font-size: 15px;
        line-height: 1.85;
        margin-top: 14px;
    }


    /* ======================================================
       SOURCE PANEL
    ====================================================== */

    .source-panel {
        padding: 38px;
        border-radius: 28px;
        background:
            linear-gradient(
                135deg,
                #0f172a,
                #172554
            );
        color: white;
        box-shadow: 0 25px 65px rgba(15, 23, 42, 0.20);
    }

    .source-item {
        padding: 18px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    }

    .source-item:last-child {
        border-bottom: none;
    }

    .source-label {
        color: #94a3b8;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .source-value {
        color: #f8fafc;
        font-size: 18px;
        font-weight: 750;
        line-height: 1.5;
        margin-top: 6px;
    }

    .source-description {
        color: #cbd5e1;
        font-size: 13px;
        line-height: 1.6;
        margin-top: 5px;
    }


    /* ======================================================
       METHODOLOGY
    ====================================================== */

    .method-card {
        min-height: 255px;
        padding: 28px;
        border-radius: 23px;
        background: white;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
    }

    .method-number {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 46px;
        height: 46px;
        border-radius: 15px;
        background: #eef2ff;
        color: #4f46e5;
        font-size: 19px;
        font-weight: 900;
    }

    .method-title {
        color: #0f172a;
        font-size: 18px;
        font-weight: 850;
        margin-top: 20px;
    }

    .method-text {
        color: #64748b;
        font-size: 14px;
        line-height: 1.75;
        margin-top: 11px;
    }


    /* ======================================================
       POLLUTANTS
    ====================================================== */

    .pollutant-card {
        padding: 22px;
        border-radius: 19px;
        background: white;
        border: 1px solid #e2e8f0;
        margin-bottom: 12px;
    }

    .pollutant-name {
        color: #0f172a;
        font-size: 19px;
        font-weight: 850;
    }

    .pollutant-value {
        color: #4f46e5;
        font-size: 26px;
        font-weight: 900;
        margin-top: 5px;
    }

    .pollutant-meta {
        color: #64748b;
        font-size: 13px;
        margin-top: 6px;
        line-height: 1.5;
    }


    /* ======================================================
       FOOTER
    ====================================================== */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 13px;
        line-height: 1.8;
        padding-top: 70px;
        padding-bottom: 25px;
    }


    /* ======================================================
       SELECT
    ====================================================== */

    div[data-baseweb="select"] > div {
        min-height: 58px;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.95);
        border-color: #cbd5e1;
    }


    /* ======================================================
       MOBILE
    ====================================================== */

    @media (max-width: 800px) {

        .aqi-layout {
            grid-template-columns: 1fr;
            gap: 35px;
        }

        .aqi-hero {
            padding: 30px;
        }

        .metric-card,
        .insight-card,
        .method-card {
            min-height: auto;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def safe_text(value):
    if pd.isna(value):
        return "Not available"

    return html.escape(str(value))


def metric_card(
    icon,
    label,
    value,
    description,
):
    return (
        '<div class="metric-card">'
        f'<div class="metric-icon">{icon}</div>'
        f'<div class="metric-label">{safe_text(label)}</div>'
        f'<div class="metric-value">{safe_text(value)}</div>'
        f'<div class="metric-description">'
        f'{safe_text(description)}'
        '</div>'
        '</div>'
    )


def insight_card(
    icon,
    title,
    text,
):
    return (
        '<div class="insight-card">'
        f'<div class="insight-icon">{icon}</div>'
        f'<div class="insight-title">{safe_text(title)}</div>'
        f'<div class="insight-text">{safe_text(text)}</div>'
        '</div>'
    )


def method_card(
    number,
    title,
    text,
):
    return (
        '<div class="method-card">'
        f'<div class="method-number">{number}</div>'
        f'<div class="method-title">{safe_text(title)}</div>'
        f'<div class="method-text">{safe_text(text)}</div>'
        '</div>'
    )


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_product_data():
    return pd.read_csv(PRODUCT_FILE)


@st.cache_data
def load_pollutant_data():
    if not POLLUTANT_FILE.exists():
        return pd.DataFrame()

    return pd.read_csv(POLLUTANT_FILE)


if not PRODUCT_FILE.exists():
    st.error(
        "CityPulse product dataset was not found."
    )
    st.stop()


product_data = load_product_data()

pollutant_data = load_pollutant_data()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    (
        '<div class="brand-pill">'
        '🏙️ CityPulse Hyderabad'
        '</div>'
        '<div class="main-title">'
        'Our <span class="title-accent">'
        'Hyderabad.</span><br>'
        'Our Air Quality.'
        '</div>'
        '<div class="main-subtitle">'
        'CityPulse transforms available monitoring-station '
        'observations into understandable locality-level '
        'air-quality estimates. Explore the air around your '
        'locality, understand the dominant pollutant and learn '
        'what the conditions may mean for your daily routine.'
        '</div>'
    ),
    unsafe_allow_html=True,
)


# ============================================================
# LOCALITY SELECTOR
# ============================================================

localities = sorted(
    product_data["locality_name"]
    .dropna()
    .unique()
    .tolist()
)


selected_locality = st.selectbox(
    "📍 Select a Hyderabad locality",
    localities,
)


selected_rows = product_data[
    product_data["locality_name"]
    == selected_locality
]


if selected_rows.empty:
    st.warning(
        "No CityPulse data available."
    )
    st.stop()


locality = selected_rows.iloc[0]


estimated_aqi = int(
    float(locality["estimated_aqi"])
)


aqi_category = str(
    locality["aqi_category"]
)


aqi_style = get_aqi_style(
    aqi_category
)


# ============================================================
# LOCALITY HEADER
# ============================================================

st.markdown(
    (
        '<div class="locality-header">'
        '<div class="eyebrow">'
        'Current locality intelligence'
        '</div>'
        '<div class="locality-name">'
        f'📍 {safe_text(selected_locality)}'
        '</div>'
        '<div class="locality-area">'
        f'{safe_text(locality["area_group"])} Hyderabad'
        '</div>'
        '</div>'
    ),
    unsafe_allow_html=True,
)


# ============================================================
# AQI HERO
# ============================================================

hero_html = (
    f'<div class="aqi-hero" '
    f'style="'
    f'background:{aqi_style["background"]};'
    f'color:{aqi_style["text"]};'
    f'border-left:8px solid {aqi_style["border"]};'
    f'">'
    '<div class="aqi-layout">'
    '<div>'
    '<div class="aqi-label">'
    'CityPulse Estimated AQI'
    '</div>'
    f'<div class="aqi-value">{estimated_aqi}</div>'
    '<div class="aqi-badge">'
    f'{aqi_style["emoji"]} '
    f'{safe_text(aqi_category)}'
    '</div>'
    '</div>'
    '<div>'
    '<div class="aqi-explanation-title">'
    f'Air quality is in the '
    f'{safe_text(aqi_category.lower())} range.'
    '</div>'
    '<div class="aqi-explanation">'
    f'{safe_text(locality["health_message"])} '
    'CityPulse estimates the locality condition using '
    'the closest available monitoring observations and '
    'the pollutant with the highest calculated sub-index.'
    '</div>'
    '<div class="aqi-action">'
    '🛡️ '
    f'{safe_text(locality["outdoor_guidance"])}'
    '</div>'
    '</div>'
    '</div>'
    '</div>'
)


st.markdown(
    hero_html,
    unsafe_allow_html=True,
)


# ============================================================
# QUICK METRICS
# ============================================================

metric_1, metric_2, metric_3, metric_4 = st.columns(4)


with metric_1:

    st.markdown(
        metric_card(
            "🧪",
            "Dominant Pollutant",
            locality["dominant_pollutant"],
            (
                "This pollutant produced the highest "
                "calculated sub-index and therefore had "
                "the strongest influence on the final "
                "CityPulse AQI estimate."
            ),
        ),
        unsafe_allow_html=True,
    )


with metric_2:

    st.markdown(
        metric_card(
            "🔬",
            "Pollutants Analysed",
            int(locality["pollutants_used"]),
            (
                "CityPulse evaluates the available "
                "pollutant observations associated with "
                "the selected monitoring station before "
                "calculating the final estimate."
            ),
        ),
        unsafe_allow_html=True,
    )


with metric_3:

    st.markdown(
        metric_card(
            "📡",
            "Coverage",
            str(
                locality["coverage_label"]
            ).title(),
            (
                "Coverage describes the geographic "
                "relationship between this locality and "
                "the monitoring station used to estimate "
                "local air-quality conditions."
            ),
        ),
        unsafe_allow_html=True,
    )


with metric_4:

    st.markdown(
        metric_card(
            "🕒",
            "Observation Updated",
            locality["last_update"],
            (
                "The AQI estimate uses pollutant "
                "observations available up to this "
                "timestamp in the downloaded official "
                "air-quality snapshot."
            ),
        ),
        unsafe_allow_html=True,
    )


# ============================================================
# WHAT THIS MEANS
# ============================================================

st.markdown(
    (
        '<div class="section">'
        '<div class="section-label">'
        'CityPulse guidance'
        '</div>'
        '<div class="section-title">'
        'What does this mean for you?'
        '</div>'
        '<div class="section-description">'
        'AQI numbers are easier to use when they are '
        'translated into everyday context. These insights '
        'explain the pollutant signal, possible health '
        'impact and practical outdoor considerations.'
        '</div>'
        '</div>'
    ),
    unsafe_allow_html=True,
)


insight_1, insight_2 = st.columns(2)


with insight_1:

    st.markdown(
        insight_card(
            "🧪",
            "Pollutant Insight",
            locality["pollutant_insight"],
        ),
        unsafe_allow_html=True,
    )


with insight_2:

    st.markdown(
        insight_card(
            "🫁",
            "Health Impact",
            locality["health_message"],
        ),
        unsafe_allow_html=True,
    )


insight_3, insight_4 = st.columns(2)


with insight_3:

    st.markdown(
        insight_card(
            "🚶",
            "Outdoor Guidance",
            locality["outdoor_guidance"],
        ),
        unsafe_allow_html=True,
    )


with insight_4:

    st.markdown(
        insight_card(
            "👥",
            "Sensitive Groups",
            locality[
                "sensitive_group_guidance"
            ],
        ),
        unsafe_allow_html=True,
    )


# ============================================================
# DATA SOURCE
# ============================================================

st.markdown(
    (
        '<div class="section">'
        '<div class="section-label">'
        'Data transparency'
        '</div>'
        '<div class="section-title">'
        'Where does this estimate come from?'
        '</div>'
        '<div class="section-description">'
        'CityPulse does not pretend that every locality has '
        'its own physical monitoring station. The estimate '
        'is linked to the nearest supported monitoring '
        'observation and clearly exposes that relationship.'
        '</div>'
        '</div>'
    ),
    unsafe_allow_html=True,
)


source_html = (
    '<div class="source-panel">'

    '<div class="source-item">'
    '<div class="source-label">'
    'Monitoring station'
    '</div>'
    '<div class="source-value">'
    f'{safe_text(locality["nearest_station"])}'
    '</div>'
    '<div class="source-description">'
    'The nearest supported station selected through '
    'geographic distance mapping.'
    '</div>'
    '</div>'

    '<div class="source-item">'
    '<div class="source-label">'
    'Distance from locality'
    '</div>'
    '<div class="source-value">'
    f'{safe_text(locality["station_distance_km"])} km'
    '</div>'
    '<div class="source-description">'
    'Straight-line geographic distance between the '
    'representative locality coordinates and station.'
    '</div>'
    '</div>'

    '<div class="source-item">'
    '<div class="source-label">'
    'Coverage classification'
    '</div>'
    '<div class="source-value">'
    f'{safe_text(locality["coverage_label"]).title()}'
    '</div>'
    '<div class="source-description">'
    'A CityPulse label that communicates the geographic '
    'proximity of the monitoring observation.'
    '</div>'
    '</div>'

    '<div class="source-item">'
    '<div class="source-label">'
    'Observation timestamp'
    '</div>'
    '<div class="source-value">'
    f'{safe_text(locality["last_update"])}'
    '</div>'
    '<div class="source-description">'
    'Latest timestamp represented in the observation '
    'used for this locality estimate.'
    '</div>'
    '</div>'

    '</div>'
)


st.markdown(
    source_html,
    unsafe_allow_html=True,
)


# ============================================================
# METHODOLOGY
# ============================================================

st.markdown(
    (
        '<div class="section">'
        '<div class="section-label">'
        'Calculation pipeline'
        '</div>'
        '<div class="section-title">'
        'How did CityPulse calculate this AQI?'
        '</div>'
        '<div class="section-description">'
        'The number shown above is produced through a '
        'transparent five-stage data pipeline. CityPulse '
        'maps location data, processes available pollutants '
        'and converts the strongest pollutant signal into '
        'an understandable locality estimate.'
        '</div>'
        '</div>'
    ),
    unsafe_allow_html=True,
)


method_1, method_2, method_3 = st.columns(3)


with method_1:

    st.markdown(
        method_card(
            "01",
            "Find the nearest station",
            (
                f"CityPulse starts with the coordinates of "
                f"{selected_locality}. Geographic distance "
                f"is calculated against supported Hyderabad "
                f"monitoring stations. The nearest available "
                f"station becomes the observation source."
            ),
        ),
        unsafe_allow_html=True,
    )


with method_2:

    st.markdown(
        method_card(
            "02",
            "Collect pollutant observations",
            (
                "Available pollutant records from the mapped "
                "station are grouped together. CityPulse "
                "processes supported pollutants such as "
                "PM2.5, PM10, NO2, SO2, CO, OZONE and NH3 "
                "when observations are available."
            ),
        ),
        unsafe_allow_html=True,
    )


with method_3:

    st.markdown(
        method_card(
            "03",
            "Calculate pollutant sub-indices",
            (
                "Each available pollutant concentration is "
                "passed through the CityPulse AQI engine. "
                "Concentration breakpoints are used to "
                "estimate an individual AQI sub-index for "
                "each supported pollutant."
            ),
        ),
        unsafe_allow_html=True,
    )


method_4, method_5 = st.columns(2)


with method_4:

    st.markdown(
        method_card(
            "04",
            "Select the highest sub-index",
            (
                f"The pollutant producing the highest "
                f"calculated sub-index becomes the dominant "
                f"pollutant. For {selected_locality}, the "
                f"current dominant pollutant is "
                f"{locality['dominant_pollutant']}. The "
                f"highest sub-index becomes the estimated AQI."
            ),
        ),
        unsafe_allow_html=True,
    )


with method_5:

    st.markdown(
        method_card(
            "05",
            "Translate AQI into guidance",
            (
                f"The estimated AQI is classified into the "
                f"{aqi_category} category. CityPulse then "
                f"adds pollutant context, health messaging, "
                f"outdoor guidance and information for "
                f"sensitive groups so the result is easier "
                f"to understand."
            ),
        ),
        unsafe_allow_html=True,
    )


# ============================================================
# POLLUTANT BREAKDOWN
# ============================================================

if not pollutant_data.empty:

    locality_pollutants = pollutant_data[
        pollutant_data["locality_name"]
        == selected_locality
    ]

    if not locality_pollutants.empty:

        st.markdown(
            (
                '<div class="section">'
                '<div class="section-label">'
                'Pollutant intelligence'
                '</div>'
                '<div class="section-title">'
                'Pollutants behind the estimate'
                '</div>'
                '<div class="section-description">'
                'The final AQI is not calculated by averaging '
                'all pollutants together. CityPulse calculates '
                'individual pollutant sub-indices and uses the '
                'highest valid sub-index as the final AQI '
                'estimate.'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )


        pollutant_columns = st.columns(3)


        for index, (_, row) in enumerate(
            locality_pollutants.iterrows()
        ):

            column = pollutant_columns[
                index % 3
            ]


            with column:

                pollutant_html = (
                    '<div class="pollutant-card">'
                    '<div class="pollutant-name">'
                    f'{safe_text(row["pollutant_id"])}'
                    '</div>'
                    '<div class="pollutant-value">'
                    f'{safe_text(row["pollutant_avg"])}'
                    '</div>'
                    '<div class="pollutant-meta">'
                    'Average concentration'
                    '<br>'
                    f'Min: '
                    f'{safe_text(row["pollutant_min"])}'
                    ' · '
                    f'Max: '
                    f'{safe_text(row["pollutant_max"])}'
                    '</div>'
                    '</div>'
                )


                st.markdown(
                    pollutant_html,
                    unsafe_allow_html=True,
                )


# ============================================================
# FINAL METHODOLOGY NOTE
# ============================================================

with st.expander(
    "📘 Read the CityPulse methodology note"
):

    st.markdown(
        """
### What CityPulse is

CityPulse Hyderabad is a locality-level air-quality
analytics project.

The application uses available monitoring-station
observations and geographic locality mapping to create
an easier-to-understand environmental view for selected
Hyderabad localities.

### Why nearest-station mapping is used

Air-quality monitoring stations are not installed in
every locality.

CityPulse therefore calculates geographic distance
between representative locality coordinates and
available monitoring stations.

The nearest supported station is selected as the
observation source.

### How the AQI estimate is produced

For each locality, CityPulse identifies the pollutants
available at the mapped monitoring station.

Supported pollutant concentrations are processed using
the AQI calculation engine.

Each pollutant produces an individual sub-index.

The highest valid pollutant sub-index determines the
final CityPulse estimated AQI and dominant pollutant.

### Important limitation

The value displayed by CityPulse is an analytical
locality-level estimate.

It should not be interpreted as an official physical
AQI measurement taken directly inside the selected
locality.

Monitoring coverage, station distance and pollutant
availability can influence the estimate.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    (
        '<div class="footer">'
        '<strong>CityPulse Hyderabad</strong>'
        '<br>'
        'Local insights · Transparent methodology · '
        'Understandable air-quality intelligence'
        '<br><br>'
        'General environmental guidance only. '
        'Not medical advice.'
        '</div>'
    ),
    unsafe_allow_html=True,
)