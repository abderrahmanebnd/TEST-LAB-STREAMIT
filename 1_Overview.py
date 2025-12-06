"""
Main Overview Page - Paris 2024 Olympics Dashboard
The Command Center: High-level summary of the entire Games
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data, filter_data, add_continent_to_data

st.set_page_config(
    page_title="Paris 2024 Olympics - Overview",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Paris 2024 brand styling
from utils_style import inject_paris_2024_style

inject_paris_2024_style()


@st.cache_data
def load_all_data():
    return load_data()


data = load_all_data()

st.sidebar.header("🔍 Global Filters")

if not data["nocs"].empty:
    country_col = "code" if "code" in data["nocs"].columns else "NOC"
    all_countries = sorted(data["nocs"][country_col].unique().tolist())
else:
    all_countries = []

if not data["events"].empty:
    sport_col = (
        "sport"
        if "sport" in data["events"].columns
        else ("Sport" if "Sport" in data["events"].columns else None)
    )
    if sport_col:
        all_sports = sorted(data["events"][sport_col].unique().tolist())
    else:
        all_sports = []
else:
    all_sports = []

if not data["nocs"].empty:
    nocs_with_continent = add_continent_to_data(data["nocs"])
    all_continents = sorted(nocs_with_continent["Continent"].unique().tolist())
else:
    all_continents = []

selected_countries = st.sidebar.multiselect(
    "Select Countries (NOC)", options=all_countries, default=[]
)

selected_sports = st.sidebar.multiselect(
    "Select Sports", options=all_sports, default=[]
)

selected_continents = st.sidebar.multiselect(
    "Select Continents", options=all_continents, default=[]
)

st.sidebar.markdown("**Select Medal Types:**")
gold = st.sidebar.checkbox("Gold", value=True)
silver = st.sidebar.checkbox("Silver", value=True)
bronze = st.sidebar.checkbox("Bronze", value=True)

medal_types = []
if gold:
    medal_types.append("Gold")
if silver:
    medal_types.append("Silver")
if bronze:
    medal_types.append("Bronze")

st.title("🏅 Paris 2024 Olympic Games Dashboard")
st.markdown(
    """
    Welcome to the comprehensive dashboard for the Paris 2024 Olympic Games! 
    This interactive platform provides insights into athletes, countries, sports, and medal distributions.
    Use the sidebar filters to explore the data from different perspectives.
"""
)

filtered_athletes = (
    filter_data(
        data["athletes"],
        countries=selected_countries,
        sports=selected_sports,
        continents=selected_continents,
    )
    if not data["athletes"].empty
    else pd.DataFrame()
)

filtered_nocs = (
    filter_data(data["nocs"], countries=selected_countries)
    if not data["nocs"].empty
    else pd.DataFrame()
)

filtered_events = (
    filter_data(data["events"], countries=selected_countries, sports=selected_sports)
    if not data["events"].empty
    else pd.DataFrame()
)

filtered_medals_total = (
    filter_data(
        data["medals_total"], countries=selected_countries, medal_types=medal_types
    )
    if not data["medals_total"].empty
    else pd.DataFrame()
)

st.header("📊 Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_athletes = (
        len(filtered_athletes) if not filtered_athletes.empty else len(data["athletes"])
    )
    st.metric("Total Athletes", f"{total_athletes:,}")

with col2:
    total_countries = (
        len(filtered_nocs) if not filtered_nocs.empty else len(data["nocs"])
    )
    st.metric("Total Countries", f"{total_countries:,}")

with col3:
    sport_col = None
    if not filtered_events.empty:
        sport_col = (
            "sport"
            if "sport" in filtered_events.columns
            else ("Sport" if "Sport" in filtered_events.columns else None)
        )
        if sport_col:
            total_sports = filtered_events[sport_col].nunique()
        else:
            total_sports = 0
    elif not data["events"].empty:
        sport_col = (
            "sport"
            if "sport" in data["events"].columns
            else ("Sport" if "Sport" in data["events"].columns else None)
        )
        if sport_col:
            total_sports = data["events"][sport_col].nunique()
        else:
            total_sports = 0
    else:
        total_sports = 0
    st.metric("Total Sports", f"{total_sports:,}")

with col4:
    if not filtered_medals_total.empty:
        total_medals = (
            filtered_medals_total["Total"].sum()
            if "Total" in filtered_medals_total.columns
            else len(filtered_medals_total)
        )
    elif not data["medals_total"].empty:
        total_medals = (
            data["medals_total"]["Total"].sum()
            if "Total" in data["medals_total"].columns
            else len(data["medals_total"])
        )
    else:
        total_medals = 0
    st.metric("Total Medals Awarded", f"{total_medals:,}")

with col5:
    total_events = (
        len(filtered_events) if not filtered_events.empty else len(data["events"])
    )
    st.metric("Number of Events", f"{total_events:,}")

st.header("📈 Visualizations")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Global Medal Distribution")

    if not data["medals"].empty:
        medal_col = "medal_type" if "medal_type" in data["medals"].columns else "Medal"

        if medal_col in data["medals"].columns:
            medal_counts = data["medals"][medal_col].value_counts()

            medal_counts.index = medal_counts.index.str.replace(
                " Medal", "", regex=False
            )

            if medal_types:
                medal_counts = medal_counts[medal_counts.index.isin(medal_types)]

        if not medal_counts.empty:
            fig_pie = px.pie(
                values=medal_counts.values,
                names=medal_counts.index,
                title="Medal Distribution (Gold, Silver, Bronze)",
                color_discrete_map={
                    "Gold": "#FFD700",
                    "Silver": "#C0C0C0",
                    "Bronze": "#CD7F32",
                },
                hole=0.4,
            )
            fig_pie.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No medal data available for the selected filters.")
    else:
        st.info("Medal data not available.")

with col2:
    st.subheader("Top 10 Medal Standings")

    if not data["medals_total"].empty:
        top_countries = data["medals_total"].copy()

        if selected_countries:
            country_col = (
                "country_code" if "country_code" in top_countries.columns else "NOC"
            )
            if country_col in top_countries.columns:
                top_countries = top_countries[
                    top_countries[country_col].isin(selected_countries)
                ]

        if "Total" in top_countries.columns:
            top_countries = top_countries.sort_values("Total", ascending=False).head(10)

            y_col = "country_code" if "country_code" in top_countries.columns else "NOC"
            labels_dict = {"Total": "Total Medals", y_col: "Country"}
            fig_bar = px.bar(
                top_countries,
                x="Total",
                y=y_col,
                orientation="h",
                title="Top 10 Countries by Total Medals",
                labels=labels_dict,
                color="Total",
                color_continuous_scale="viridis",
            )
            fig_bar.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Total medal data not available in expected format.")
    else:
        st.info("Medal standings data not available.")

st.header("💡 Quick Insights")
insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    st.info(
        """
    **Dataset Overview:**
    - Comprehensive data from Paris 2024 Olympic Games
    - Multiple perspectives: athletes, countries, sports, and events
    - Interactive filtering for customized analysis
    """
    )

with insights_col2:
    st.info(
        """
    **Navigation:**
    - Use the sidebar to filter data across all pages
    - Explore different pages for detailed analysis
    - All visualizations are interactive and responsive
    """
    )
