"""
Utility functions for the Paris 2024 Olympics Streamlit Dashboard
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import pycountry

# Continent mapping for countries
CONTINENT_MAPPING = {
    'AF': 'Africa', 'AL': 'Europe', 'DZ': 'Africa', 'AR': 'South America', 'AU': 'Oceania',
    'AT': 'Europe', 'AZ': 'Asia', 'BS': 'North America', 'BD': 'Asia', 'BE': 'Europe',
    'BZ': 'North America', 'BJ': 'Africa', 'BT': 'Asia', 'BO': 'South America', 'BA': 'Europe',
    'BW': 'Africa', 'BR': 'South America', 'BG': 'Europe', 'BF': 'Africa', 'BI': 'Africa',
    'KH': 'Asia', 'CM': 'Africa', 'CA': 'North America', 'CV': 'Africa', 'CF': 'Africa',
    'TD': 'Africa', 'CL': 'South America', 'CN': 'Asia', 'CO': 'South America', 'KM': 'Africa',
    'CG': 'Africa', 'CD': 'Africa', 'CR': 'North America', 'HR': 'Europe', 'CU': 'North America',
    'CY': 'Asia', 'CZ': 'Europe', 'DK': 'Europe', 'DJ': 'Africa', 'DM': 'North America',
    'DO': 'North America', 'EC': 'South America', 'EG': 'Africa', 'SV': 'North America',
    'GQ': 'Africa', 'ER': 'Africa', 'EE': 'Europe', 'SZ': 'Africa', 'ET': 'Africa',
    'FJ': 'Oceania', 'FI': 'Europe', 'FR': 'Europe', 'GA': 'Africa', 'GM': 'Africa',
    'GE': 'Asia', 'DE': 'Europe', 'GH': 'Africa', 'GR': 'Europe', 'GD': 'North America',
    'GT': 'North America', 'GN': 'Africa', 'GW': 'Africa', 'GY': 'South America',
    'HT': 'North America', 'HN': 'North America', 'HU': 'Europe', 'IS': 'Europe',
    'IN': 'Asia', 'ID': 'Asia', 'IR': 'Asia', 'IQ': 'Asia', 'IE': 'Europe',
    'IL': 'Asia', 'IT': 'Europe', 'CI': 'Africa', 'JM': 'North America', 'JP': 'Asia',
    'JO': 'Asia', 'KZ': 'Asia', 'KE': 'Africa', 'KI': 'Oceania', 'KW': 'Asia',
    'KG': 'Asia', 'LA': 'Asia', 'LV': 'Europe', 'LB': 'Asia', 'LS': 'Africa',
    'LR': 'Africa', 'LY': 'Africa', 'LI': 'Europe', 'LT': 'Europe', 'LU': 'Europe',
    'MG': 'Africa', 'MW': 'Africa', 'MY': 'Asia', 'MV': 'Asia', 'ML': 'Africa',
    'MT': 'Europe', 'MH': 'Oceania', 'MR': 'Africa', 'MU': 'Africa', 'MX': 'North America',
    'FM': 'Oceania', 'MD': 'Europe', 'MC': 'Europe', 'MN': 'Asia', 'ME': 'Europe',
    'MA': 'Africa', 'MZ': 'Africa', 'MM': 'Asia', 'NA': 'Africa', 'NR': 'Oceania',
    'NP': 'Asia', 'NL': 'Europe', 'NZ': 'Oceania', 'NI': 'North America', 'NE': 'Africa',
    'NG': 'Africa', 'KP': 'Asia', 'MK': 'Europe', 'NO': 'Europe', 'OM': 'Asia',
    'PK': 'Asia', 'PW': 'Oceania', 'PA': 'North America', 'PG': 'Oceania', 'PY': 'South America',
    'PE': 'South America', 'PH': 'Asia', 'PL': 'Europe', 'PT': 'Europe', 'QA': 'Asia',
    'RO': 'Europe', 'RU': 'Europe', 'RW': 'Africa', 'KN': 'North America', 'LC': 'North America',
    'VC': 'North America', 'WS': 'Oceania', 'SM': 'Europe', 'ST': 'Africa', 'SA': 'Asia',
    'SN': 'Africa', 'RS': 'Europe', 'SC': 'Africa', 'SL': 'Africa', 'SG': 'Asia',
    'SK': 'Europe', 'SI': 'Europe', 'SB': 'Oceania', 'SO': 'Africa', 'ZA': 'Africa',
    'KR': 'Asia', 'SS': 'Africa', 'ES': 'Europe', 'LK': 'Asia', 'SD': 'Africa',
    'SR': 'South America', 'SE': 'Europe', 'CH': 'Europe', 'SY': 'Asia', 'TW': 'Asia',
    'TJ': 'Asia', 'TZ': 'Africa', 'TH': 'Asia', 'TL': 'Asia', 'TG': 'Africa',
    'TO': 'Oceania', 'TT': 'North America', 'TN': 'Africa', 'TR': 'Asia', 'TM': 'Asia',
    'TV': 'Oceania', 'UG': 'Africa', 'UA': 'Europe', 'AE': 'Asia', 'GB': 'Europe',
    'US': 'North America', 'UY': 'South America', 'UZ': 'Asia', 'VU': 'Oceania',
    'VE': 'South America', 'VN': 'Asia', 'YE': 'Asia', 'ZM': 'Africa', 'ZW': 'Africa'
}

def get_continent_from_noc(noc_code: str) -> str:
    """Get continent from NOC code (handles both 2-letter and 3-letter codes)"""
    if not noc_code or pd.isna(noc_code):
        return 'Unknown'
    
    noc_code = str(noc_code).upper().strip()
    
    # Mapping for 3-letter NOC codes (Olympic codes) to continents
    NOC_TO_CONTINENT = {
        # Africa
        'AFG': 'Asia', 'ALG': 'Africa', 'ANG': 'Africa', 'BEN': 'Africa', 'BOT': 'Africa',
        'BUR': 'Africa', 'BDI': 'Africa', 'CMR': 'Africa', 'CPV': 'Africa', 'CAF': 'Africa',
        'TCD': 'Africa', 'COM': 'Africa', 'CGO': 'Africa', 'COD': 'Africa', 'CIV': 'Africa',
        'DJI': 'Africa', 'EGY': 'Africa', 'GNQ': 'Africa', 'ERI': 'Africa', 'SWZ': 'Africa',
        'ETH': 'Africa', 'GAB': 'Africa', 'GAM': 'Africa', 'GHA': 'Africa', 'GUI': 'Africa',
        'GBS': 'Africa', 'KEN': 'Africa', 'LES': 'Africa', 'LBR': 'Africa', 'LBA': 'Africa',
        'MAD': 'Africa', 'MWI': 'Africa', 'MLI': 'Africa', 'MTN': 'Africa', 'MRI': 'Africa',
        'MAR': 'Africa', 'MOZ': 'Africa', 'NAM': 'Africa', 'NIG': 'Africa', 'NGA': 'Africa',
        'RWA': 'Africa', 'STP': 'Africa', 'SEN': 'Africa', 'SLE': 'Africa', 'SOM': 'Africa',
        'RSA': 'Africa', 'SSD': 'Africa', 'SDN': 'Africa', 'TAN': 'Africa', 'TOG': 'Africa',
        'TUN': 'Africa', 'UGA': 'Africa', 'ZAM': 'Africa', 'ZIM': 'Africa',
        
        # Asia
        'BHR': 'Asia', 'BAN': 'Asia', 'BHU': 'Asia', 'BRN': 'Asia', 'KHM': 'Asia',
        'CHN': 'Asia', 'TPE': 'Asia', 'HKG': 'Asia', 'IND': 'Asia', 'IDN': 'Asia',
        'IRN': 'Asia', 'IRQ': 'Asia', 'ISR': 'Asia', 'JPN': 'Asia', 'JOR': 'Asia',
        'KAZ': 'Asia', 'KOR': 'Asia', 'PRK': 'Asia', 'KWT': 'Asia', 'KGZ': 'Asia',
        'LAO': 'Asia', 'LBN': 'Asia', 'MAS': 'Asia', 'MDV': 'Asia', 'MGL': 'Asia',
        'MYA': 'Asia', 'NEP': 'Asia', 'OMA': 'Asia', 'PAK': 'Asia', 'PHI': 'Asia',
        'QAT': 'Asia', 'KSA': 'Asia', 'SGP': 'Asia', 'SRI': 'Asia', 'SYR': 'Asia',
        'TJK': 'Asia', 'THA': 'Asia', 'TLS': 'Asia', 'TUR': 'Asia', 'TKM': 'Asia',
        'UAE': 'Asia', 'UZB': 'Asia', 'VIE': 'Asia', 'YEM': 'Asia',
        
        # Europe
        'ALB': 'Europe', 'AND': 'Europe', 'ARM': 'Europe', 'AUT': 'Europe', 'AZE': 'Europe',
        'BLR': 'Europe', 'BEL': 'Europe', 'BIH': 'Europe', 'BUL': 'Europe', 'CRO': 'Europe',
        'CYP': 'Europe', 'CZE': 'Europe', 'DEN': 'Europe', 'EST': 'Europe', 'FIN': 'Europe',
        'FRA': 'Europe', 'GEO': 'Europe', 'GER': 'Europe', 'GBR': 'Europe', 'GRE': 'Europe',
        'HUN': 'Europe', 'ISL': 'Europe', 'IRL': 'Europe', 'ITA': 'Europe', 'LAT': 'Europe',
        'LIE': 'Europe', 'LTU': 'Europe', 'LUX': 'Europe', 'MKD': 'Europe', 'MLT': 'Europe',
        'MDA': 'Europe', 'MON': 'Europe', 'MNE': 'Europe', 'NED': 'Europe', 'NOR': 'Europe',
        'POL': 'Europe', 'POR': 'Europe', 'ROU': 'Europe', 'RUS': 'Europe', 'SMR': 'Europe',
        'SRB': 'Europe', 'SVK': 'Europe', 'SLO': 'Europe', 'ESP': 'Europe', 'SWE': 'Europe',
        'SUI': 'Europe', 'UKR': 'Europe',
        
        # North America
        'ANT': 'North America', 'ARU': 'North America', 'BAH': 'North America', 'BAR': 'North America',
        'BLZ': 'North America', 'BER': 'North America', 'CAN': 'North America', 'CAY': 'North America',
        'CRC': 'North America', 'CUB': 'North America', 'DMA': 'North America', 'DOM': 'North America',
        'ESA': 'North America', 'GRN': 'North America', 'GUA': 'North America', 'HAI': 'North America',
        'HON': 'North America', 'JAM': 'North America', 'MEX': 'North America', 'NCA': 'North America',
        'PAN': 'North America', 'PUR': 'North America', 'SKN': 'North America', 'LCA': 'North America',
        'VIN': 'North America', 'TTO': 'North America', 'USA': 'North America', 'ISV': 'North America',
        
        # South America
        'ARG': 'South America', 'BOL': 'South America', 'BRA': 'South America', 'CHI': 'South America',
        'COL': 'South America', 'ECU': 'South America', 'GUY': 'South America', 'PAR': 'South America',
        'PER': 'South America', 'SUR': 'South America', 'URU': 'South America', 'VEN': 'South America',
        
        # Oceania
        'ASA': 'Oceania', 'AUS': 'Oceania', 'COK': 'Oceania', 'FIJ': 'Oceania', 'GUM': 'Oceania',
        'KIR': 'Oceania', 'FSM': 'Oceania', 'NRU': 'Oceania', 'NZL': 'Oceania', 'PLW': 'Oceania',
        'PNG': 'Oceania', 'SAM': 'Oceania', 'SOL': 'Oceania', 'TGA': 'Oceania', 'TUV': 'Oceania',
        'VAN': 'Oceania',
    }
    
    # First check 3-letter NOC code mapping
    if noc_code in NOC_TO_CONTINENT:
        return NOC_TO_CONTINENT[noc_code]
    
    # If it's a 2-letter code, check CONTINENT_MAPPING
    if len(noc_code) == 2 and noc_code in CONTINENT_MAPPING:
        return CONTINENT_MAPPING[noc_code]
    
    # Try pycountry for 2-letter codes
    if len(noc_code) == 2:
        try:
            country = pycountry.countries.get(alpha_2=noc_code)
            if country:
                # Use the mapping if available
                if noc_code in CONTINENT_MAPPING:
                    return CONTINENT_MAPPING[noc_code]
        except:
            pass
    
    # Try pycountry for 3-letter codes (ISO alpha-3)
    if len(noc_code) == 3:
        try:
            country = pycountry.countries.get(alpha_3=noc_code)
            if country:
                # Try to map based on country name patterns
                name = country.name.lower()
                if any(x in name for x in ['united states', 'canada', 'mexico', 'cuba', 'jamaica']):
                    return 'North America'
                elif any(x in name for x in ['brazil', 'argentina', 'chile', 'colombia', 'peru']):
                    return 'South America'
                elif any(x in name for x in ['china', 'japan', 'india', 'korea', 'thailand', 'vietnam']):
                    return 'Asia'
                elif any(x in name for x in ['france', 'germany', 'italy', 'spain', 'united kingdom', 'russia']):
                    return 'Europe'
                elif any(x in name for x in ['australia', 'new zealand', 'fiji', 'samoa']):
                    return 'Oceania'
                elif any(x in name for x in ['south africa', 'egypt', 'nigeria', 'kenya', 'ethiopia']):
                    return 'Africa'
        except:
            pass
    
    # Default fallback
    return 'Unknown'

def load_data(data_path: str = "data") -> Dict[str, pd.DataFrame]:
    """Load all CSV files from the data directory"""
    files = {
        'athletes': 'athletes.csv',
        'coaches': 'coaches.csv',
        'events': 'events.csv',
        'medals': 'medals.csv',
        'medals_total': 'medals_total.csv',
        'medalists': 'medallists.csv',  # Note: file is medallists.csv (double 'l')
        'nocs': 'nocs.csv',
        'schedule': 'schedules.csv',  # Note: file is schedules.csv (plural)
        'schedule_preliminary': 'schedules_preliminary.csv',  # Note: file is schedules_preliminary.csv (plural)
        'teams': 'teams.csv',
        'technical_officials': 'technical_officials.csv',
        'torch_route': 'torch_route.csv',
        'venues': 'venues.csv'
    }
    
    data = {}
    for key, filename in files.items():
        try:
            filepath = f"{data_path}/{filename}"
            data[key] = pd.read_csv(filepath)
        except Exception as e:
            print(f"Warning: Could not load {filename}: {e}")
            data[key] = pd.DataFrame()
    
    return data

def add_continent_to_data(df: pd.DataFrame, noc_column: str = None) -> pd.DataFrame:
    """Add continent column to dataframe based on NOC code"""
    df = df.copy()
    
    # Auto-detect the NOC/code column if not specified
    if noc_column is None:
        if 'NOC' in df.columns:
            noc_column = 'NOC'
        elif 'code' in df.columns:
            noc_column = 'code'
        elif 'country_code' in df.columns:
            noc_column = 'country_code'
        else:
            # Try to find any column that might contain country codes
            for col in ['NOC', 'code', 'country_code', 'Code', 'Country_Code']:
                if col in df.columns:
                    noc_column = col
                    break
    
    if noc_column and noc_column in df.columns:
        df['Continent'] = df[noc_column].apply(get_continent_from_noc)
    else:
        df['Continent'] = 'Unknown'
    
    return df

def get_country_column(df: pd.DataFrame) -> str:
    """Get the country/NOC column name from a dataframe"""
    for col in ['NOC', 'code', 'country_code', 'Code', 'Country_Code']:
        if col in df.columns:
            return col
    return 'NOC'  # Default fallback

def filter_data(df: pd.DataFrame, 
                countries: List[str] = None,
                sports: List[str] = None,
                continents: List[str] = None,
                medal_types: List[str] = None,
                country_col: str = None,
                sport_col: str = 'Sport',
                continent_col: str = 'Continent',
                medal_col: str = 'Medal') -> pd.DataFrame:
    """Apply global filters to dataframe"""
    filtered_df = df.copy()
    
    # Auto-detect country column if not specified
    if country_col is None:
        country_col = get_country_column(df)
    
    if countries and len(countries) > 0 and country_col in filtered_df.columns:
        filtered_df = filtered_df[filtered_df[country_col].isin(countries)]
    
    if sports and len(sports) > 0:
        if sport_col in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[sport_col].isin(sports)]
    
    if continents and len(continents) > 0:
        if continent_col in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[continent_col].isin(continents)]
    
    if medal_types and len(medal_types) > 0:
        if medal_col in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[medal_col].isin(medal_types)]
    
    return filtered_df

def get_country_flag_emoji(country_name: str) -> str:
    """Get flag emoji for country name (simplified)"""
    flag_map = {
        'United States': '🇺🇸', 'China': '🇨🇳', 'Japan': '🇯🇵', 'France': '🇫🇷',
        'Germany': '🇩🇪', 'Italy': '🇮🇹', 'United Kingdom': '🇬🇧', 'Russia': '🇷🇺',
        'Australia': '🇦🇺', 'Canada': '🇨🇦', 'Brazil': '🇧🇷', 'South Korea': '🇰🇷',
        'Spain': '🇪🇸', 'Netherlands': '🇳🇱', 'Poland': '🇵🇱', 'India': '🇮🇳'
    }
    return flag_map.get(country_name, '🏳️')

def merge_athlete_coach_data(athletes_df: pd.DataFrame, 
                            coaches_df: pd.DataFrame,
                            teams_df: pd.DataFrame) -> pd.DataFrame:
    """Merge athlete data with coach information"""
    # This is a simplified merge - adjust based on actual data structure
    merged = athletes_df.copy()
    
    # Try to merge with teams first, then coaches
    if not teams_df.empty and 'Team' in athletes_df.columns:
        merged = merged.merge(teams_df, on='Team', how='left', suffixes=('', '_team'))
    
    return merged

