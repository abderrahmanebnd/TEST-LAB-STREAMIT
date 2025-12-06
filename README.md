# 🏅 Paris 2024 Olympic Games Streamlit Dashboard

A comprehensive, interactive multi-page dashboard for exploring and analyzing data from the Paris 2024 Olympic Games. Built as part of the LA28 Volunteer Selection Challenge for Software Engineering for Data Science.

## 📋 Overview

This Streamlit application provides a powerful interface to explore Olympic data through multiple analytical perspectives:

- **Overview Page**: High-level KPIs and summary statistics
- **Global Analysis**: Geographical and hierarchical visualizations
- **Athlete Performance**: Individual athlete profiles and demographic analysis
- **Sports and Events**: Competition schedules and venue information

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone this repository:
```bash
git clone https://github.com/abderrahmanebnd/paris-2024-olympics-streamlit.git
cd paris-2024-olympics-streamlit
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Download the dataset from [Kaggle](https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games) and place the CSV files in the `data/` directory.

4. Run the Streamlit application:
```bash
streamlit run 1_Overview.py
```

The application will open in your default web browser at `http://localhost:8501`

## 🎨 Design Choices & Creative Features

### Paris 2024 Branding

The dashboard features the official Paris 2024 Olympics brand colors:
- **Primary Pink (#E91E63)**: Used for headers, metrics, and primary UI elements
- **Purple/Lavender (#6A1B9A)**: Used for subheaders and secondary elements
- **Blue (#1976D2)**: Used for tertiary elements and accents
- **Green (#4CAF50)**: Used for success indicators

### Design Choices

1. **Dynamic Column Detection**: The application automatically detects column names (handles both uppercase and lowercase variations like `NOC`/`code`, `Sport`/`sport`, `Medal`/`medal_type`) to work with different data formats.

2. **Continent Mapping**: Implemented a comprehensive 3-letter NOC code to continent mapping system, allowing for geographical analysis across all visualizations.

3. **Modular Architecture**: Separated utility functions into `utils.py` and styling into `utils_style.py` for code reusability and maintainability across all pages.

4. **Responsive Filtering**: All filters are reactive and update visualizations in real-time, providing an interactive user experience.

5. **Error Handling**: Graceful handling of missing data, empty datasets, and column mismatches with informative user messages.

6. **Paris 2024 Theme**: Custom Streamlit theme configuration with brand colors applied consistently across all pages.

### Creative Features Beyond Requirements

1. **Continent Filter**: Added a continent filter (creative requirement) that works across all pages, enabling geographical analysis.

2. **Interactive Venue Map with Selector**: 
   - Added coordinates for all 35 Olympic venues
   - Created an interactive venue selector table
   - Map updates dynamically when a venue is selected
   - Shows venue information and sports hosted

3. **Age Calculation**: Automatically calculates athlete age from `birth_date` when `Age` column is not available.

4. **Athlete Profile Card**: Comprehensive athlete profile with image placeholder, coach information, and detailed stats.

5. **Enhanced Visualizations**:
   - Color-coded markers on venue map
   - Hierarchical sunburst and treemap charts
   - Interactive hover tooltips on all charts

6. **Smart Data Merging**: Automatically merges medals with events data to get sport information when needed.

## 📁 Project Structure

```
paris-2024-olympics-streamlit/
│
├── 1_Overview.py              # Main entry point
├── pages/                     # Multi-page application pages
│   ├── 2_Global_Analysis.py
│   ├── 3_Athlete_Performance.py
│   └── 4_Sports_and_Events.py
├── utils.py                   # Utility functions
├── utils_style.py             # Paris 2024 brand styling
├── requirements.txt            # Python dependencies
├── README.md                  # This file
├── .streamlit/                # Streamlit configuration
│   ├── config.toml           # Theme configuration
│   └── style.css             # Custom CSS styling
├── .gitignore                # Git ignore rules
├── data/                      # Dataset directory (place CSV files here)
│   ├── athletes.csv
│   ├── coaches.csv
│   ├── events.csv
│   ├── medals.csv
│   ├── medals_total.csv
│   ├── medallists.csv
│   ├── nocs.csv
│   ├── schedules.csv
│   ├── schedules_preliminary.csv
│   ├── teams.csv
│   ├── venues.csv
│   └── results/              # Detailed results by sport
└── SEDS_Streamlit_Challenging_Test.ipynb  # Documentation notebook (optional)
```

## 🎯 Features

### Global Filters (Available on All Pages)
- **Country Filter**: Multiselect for NOC codes
- **Sport Filter**: Multiselect for sports
- **Continent Filter**: Multiselect for continents (creative feature)
- **Medal Type Filter**: Checkboxes for Gold, Silver, Bronze (Paris 2024 branded)

### Page 1: Overview
- **5 Key Performance Indicators**: Total Athletes, Countries, Sports, Medals, Events
- **Global Medal Distribution**: Interactive donut chart
- **Top 10 Medal Standings**: Horizontal bar chart

### Page 2: Global Analysis
- **World Medal Map**: Choropleth map showing medal distribution
- **Medal Hierarchy**: Sunburst and Treemap charts (Continent → Country → Sport)
- **Continent vs. Medals**: Grouped bar chart
- **Top 20 Countries vs. Medals**: Grouped bar chart

### Page 3: Athlete Performance
- **Athlete Profile Card**: Detailed information with search functionality
- **Age Distribution**: Box and Violin plots by sport/gender
- **Gender Distribution**: Interactive charts by world/continent/country
- **Top Athletes by Medals**: Bar chart of top 10 medal winners

### Page 4: Sports and Events
- **Event Schedule**: Gantt/Timeline chart for sports or venues
- **Medal Count by Sport**: Treemap visualization
- **Venue Map**: Scatter mapbox showing Olympic venues in Paris
- **Sport Statistics**: Additional insights and rankings

## 🎨 Design Choices

### Technical Implementation
- **Multi-page Architecture**: Uses Streamlit's native multi-page feature for better organization
- **Caching**: `@st.cache_data` decorator for efficient data loading
- **Modular Code**: Utility functions in `utils.py` for reusability
- **Error Handling**: Graceful handling of missing data or columns

### User Experience
- **Consistent Layout**: Wide layout with columns for better space utilization
- **Interactive Visualizations**: All charts are interactive Plotly visualizations
- **Responsive Filters**: Sidebar filters update all visualizations dynamically
- **Clear Navigation**: Intuitive page structure with emoji icons

### Data Processing
- **Continent Mapping**: Custom mapping function for geographical analysis
- **Data Merging**: Intelligent merging of related datasets (athletes, coaches, events)
- **Filtering Logic**: Centralized filtering function for consistency

## 🌟 Creative Features

1. **Continent Filter**: Added continent-level filtering as a creative enhancement
2. **Athlete Profile Cards**: Comprehensive athlete information display with image placeholders
3. **Multiple Visualization Types**: Box plots, violin plots, sunburst, treemap, choropleth, timeline
4. **Dynamic Grouping**: Age distribution can be grouped by sport or gender
5. **Flexible Gender Analysis**: View gender distribution at world, continent, or country level

## 📊 Data Sources

All data is sourced from the [Paris 2024 Olympic Games Dataset](https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games) on Kaggle.


## 👥 Team

Developed as part of the Software Engineering for Data Science course evaluation by Abderrahmane Bendaia

## 📄 License

This project is created for educational purposes as part of the LA28 Volunteer Selection Challenge.

## 🌐 Deployed Dashboard

**Live Application**: [https://paris-2024-olympics.streamlit.app](https://paris-2024-olympics.streamlit.app)


- **Dataset**: [Kaggle - Paris 2024 Olympic Games](https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games)
- **Streamlit Documentation**: [https://docs.streamlit.io/](https://docs.streamlit.io/)
- **Plotly Documentation**: [https://plotly.com/python/](https://plotly.com/python/)


