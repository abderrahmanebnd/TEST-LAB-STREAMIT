"""
Athlete Performance Page - Paris 2024 Olympics Dashboard
The Human Story: Analysis from the perspective of athletes
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    load_data,
    filter_data,
    add_continent_to_data,
    merge_athlete_coach_data,
    get_country_flag_emoji,
)

st.set_page_config(
    page_title="Athlete Performance - Paris 2024 Olympics",
    page_icon="👤",
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

st.title("👤 Athlete Performance")
st.markdown(
    "Explore the human side of the Olympic Games - the athletes and their stories"
)

st.header("👥 Athlete Profile")

if not data["athletes"].empty:
    name_col = (
        "name"
        if "name" in data["athletes"].columns
        else ("Name" if "Name" in data["athletes"].columns else None)
    )

    if name_col:
        athlete_names = sorted(data["athletes"][name_col].dropna().unique().tolist())
    else:
        athlete_names = []

    selected_athlete_name = st.selectbox(
        "Search and Select an Athlete",
        options=[""] + athlete_names,
        format_func=lambda x: "Select an athlete..." if x == "" else x,
    )

    if selected_athlete_name and selected_athlete_name != "":
        athlete_data = data["athletes"][
            data["athletes"][name_col] == selected_athlete_name
        ]

        if not athlete_data.empty:
            athlete = athlete_data.iloc[0]

            col1, col2, col3 = st.columns([1, 2, 1])

            with col1:
                st.subheader("Profile")
                # Check for image in various possible column names
                image_col = None
                for col in [
                    "Image",
                    "image",
                    "Image_URL",
                    "image_url",
                    "photo",
                    "Photo",
                    "picture",
                    "Picture",
                ]:
                    if (
                        col in athlete.index
                        and pd.notna(athlete[col])
                        and str(athlete[col]).strip() != ""
                    ):
                        image_col = col
                        break

                if image_col:
                    try:
                        image_url = str(athlete[image_col]).strip()
                        if image_url.startswith("http"):
                            st.image(image_url, width=200)
                        else:
                            # Try as local path
                            st.image(image_url, width=200)
                    except Exception as e:
                        # Use default profile image
                        st.image("icons8-user-profile-100.png", width=200)
                else:
                    # Use default profile image
                    st.image("icons8-user-profile-100.png", width=200)

            with col2:
                st.subheader("Personal Information")

                name_col_athlete = (
                    "name"
                    if "name" in athlete.index
                    else ("Name" if "Name" in athlete.index else None)
                )
                if name_col_athlete:
                    st.markdown(f"**Full Name:** {athlete[name_col_athlete]}")

                country_col = None
                for col in ["country_code", "NOC", "code", "Code"]:
                    if col in athlete.index:
                        country_col = col
                        break

                if country_col:
                    country_name = athlete[country_col]
                    flag = get_country_flag_emoji(country_name)
                    st.markdown(f"**Country/NOC:** {flag} {country_name}")
                elif "country" in athlete.index:
                    country_name = athlete["country"]
                    flag = get_country_flag_emoji(country_name)
                    st.markdown(f"**Country/NOC:** {flag} {country_name}")

                height_weight_col1, height_weight_col2 = st.columns(2)
                with height_weight_col1:
                    height_col = (
                        "height"
                        if "height" in athlete.index
                        else ("Height" if "Height" in athlete.index else None)
                    )
                    if height_col and pd.notna(athlete[height_col]):
                        try:
                            height_value = float(athlete[height_col])
                            if height_value > 0:
                                st.metric("Height", f"{height_value} cm")
                            else:
                                st.metric("Height", "N/A")
                        except (ValueError, TypeError):
                            st.metric("Height", "N/A")
                    else:
                        st.metric("Height", "N/A")

                with height_weight_col2:
                    weight_col = (
                        "weight"
                        if "weight" in athlete.index
                        else ("Weight" if "Weight" in athlete.index else None)
                    )
                    if weight_col and pd.notna(athlete[weight_col]):
                        try:
                            weight_value = float(athlete[weight_col])
                            if weight_value > 0:
                                st.metric("Weight", f"{weight_value} kg")
                            else:
                                st.metric("Weight", "N/A")
                        except (ValueError, TypeError):
                            st.metric("Weight", "N/A")
                    else:
                        st.metric("Weight", "N/A")

                coach_col = (
                    "coach"
                    if "coach" in athlete.index
                    else ("Coach" if "Coach" in athlete.index else None)
                )
                if coach_col and pd.notna(athlete[coach_col]):
                    st.markdown(f"**Coach:** {athlete[coach_col]}")
                else:
                    st.markdown("**Coach:** Information not available")

                disciplines_col = (
                    "disciplines"
                    if "disciplines" in athlete.index
                    else ("Disciplines" if "Disciplines" in athlete.index else None)
                )
                if disciplines_col and pd.notna(athlete[disciplines_col]):
                    st.markdown(f"**Discipline(s):** {athlete[disciplines_col]}")
                elif "discipline" in athlete.index and pd.notna(athlete["discipline"]):
                    st.markdown(f"**Discipline:** {athlete['discipline']}")
                elif "Discipline" in athlete.index and pd.notna(athlete["Discipline"]):
                    st.markdown(f"**Discipline:** {athlete['Discipline']}")

            with col3:
                st.subheader("Additional Info")
                gender_col = (
                    "gender"
                    if "gender" in athlete.index
                    else ("Gender" if "Gender" in athlete.index else None)
                )
                if gender_col and pd.notna(athlete[gender_col]):
                    st.markdown(f"**Gender:** {athlete[gender_col]}")

                age = None
                if "birth_date" in athlete.index and pd.notna(athlete["birth_date"]):
                    try:
                        from datetime import datetime

                        birth_date = pd.to_datetime(athlete["birth_date"])
                        age = (datetime.now() - birth_date).days // 365
                        st.metric("Age", f"{age} years")
                    except:
                        pass
                elif "Age" in athlete.index and pd.notna(athlete["Age"]):
                    st.metric("Age", f"{int(athlete['Age'])} years")
        else:
            st.info("Athlete information not found.")
    else:
        st.info("Please select an athlete to view their profile.")
else:
    st.info("Athlete data not available.")

st.header("📊 Age Distribution Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Box Plot")
    st.markdown("Age distribution by sport or gender")

    has_age = "Age" in data["athletes"].columns or "age" in data["athletes"].columns
    has_birth_date = (
        "birth_date" in data["athletes"].columns
        or "Birth_Date" in data["athletes"].columns
    )

    if not data["athletes"].empty and (has_age or has_birth_date):
        athletes_df = data["athletes"].copy()

        if selected_countries:
            country_col = (
                "country_code"
                if "country_code" in athletes_df.columns
                else ("NOC" if "NOC" in athletes_df.columns else "code")
            )
            if country_col in athletes_df.columns:
                athletes_df = athletes_df[
                    athletes_df[country_col].isin(selected_countries)
                ]
        sport_col = (
            "Sport"
            if "Sport" in athletes_df.columns
            else ("sport" if "sport" in athletes_df.columns else None)
        )
        if selected_sports and sport_col and sport_col in athletes_df.columns:
            athletes_df = athletes_df[athletes_df[sport_col].isin(selected_sports)]

        if "Age" not in athletes_df.columns and "age" not in athletes_df.columns:
            if "birth_date" in athletes_df.columns:
                try:
                    from datetime import datetime

                    athletes_df["Age"] = (
                        datetime.now()
                        - pd.to_datetime(athletes_df["birth_date"], errors="coerce")
                    ).dt.days // 365
                except:
                    pass

        age_col = (
            "Age"
            if "Age" in athletes_df.columns
            else ("age" if "age" in athletes_df.columns else None)
        )
        if age_col:
            athletes_df = athletes_df[athletes_df[age_col].notna()]
        else:
            st.info("Age data not available.")
            age_col = None

        if not athletes_df.empty and age_col:
            group_options = []
            if "Sport" in athletes_df.columns or "sport" in athletes_df.columns:
                group_options.append("Sport")
            if "Gender" in athletes_df.columns or "gender" in athletes_df.columns:
                group_options.append("Gender")
            if "disciplines" in athletes_df.columns:
                group_options.append("Disciplines")

            if group_options:
                group_by = st.selectbox("Group by:", group_options, key="age_group")

                group_col = None
                if group_by == "Sport":
                    group_col = (
                        "sport"
                        if "sport" in athletes_df.columns
                        else ("Sport" if "Sport" in athletes_df.columns else None)
                    )
                elif group_by == "Gender":
                    group_col = (
                        "gender"
                        if "gender" in athletes_df.columns
                        else ("Gender" if "Gender" in athletes_df.columns else None)
                    )
                elif group_by == "Disciplines":
                    group_col = "disciplines"

                if group_col and group_col in athletes_df.columns:
                    fig_box = px.box(
                        athletes_df,
                        x=group_col,
                        y=age_col,
                        title=f"Age Distribution by {group_by}",
                        labels={age_col: "Age (years)", group_col: group_by},
                    )
                    fig_box.update_xaxes(tickangle=45)
                    st.plotly_chart(fig_box, use_container_width=True)
                else:
                    st.info(f"{group_by} column not found in data.")
            else:
                st.info("No grouping columns available.")
        else:
            st.info("No athlete data available after filtering.")
    else:
        st.info("Age data not available.")

with col2:
    st.subheader("Violin Plot")
    st.markdown("Age distribution with density")

    has_age = "Age" in data["athletes"].columns or "age" in data["athletes"].columns
    has_birth_date = (
        "birth_date" in data["athletes"].columns
        or "Birth_Date" in data["athletes"].columns
    )

    if not data["athletes"].empty and (has_age or has_birth_date):
        athletes_df = data["athletes"].copy()

        if selected_countries:
            country_col = (
                "country_code"
                if "country_code" in athletes_df.columns
                else ("NOC" if "NOC" in athletes_df.columns else "code")
            )
            if country_col in athletes_df.columns:
                athletes_df = athletes_df[
                    athletes_df[country_col].isin(selected_countries)
                ]
        sport_col = (
            "Sport"
            if "Sport" in athletes_df.columns
            else ("sport" if "sport" in athletes_df.columns else None)
        )
        if selected_sports and sport_col and sport_col in athletes_df.columns:
            athletes_df = athletes_df[athletes_df[sport_col].isin(selected_sports)]

        if "Age" not in athletes_df.columns and "age" not in athletes_df.columns:
            if "birth_date" in athletes_df.columns:
                try:
                    from datetime import datetime

                    athletes_df["Age"] = (
                        datetime.now()
                        - pd.to_datetime(athletes_df["birth_date"], errors="coerce")
                    ).dt.days // 365
                except:
                    pass

        age_col = (
            "Age"
            if "Age" in athletes_df.columns
            else ("age" if "age" in athletes_df.columns else None)
        )
        if age_col:
            athletes_df = athletes_df[athletes_df[age_col].notna()]
        else:
            st.info("Age data not available.")
            age_col = None

        if not athletes_df.empty and age_col:
            group_options = []
            if "Sport" in athletes_df.columns or "sport" in athletes_df.columns:
                group_options.append("Sport")
            if "Gender" in athletes_df.columns or "gender" in athletes_df.columns:
                group_options.append("Gender")
            if "disciplines" in athletes_df.columns:
                group_options.append("Disciplines")

            if group_options:
                group_by = st.selectbox("Group by:", group_options, key="violin_group")

                group_col = None
                if group_by == "Sport":
                    group_col = (
                        "sport"
                        if "sport" in athletes_df.columns
                        else ("Sport" if "Sport" in athletes_df.columns else None)
                    )
                elif group_by == "Gender":
                    group_col = (
                        "gender"
                        if "gender" in athletes_df.columns
                        else ("Gender" if "Gender" in athletes_df.columns else None)
                    )
                elif group_by == "Disciplines":
                    group_col = "disciplines"

                if group_col and group_col in athletes_df.columns:
                    fig_violin = px.violin(
                        athletes_df,
                        x=group_col,
                        y=age_col,
                        title=f"Age Distribution (Violin) by {group_by}",
                        labels={age_col: "Age (years)", group_col: group_by},
                        box=True,
                    )
                    fig_violin.update_xaxes(tickangle=45)
                    st.plotly_chart(fig_violin, use_container_width=True)
                else:
                    st.info(f"{group_by} column not found in data.")
            else:
                st.info("No grouping columns available.")
        else:
            st.info("No athlete data available after filtering.")
    else:
        st.info("Age data not available.")

st.header("⚖️ Gender Distribution")

gender_filter_type = st.selectbox(
    "View gender distribution for:",
    ["World", "Continent", "Country"],
    key="gender_filter",
)

has_gender = (
    "Gender" in data["athletes"].columns or "gender" in data["athletes"].columns
)

if not data["athletes"].empty and has_gender:
    athletes_df = data["athletes"].copy()

    if selected_countries:
        country_col = (
            "country_code"
            if "country_code" in athletes_df.columns
            else ("NOC" if "NOC" in athletes_df.columns else "code")
        )
        if country_col in athletes_df.columns:
            athletes_df = athletes_df[athletes_df[country_col].isin(selected_countries)]
    if selected_sports and "Sport" in athletes_df.columns:
        athletes_df = athletes_df[athletes_df["Sport"].isin(selected_sports)]

    gender_col = (
        "gender"
        if "gender" in athletes_df.columns
        else ("Gender" if "Gender" in athletes_df.columns else None)
    )

    if gender_col and gender_filter_type == "World":
        gender_counts = athletes_df[gender_col].value_counts()

        fig_pie = px.pie(
            values=gender_counts.values,
            names=gender_counts.index,
            title="Gender Distribution (World)",
            color_discrete_map={
                "M": "#3498db",
                "F": "#e91e63",
                "Male": "#3498db",
                "Female": "#e91e63",
            },
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    elif gender_filter_type == "Continent":
        country_col = (
            "country_code"
            if "country_code" in athletes_df.columns
            else ("NOC" if "NOC" in athletes_df.columns else "code")
        )
        athletes_with_continent = add_continent_to_data(athletes_df, country_col)

        if selected_continents:
            athletes_with_continent = athletes_with_continent[
                athletes_with_continent["Continent"].isin(selected_continents)
            ]

        gender_continent = (
            athletes_with_continent.groupby(["Continent", gender_col])
            .size()
            .reset_index(name="Count")
        )

        if not gender_continent.empty:
            fig_bar = px.bar(
                gender_continent,
                x="Continent",
                y="Count",
                color=gender_col,
                title="Gender Distribution by Continent",
                barmode="group",
                color_discrete_map={
                    "M": "#3498db",
                    "F": "#e91e63",
                    "Male": "#3498db",
                    "Female": "#e91e63",
                },
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No data available for continent gender distribution.")

    elif gender_filter_type == "Country":
        selected_country_gender = st.selectbox(
            "Select Country:", all_countries, key="gender_country"
        )

        if selected_country_gender:
            country_col = (
                "country_code"
                if "country_code" in athletes_df.columns
                else ("NOC" if "NOC" in athletes_df.columns else "code")
            )
            if country_col in athletes_df.columns:
                country_athletes = athletes_df[
                    athletes_df[country_col] == selected_country_gender
                ]
            else:
                country_athletes = pd.DataFrame()
            if not country_athletes.empty and gender_col:
                gender_counts = country_athletes[gender_col].value_counts()
            else:
                gender_counts = pd.Series(dtype=int)

            if not gender_counts.empty:
                fig_pie = px.pie(
                    values=gender_counts.values,
                    names=gender_counts.index,
                    title=f"Gender Distribution - {selected_country_gender}",
                    color_discrete_map={
                        "M": "#3498db",
                        "F": "#e91e63",
                        "Male": "#3498db",
                        "Female": "#e91e63",
                    },
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info(f"No data available for {selected_country_gender}.")
else:
    st.info("Gender data not available.")

st.header("🏆 Top Athletes by Medals")

if not data["medalists"].empty:
    medalists_df = data["medalists"].copy()

    if selected_countries:
        country_col = (
            "country_code"
            if "country_code" in medalists_df.columns
            else ("NOC" if "NOC" in medalists_df.columns else "code")
        )
        if country_col in medalists_df.columns:
            medalists_df = medalists_df[
                medalists_df[country_col].isin(selected_countries)
            ]

    if selected_sports and "Sport" in medalists_df.columns:
        medalists_df = medalists_df[medalists_df["Sport"].isin(selected_sports)]

    if medal_types and "Medal" in medalists_df.columns:
        medalists_df = medalists_df[medalists_df["Medal"].isin(medal_types)]

    name_col_medalists = (
        "name"
        if "name" in medalists_df.columns
        else ("Name" if "Name" in medalists_df.columns else None)
    )

    if name_col_medalists:
        athlete_medals = (
            medalists_df.groupby(name_col_medalists)
            .size()
            .sort_values(ascending=False)
            .head(10)
            .reset_index(name="Medal_Count")
        )

        if not athlete_medals.empty:
            fig_bar = px.bar(
                athlete_medals,
                x="Medal_Count",
                y=name_col_medalists,
                orientation="h",
                title="Top 10 Athletes by Total Medal Count",
                labels={
                    "Medal_Count": "Number of Medals",
                    name_col_medalists: "Athlete",
                },
                color="Medal_Count",
                color_continuous_scale="viridis",
            )
            fig_bar.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No medalist data available after filtering.")
    else:
        st.info("Name column not found in medalists data.")
else:
    st.info("Medalist data not available.")
