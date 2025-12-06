"""
Global Analysis Page - Paris 2024 Olympics Dashboard
The World View: Geographical and hierarchical perspective
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data, filter_data, add_continent_to_data

st.set_page_config(
    page_title="Global Analysis - Paris 2024 Olympics",
    page_icon="🗺️",
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

st.title("🗺️ Global Analysis")
st.markdown(
    "Explore the Olympic Games from a geographical and hierarchical perspective"
)

if not data["medals_total"].empty:
    medals_with_continent = add_continent_to_data(data["medals_total"])
    filtered_medals = filter_data(
        medals_with_continent,
        countries=selected_countries,
        continents=selected_continents,
        medal_types=medal_types,
    )
else:
    filtered_medals = pd.DataFrame()

st.header("🌍 World Medal Map")
st.markdown("Countries color-coded by total medal count")

if not filtered_medals.empty and "Total" in filtered_medals.columns:
    country_col = (
        "country_code"
        if "country_code" in filtered_medals.columns
        else ("NOC" if "NOC" in filtered_medals.columns else "code")
    )

    if country_col in filtered_medals.columns:
        fig_map = px.choropleth(
            filtered_medals,
            locations=country_col,
            locationmode="ISO-3",
            color="Total",
            hover_name=country_col,
            hover_data=["Total"],
            color_continuous_scale="viridis",
            title="World Medal Distribution",
            labels={"Total": "Total Medals"},
        )
    fig_map.update_layout(height=600)
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.info("Medal data not available for world map visualization.")

st.header("🌳 Medal Hierarchy by Continent")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Sunburst Chart")
    st.markdown("Hierarchy: Continent → Country → Sport → Medal Count")

    if not data["medals"].empty and not data["events"].empty:
        medals_df = data["medals"].copy()
        events_df = data["events"].copy()

        country_col = (
            "country_code"
            if "country_code" in medals_df.columns
            else ("NOC" if "NOC" in medals_df.columns else "code")
        )
        if country_col in medals_df.columns:
            medals_with_continent = add_continent_to_data(medals_df, country_col)

            event_col_medals = "event" if "event" in medals_df.columns else "Event"
            event_col_events = "event" if "event" in events_df.columns else "Event"
            sport_col_events = "sport" if "sport" in events_df.columns else "Sport"

            if (
                event_col_medals in medals_df.columns
                and event_col_events in events_df.columns
            ):
                events_for_merge = events_df[
                    [event_col_events, sport_col_events]
                ].drop_duplicates()
                events_for_merge = events_for_merge.rename(
                    columns={event_col_events: "event", sport_col_events: "sport"}
                )

                medals_for_merge = medals_with_continent.copy()
                if event_col_medals != "event":
                    medals_for_merge = medals_for_merge.rename(
                        columns={event_col_medals: "event"}
                    )

                medals_with_sport = medals_for_merge.merge(
                    events_for_merge,
                    on="event",
                    how="left",
                )

                sport_col = "sport" if "sport" in medals_with_sport.columns else "Sport"
                if sport_col in medals_with_sport.columns:
                    hierarchy_data = (
                        medals_with_sport.groupby(["Continent", country_col, sport_col])
                        .size()
                        .reset_index(name="Medal_Count")
                    )
                    hierarchy_data = hierarchy_data.rename(
                        columns={country_col: "Country", sport_col: "Sport"}
                    )
                else:
                    hierarchy_data = pd.DataFrame()

                if not hierarchy_data.empty:
                    fig_sunburst = px.sunburst(
                        hierarchy_data,
                        path=["Continent", "Country", "Sport"],
                        values="Medal_Count",
                        title="Medal Hierarchy by Continent",
                        color="Medal_Count",
                        color_continuous_scale="viridis",
                    )
                    st.plotly_chart(fig_sunburst, use_container_width=True)
                else:
                    st.info("No data available for sunburst chart.")
            else:
                st.info("Event data structure not compatible.")
        else:
            st.info("NOC column not found in medals data.")
    else:
        st.info("Required data files not available.")

with col2:
    st.subheader("Treemap Chart")
    st.markdown("Hierarchy: Continent → Country → Sport → Medal Count")

    if not data["medals"].empty and not data["events"].empty:
        medals_df = data["medals"].copy()
        events_df = data["events"].copy()

        country_col = (
            "country_code"
            if "country_code" in medals_df.columns
            else ("NOC" if "NOC" in medals_df.columns else "code")
        )
        if country_col in medals_df.columns:
            medals_with_continent = add_continent_to_data(medals_df, country_col)

            event_col_medals = "event" if "event" in medals_df.columns else "Event"
            event_col_events = "event" if "event" in events_df.columns else "Event"
            sport_col_events = "sport" if "sport" in events_df.columns else "Sport"

            if (
                event_col_medals in medals_df.columns
                and event_col_events in events_df.columns
            ):
                events_for_merge = events_df[
                    [event_col_events, sport_col_events]
                ].drop_duplicates()
                events_for_merge = events_for_merge.rename(
                    columns={event_col_events: "event", sport_col_events: "sport"}
                )

                medals_for_merge = medals_with_continent.copy()
                if event_col_medals != "event":
                    medals_for_merge = medals_for_merge.rename(
                        columns={event_col_medals: "event"}
                    )

                medals_with_sport = medals_for_merge.merge(
                    events_for_merge,
                    on="event",
                    how="left",
                )

                sport_col = "sport" if "sport" in medals_with_sport.columns else "Sport"
                if sport_col in medals_with_sport.columns:
                    hierarchy_data = (
                        medals_with_sport.groupby(["Continent", country_col, sport_col])
                        .size()
                        .reset_index(name="Medal_Count")
                    )
                    hierarchy_data = hierarchy_data.rename(
                        columns={country_col: "Country", sport_col: "Sport"}
                    )
                else:
                    hierarchy_data = pd.DataFrame()

                if not hierarchy_data.empty:
                    fig_treemap = px.treemap(
                        hierarchy_data,
                        path=[px.Constant("World"), "Continent", "Country", "Sport"],
                        values="Medal_Count",
                        title="Medal Hierarchy Treemap",
                        color="Medal_Count",
                        color_continuous_scale="viridis",
                    )
                    st.plotly_chart(fig_treemap, use_container_width=True)
                else:
                    st.info("No data available for treemap chart.")
            else:
                st.info("Event data structure not compatible.")
        else:
            st.info("Country code column not found in medals data.")
    else:
        st.info("Required data files not available.")

st.header("📊 Continent vs. Medals")
st.markdown("Grouped bar chart showing Gold, Silver, and Bronze medals by continent")

if not data["medals"].empty:
    medals_df = data["medals"].copy()
    country_col = (
        "country_code"
        if "country_code" in medals_df.columns
        else ("NOC" if "NOC" in medals_df.columns else "code")
    )
    medal_col = "medal_type" if "medal_type" in medals_df.columns else "Medal"

    if selected_sports and not data["events"].empty:
        events_df = data["events"].copy()
        event_col_medals = "event" if "event" in medals_df.columns else "Event"
        event_col_events = "event" if "event" in events_df.columns else "Event"
        sport_col_events = "sport" if "sport" in events_df.columns else "Sport"

        if (
            event_col_medals in medals_df.columns
            and event_col_events in events_df.columns
        ):
            events_for_merge = events_df[
                [event_col_events, sport_col_events]
            ].drop_duplicates()
            events_for_merge = events_for_merge.rename(
                columns={event_col_events: "event", sport_col_events: "sport"}
            )

            medals_for_merge = medals_df.copy()
            if event_col_medals != "event":
                medals_for_merge = medals_for_merge.rename(
                    columns={event_col_medals: "event"}
                )

            medals_with_sport = medals_for_merge.merge(
                events_for_merge, on="event", how="left"
            )

            sport_col = "sport" if "sport" in medals_with_sport.columns else "Sport"
            if sport_col in medals_with_sport.columns:
                medals_df = medals_with_sport[
                    medals_with_sport[sport_col].isin(selected_sports)
                ]
            else:
                medals_df = medals_with_sport

    if country_col in medals_df.columns:
        medals_with_continent = add_continent_to_data(medals_df, country_col)

        if selected_countries:
            medals_with_continent = medals_with_continent[
                medals_with_continent[country_col].isin(selected_countries)
            ]

        if selected_continents:
            medals_with_continent = medals_with_continent[
                medals_with_continent["Continent"].isin(selected_continents)
            ]

        if medal_types and medal_col in medals_with_continent.columns:
            medal_mapping = {
                "Gold": "Gold Medal",
                "Silver": "Silver Medal",
                "Bronze": "Bronze Medal",
            }
            medal_values = [medal_mapping.get(m, m) for m in medal_types]
            medals_with_continent = medals_with_continent[
                medals_with_continent[medal_col].isin(medal_values)
            ]

        if medal_col in medals_with_continent.columns:
            continent_medals = (
                medals_with_continent.groupby(["Continent", medal_col])
                .size()
                .reset_index(name="Count")
            )
            continent_medals = continent_medals.rename(columns={medal_col: "Medal"})
            continent_medals["Medal"] = continent_medals["Medal"].str.replace(
                " Medal", "", regex=False
            )
        else:
            continent_medals = pd.DataFrame()

        if not continent_medals.empty:
            fig_continent = px.bar(
                continent_medals,
                x="Continent",
                y="Count",
                color="Medal",
                title="Medal Distribution by Continent",
                labels={"Count": "Number of Medals", "Continent": "Continent"},
                color_discrete_map={
                    "Gold": "#FFD700",
                    "Silver": "#C0C0C0",
                    "Bronze": "#CD7F32",
                },
                barmode="group",
            )
            st.plotly_chart(fig_continent, use_container_width=True)
        else:
            st.info("No medal data available for continent analysis.")
    else:
        st.info("Country column not found in medals data.")
else:
    st.info("Medal data not available.")

st.header("🏆 Top 20 Countries vs. Medals")
st.markdown(
    "Grouped bar chart showing Gold, Silver, and Bronze medals for top 20 countries"
)

if not data["medals"].empty:
    medals_df = data["medals"].copy()

    country_col = (
        "country_code"
        if "country_code" in medals_df.columns
        else ("NOC" if "NOC" in medals_df.columns else "code")
    )
    medal_col = "medal_type" if "medal_type" in medals_df.columns else "Medal"

    if selected_sports and not data["events"].empty:
        events_df = data["events"].copy()
        event_col_medals = "event" if "event" in medals_df.columns else "Event"
        event_col_events = "event" if "event" in events_df.columns else "Event"
        sport_col_events = "sport" if "sport" in events_df.columns else "Sport"

        if (
            event_col_medals in medals_df.columns
            and event_col_events in events_df.columns
        ):
            events_for_merge = events_df[
                [event_col_events, sport_col_events]
            ].drop_duplicates()
            events_for_merge = events_for_merge.rename(
                columns={event_col_events: "event", sport_col_events: "sport"}
            )

            medals_for_merge = medals_df.copy()
            if event_col_medals != "event":
                medals_for_merge = medals_for_merge.rename(
                    columns={event_col_medals: "event"}
                )

            medals_with_sport = medals_for_merge.merge(
                events_for_merge, on="event", how="left"
            )

            sport_col = "sport" if "sport" in medals_with_sport.columns else "Sport"
            if sport_col in medals_with_sport.columns:
                medals_df = medals_with_sport[
                    medals_with_sport[sport_col].isin(selected_sports)
                ]
            else:
                medals_df = medals_with_sport

    if selected_countries:
        if country_col in medals_df.columns:
            medals_df = medals_df[medals_df[country_col].isin(selected_countries)]

    if medal_types and medal_col in medals_df.columns:
        medal_mapping = {
            "Gold": "Gold Medal",
            "Silver": "Silver Medal",
            "Bronze": "Bronze Medal",
        }
        medal_values = [medal_mapping.get(m, m) for m in medal_types]
        medals_df = medals_df[medals_df[medal_col].isin(medal_values)]

    if country_col in medals_df.columns:
        country_totals = (
            medals_df.groupby(country_col).size().sort_values(ascending=False).head(20)
        )
        top_countries = country_totals.index.tolist()

        medals_top20 = medals_df[medals_df[country_col].isin(top_countries)]

        if medal_col in medals_top20.columns:
            country_medals = (
                medals_top20.groupby([country_col, medal_col])
                .size()
                .reset_index(name="Count")
            )
            country_medals = country_medals.rename(
                columns={country_col: "Country", medal_col: "Medal"}
            )
            country_medals["Medal"] = country_medals["Medal"].str.replace(
                " Medal", "", regex=False
            )
        else:
            country_medals = pd.DataFrame()
    else:
        country_medals = pd.DataFrame()

    if not country_medals.empty:
        fig_country = px.bar(
            country_medals,
            x="Country",
            y="Count",
            color="Medal",
            title="Medal Distribution for Top 20 Countries",
            labels={"Count": "Number of Medals", "NOC": "Country"},
            color_discrete_map={
                "Gold": "#FFD700",
                "Silver": "#C0C0C0",
                "Bronze": "#CD7F32",
            },
            barmode="group",
        )
        fig_country.update_xaxes(tickangle=45)
        st.plotly_chart(fig_country, use_container_width=True)
    else:
        st.info("No medal data available for country analysis.")
else:
    st.info("Medal data not available.")
