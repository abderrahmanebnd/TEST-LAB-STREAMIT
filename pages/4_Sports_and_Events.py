"""
Sports and Events Page - Paris 2024 Olympics Dashboard
The Competition Arena: Analysis from the perspective of sports and events
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data, filter_data, add_continent_to_data, get_country_column

st.set_page_config(
    page_title="Sports and Events - Paris 2024 Olympics",
    page_icon="🏟️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Paris 2024 brand styling
from utils_style import inject_paris_2024_style

inject_paris_2024_style()


@st.cache_data
def load_all_data():
    return load_data()


data = load_data()

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

st.title("🏟️ Sports and Events")
st.markdown(
    "Explore the competition arena - schedules, venues, and sport-specific insights"
)

st.header("📅 Event Schedule")
st.markdown("Timeline view of events for selected sport or venue")

if not data["schedule"].empty:
    schedule_df = data["schedule"].copy()

    schedule_filter_type = st.selectbox(
        "Filter schedule by:", ["Sport", "Venue"], key="schedule_filter"
    )

    if schedule_filter_type == "Sport":
        sport_col = (
            "discipline"
            if "discipline" in schedule_df.columns
            else ("Sport" if "Sport" in schedule_df.columns else "sport")
        )

        if selected_sports and sport_col in schedule_df.columns:
            schedule_df = schedule_df[schedule_df[sport_col].isin(selected_sports)]
        else:
            pass

        available_sports = (
            sorted(schedule_df[sport_col].unique().tolist())
            if sport_col in schedule_df.columns
            else []
        )
        selected_sport_schedule = st.selectbox(
            "Select Sport:", available_sports, key="sport_schedule"
        )

        if selected_sport_schedule:
            schedule_filtered = schedule_df[
                schedule_df[sport_col] == selected_sport_schedule
            ]

            start_col = (
                "start_date"
                if "start_date" in schedule_filtered.columns
                else ("Start" if "Start" in schedule_filtered.columns else "start")
            )
            end_col = (
                "end_date"
                if "end_date" in schedule_filtered.columns
                else ("End" if "End" in schedule_filtered.columns else "end")
            )
            event_col = "event" if "event" in schedule_filtered.columns else "Event"

            if (
                start_col in schedule_filtered.columns
                and event_col in schedule_filtered.columns
            ):
                try:
                    schedule_filtered[start_col] = pd.to_datetime(
                        schedule_filtered[start_col]
                    )
                    schedule_filtered[end_col] = (
                        pd.to_datetime(schedule_filtered[end_col])
                        if end_col in schedule_filtered.columns
                        else schedule_filtered[start_col]
                    )

                    fig_timeline = px.timeline(
                        schedule_filtered,
                        x_start=start_col,
                        x_end=end_col,
                        y=event_col,
                        title=f"Event Schedule - {selected_sport_schedule}",
                        labels={
                            event_col: "Event Name",
                            start_col: "Start Time",
                            end_col: "End Time",
                        },
                    )
                    fig_timeline.update_yaxes(autorange="reversed")
                    st.plotly_chart(fig_timeline, use_container_width=True)
                except Exception as e:
                    st.info(f"Date conversion issue. Showing event list instead.")
                    display_cols = [event_col, start_col]
                    if end_col in schedule_filtered.columns:
                        display_cols.append(end_col)
                    st.dataframe(schedule_filtered[display_cols].head(20))
            else:
                st.info("Required columns (Start, Event) not found in schedule data.")
        else:
            st.info("Please select a sport to view its schedule.")

    elif schedule_filter_type == "Venue":
        venue_col = "venue" if "venue" in schedule_df.columns else "Venue"
        if venue_col in schedule_df.columns:
            available_venues = sorted(schedule_df[venue_col].unique().tolist())
            selected_venue = st.selectbox(
                "Select Venue:", available_venues, key="venue_schedule"
            )

            if selected_venue:
                schedule_filtered = schedule_df[
                    schedule_df[venue_col] == selected_venue
                ]

                start_col = (
                    "start_date"
                    if "start_date" in schedule_filtered.columns
                    else ("Start" if "Start" in schedule_filtered.columns else "start")
                )
                end_col = (
                    "end_date"
                    if "end_date" in schedule_filtered.columns
                    else ("End" if "End" in schedule_filtered.columns else "end")
                )
                event_col = "event" if "event" in schedule_filtered.columns else "Event"

                if (
                    start_col in schedule_filtered.columns
                    and event_col in schedule_filtered.columns
                ):
                    try:
                        schedule_filtered[start_col] = pd.to_datetime(
                            schedule_filtered[start_col]
                        )
                        schedule_filtered[end_col] = (
                            pd.to_datetime(schedule_filtered[end_col])
                            if end_col in schedule_filtered.columns
                            else schedule_filtered[start_col]
                        )

                        fig_timeline = px.timeline(
                            schedule_filtered,
                            x_start=start_col,
                            x_end=end_col,
                            y=event_col,
                            title=f"Event Schedule - {selected_venue}",
                            labels={event_col: "Event Name"},
                        )
                        fig_timeline.update_yaxes(autorange="reversed")
                        st.plotly_chart(fig_timeline, use_container_width=True)
                    except Exception as e:
                        st.info(f"Date conversion issue. Showing event list instead.")
                        display_cols = [event_col, start_col]
                        if end_col in schedule_filtered.columns:
                            display_cols.append(end_col)
                        st.dataframe(schedule_filtered[display_cols].head(20))
                else:
                    st.info("Required columns not found.")
            else:
                st.info("Please select a venue to view its schedule.")
        else:
            st.info("Venue column not found in schedule data.")
else:
    st.info("Schedule data not available.")

st.header("🏅 Medal Count by Sport")
st.markdown("Treemap visualization showing medal distribution across sports")

if not data["medals"].empty and not data["events"].empty:
    medals_df = data["medals"].copy()
    events_df = data["events"].copy()

    medal_col = "medal_type" if "medal_type" in medals_df.columns else "Medal"
    if medal_types and medal_col in medals_df.columns:
        medal_mapping = {
            "Gold": "Gold Medal",
            "Silver": "Silver Medal",
            "Bronze": "Bronze Medal",
        }
        medal_values = [medal_mapping.get(m, m) for m in medal_types]
        medals_df = medals_df[medals_df[medal_col].isin(medal_values)]

    event_col_medals = "event" if "event" in medals_df.columns else "Event"
    event_col_events = "event" if "event" in events_df.columns else "Event"
    sport_col_events = "sport" if "sport" in events_df.columns else "Sport"

    if event_col_medals in medals_df.columns and event_col_events in events_df.columns:
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

        if selected_sports:
            sport_col = "sport" if "sport" in medals_with_sport.columns else "Sport"
            if sport_col in medals_with_sport.columns:
                medals_with_sport = medals_with_sport[
                    medals_with_sport[sport_col].isin(selected_sports)
                ]

        sport_col = "sport" if "sport" in medals_with_sport.columns else "Sport"
        if sport_col in medals_with_sport.columns:
            sport_medals = (
                medals_with_sport.groupby(sport_col)
                .size()
                .reset_index(name="Medal_Count")
            )
            sport_medals = sport_medals.rename(columns={sport_col: "Sport"})
        else:
            sport_medals = pd.DataFrame()

        if not sport_medals.empty:
            fig_treemap = px.treemap(
                sport_medals,
                path=[px.Constant("All Sports"), "Sport"],
                values="Medal_Count",
                title="Medal Count by Sport",
                color="Medal_Count",
                color_continuous_scale="viridis",
            )
            st.plotly_chart(fig_treemap, use_container_width=True)
        else:
            st.info("No medal data available after filtering.")
    else:
        sport_col = (
            "sport"
            if "sport" in medals_df.columns
            else ("Sport" if "Sport" in medals_df.columns else None)
        )
        if sport_col:
            sport_medals = (
                medals_df.groupby(sport_col).size().reset_index(name="Medal_Count")
            )
            sport_medals = sport_medals.rename(columns={sport_col: "Sport"})

            if not sport_medals.empty:
                fig_treemap = px.treemap(
                    sport_medals,
                    path=[px.Constant("All Sports"), "Sport"],
                    values="Medal_Count",
                    title="Medal Count by Sport",
                    color="Medal_Count",
                    color_continuous_scale="viridis",
                )
                st.plotly_chart(fig_treemap, use_container_width=True)
            else:
                st.info("No medal data available.")
        else:
            st.info("Sport information not available in medals data.")
else:
    st.info("Required data files (medals, events) not available.")

st.header("🗺️ Olympic Venues Map")
st.markdown("Interactive map showing locations of Olympic venues in Paris")

if not data["venues"].empty:
    venues_df = data["venues"].copy()

    VENUE_COORDINATES = {
        "Aquatics Centre": (48.8361, 2.3772),
        "Bercy Arena": (48.8386, 2.3775),
        "Bordeaux Stadium": (44.8964, -0.5636),
        "Champ de Mars Arena": (48.8566, 2.2992),
        "Château de Versailles": (48.8049, 2.1204),
        "Chateauroux Shooting Centre": (46.8120, 1.6900),
        "Eiffel Tower Stadium": (48.8584, 2.2945),
        "Elancourt Hill": (48.7800, 1.9600),
        "Geoffroy-Guichard Stadium": (45.4600, 4.3900),
        "Grand Palais": (48.8660, 2.3122),
        "Hôtel de Ville": (48.8566, 2.3522),
        "Invalides": (48.8566, 2.3129),
        "La Beaujoire Stadium": (47.2556, -1.5253),
        "La Concorde": (48.8656, 2.3212),
        "Le Bourget Sport Climbing Venue": (48.9444, 2.4361),
        "Golf National": (48.7500, 2.1000),
        "Lyon Stadium": (45.7650, 4.9800),
        "Marseille Marina": (43.2965, 5.3698),
        "Marseille Stadium": (43.2697, 5.3959),
        "Nice Stadium": (43.7102, 7.2620),
        "North Paris Arena": (48.9000, 2.3500),
        "Parc des Princes": (48.8414, 2.2530),
        "Paris La Defense Arena": (48.8925, 2.2383),
        "Pierre Mauroy Stadium": (50.6114, 3.1303),
        "Pont Alexandre III": (48.8636, 2.3133),
        "Porte de La Chapelle Arena": (48.8964, 2.3611),
        "Stade Roland-Garros": (48.8470, 2.2470),
        "Saint-Quentin-en-Yvelines BMX Stadium": (48.7800, 2.0400),
        "Saint-Quentin-en-Yvelines Velodrome": (48.7800, 2.0400),
        "South Paris Arena": (48.8300, 2.3600),
        "Stade de France": (48.9244, 2.3600),
        "Teahupo'o, Tahiti": (-17.8419, -149.2669),
        "Trocadéro": (48.8625, 2.2872),
        "Vaires-sur-Marne Nautical Stadium": (48.8731, 2.6250),
        "Yves-du-Manoir Stadium": (48.8361, 2.3772),
    }

    if "latitude" not in venues_df.columns and "longitude" not in venues_df.columns:
        venue_col = "venue" if "venue" in venues_df.columns else "Venue"
        if venue_col in venues_df.columns:
            venues_df["latitude"] = venues_df[venue_col].apply(
                lambda x: (
                    VENUE_COORDINATES.get(x, (None, None))[0]
                    if x in VENUE_COORDINATES
                    else None
                )
            )
            venues_df["longitude"] = venues_df[venue_col].apply(
                lambda x: (
                    VENUE_COORDINATES.get(x, (None, None))[1]
                    if x in VENUE_COORDINATES
                    else None
                )
            )

    lat_col = None
    lon_col = None

    for col in venues_df.columns:
        col_lower = col.lower()
        if "lat" in col_lower:
            lat_col = col
        if "lon" in col_lower or "lng" in col_lower or "long" in col_lower:
            lon_col = col

    if lat_col and lon_col:
        venues_with_coords = venues_df[
            venues_df[lat_col].notna() & venues_df[lon_col].notna()
        ]

        if not venues_with_coords.empty:
            venue_name_col = (
                "venue"
                if "venue" in venues_with_coords.columns
                else (
                    "Venue"
                    if "Venue" in venues_with_coords.columns
                    else venues_with_coords.columns[0]
                )
            )

            col_table, col_map = st.columns([1, 2])

            with col_table:
                st.subheader("📍 Select a Venue")
                st.markdown("Choose a venue to view its location on the map")

                venue_list = ["All Venues"] + sorted(
                    venues_with_coords[venue_name_col].unique().tolist()
                )

                selected_venue = st.selectbox(
                    "Choose a venue:", options=venue_list, key="venue_selector", index=0
                )

                st.subheader("📋 All Venues")
                display_cols = [venue_name_col]
                if "sports" in venues_with_coords.columns:
                    display_cols.append("sports")
                if "date_start" in venues_with_coords.columns:
                    display_cols.append("date_start")
                if "date_end" in venues_with_coords.columns:
                    display_cols.append("date_end")

                display_df = venues_with_coords[display_cols].copy()
                if "sports" in display_df.columns:
                    display_df["sports"] = display_df["sports"].apply(
                        lambda x: str(x)[:50] + "..." if len(str(x)) > 50 else str(x)
                    )

                st.dataframe(
                    display_df, use_container_width=True, height=400, hide_index=True
                )

            with col_map:
                if selected_venue and selected_venue != "All Venues":
                    map_venues = venues_with_coords[
                        venues_with_coords[venue_name_col] == selected_venue
                    ].copy()
                    center_lat = map_venues[lat_col].iloc[0]
                    center_lon = map_venues[lon_col].iloc[0]
                    zoom_level = 13
                    title_suffix = f" - {selected_venue}"
                    map_venues["color"] = "#FF0000"
                    map_venues["size"] = 15
                else:
                    map_venues = venues_with_coords.copy()
                    center_lat = map_venues[lat_col].mean()
                    center_lon = map_venues[lon_col].mean()
                    zoom_level = 9
                    title_suffix = " - All Venues"
                    map_venues["color"] = "#FF6B6B"
                    map_venues["size"] = 10

                fig_map = px.scatter_mapbox(
                    map_venues,
                    lat=lat_col,
                    lon=lon_col,
                    hover_name=venue_name_col,
                    hover_data=(
                        [venue_name_col, "sports"]
                        if "sports" in map_venues.columns
                        else [venue_name_col]
                    ),
                    zoom=zoom_level,
                    height=600,
                    title=f"Interactive Map: Olympic Venues{title_suffix}",
                    color="color",
                    size="size",
                    color_discrete_map={"#FF0000": "#FF0000", "#FF6B6B": "#FF6B6B"},
                    size_max=15,
                )

                fig_map.update_layout(
                    mapbox=dict(
                        style="open-street-map",
                        center=dict(lat=center_lat, lon=center_lon),
                        zoom=zoom_level,
                    ),
                    margin={"r": 0, "t": 50, "l": 0, "b": 0},
                    height=600,
                    showlegend=False,
                )

                fig_map.update_traces(
                    marker=dict(
                        size=map_venues["size"].tolist(),
                        opacity=0.8,
                    ),
                    hovertemplate="<b>%{hovertext}</b><br>"
                    + "Lat: %{lat:.4f}<br>"
                    + "Lon: %{lon:.4f}<extra></extra>",
                )
                st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info("No venues with valid coordinates found.")
            st.dataframe(venues_df.head(20))
    else:
        st.info(
            """
        **Note:** Latitude and longitude data not found in venues file. 
        For a complete implementation, you would need to:
        1. Add coordinates to the venues.csv file, or
        2. Use a geocoding service to convert venue addresses to coordinates
        """
        )
        st.subheader("Available Venues")
        st.dataframe(venues_df.head(20))
else:
    st.info("Venue data not available.")

st.header("📊 Sport Statistics")

col1, col2 = st.columns(2)

with col1:
    if not data["events"].empty:
        sport_col = (
            "sport"
            if "sport" in data["events"].columns
            else ("Sport" if "Sport" in data["events"].columns else None)
        )
        if sport_col:
            events_by_sport = (
                data["events"]
                .groupby(sport_col)
                .size()
                .sort_values(ascending=False)
                .head(10)
            )
            events_by_sport.index.name = "Sport"

            events_df_plot = events_by_sport.reset_index()
            events_df_plot.columns = ["Sport", "Event_Count"]

            fig_bar = px.bar(
                events_df_plot,
                x="Event_Count",
                y="Sport",
                orientation="h",
                title="Top 10 Sports by Number of Events",
                labels={"Event_Count": "Number of Events", "Sport": "Sport"},
            )
            fig_bar.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    if not data["medals"].empty and not data["events"].empty:
        medals_df = data["medals"].copy()
        events_df = data["events"].copy()

        if selected_countries:
            country_col = get_country_column(medals_df)
            if country_col in medals_df.columns:
                medals_df = medals_df[medals_df[country_col].isin(selected_countries)]

        medal_col = (
            "medal_type"
            if "medal_type" in medals_df.columns
            else ("Medal" if "Medal" in medals_df.columns else None)
        )
        if medal_col and medal_col in medals_df.columns and medal_types:
            medal_mapping = {
                "Gold": "Gold Medal",
                "Silver": "Silver Medal",
                "Bronze": "Bronze Medal",
            }
            medal_values = [medal_mapping.get(m, m) for m in medal_types]
            medals_df = medals_df[medals_df[medal_col].isin(medal_values)]

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

            if selected_sports:
                sport_col = "sport" if "sport" in medals_with_sport.columns else "Sport"
                if sport_col in medals_with_sport.columns:
                    medals_with_sport = medals_with_sport[
                        medals_with_sport[sport_col].isin(selected_sports)
                    ]

            sport_col = "sport" if "sport" in medals_with_sport.columns else "Sport"
            if sport_col in medals_with_sport.columns:
                medals_by_sport = (
                    medals_with_sport.groupby(sport_col)
                    .size()
                    .sort_values(ascending=False)
                    .head(10)
                )
                medals_by_sport.index.name = "Sport"
            else:
                medals_by_sport = pd.Series(dtype=int)
        else:
            sport_col = (
                "sport"
                if "sport" in medals_df.columns
                else ("Sport" if "Sport" in medals_df.columns else None)
            )
            if sport_col:
                medals_by_sport = (
                    medals_df.groupby(sport_col)
                    .size()
                    .sort_values(ascending=False)
                    .head(10)
                )
                medals_by_sport.index.name = "Sport"
            else:
                medals_by_sport = pd.Series(dtype=int)

        if not medals_by_sport.empty:
            medals_df_plot = medals_by_sport.reset_index()
            medals_df_plot.columns = ["Sport", "Medal_Count"]

            fig_bar = px.bar(
                medals_df_plot,
                x="Medal_Count",
                y="Sport",
                orientation="h",
                title="Top 10 Sports by Number of Medals",
                labels={"Medal_Count": "Number of Medals", "Sport": "Sport"},
                color="Medal_Count",
                color_continuous_scale="viridis",
            )
            fig_bar.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No medal data available for sport statistics.")
    elif not data["medals"].empty:
        st.info("Events data not available to merge with medals.")
    else:
        st.info("Medal data not available.")
