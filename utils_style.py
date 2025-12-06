"""
Paris 2024 Olympics Brand Styling
Shared CSS styling for all pages
"""

PARIS_2024_CSS = """
<style>
    /* Paris 2024 Olympics Brand Styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    h1 {
        color: #E91E63 !important; /* Paris Pink */
        font-weight: 700;
        border-bottom: 3px solid #E91E63;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    h2 {
        color: #6A1B9A !important; /* Purple/Lavender */
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    h3 {
        color: #1976D2 !important; /* Blue */
        font-weight: 600;
    }
    
    [data-testid="stMetricValue"] {
        color: #E91E63 !important;
        font-weight: 700;
        font-size: 2rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: #6A1B9A !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F8F9FA 0%, #FFFFFF 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
        color: #E91E63 !important;
        border-bottom: 2px solid #E91E63;
        padding-bottom: 0.3rem;
    }
    
    .stButton > button {
        background-color: #E91E63;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #C2185B;
        box-shadow: 0 4px 8px rgba(233, 30, 99, 0.3);
    }
    
    .stCheckbox label {
        color: #1A1A1A;
        font-weight: 500;
    }
    
    .stCheckbox input[type="checkbox"]:checked + label {
        color: #E91E63;
    }
    
    div[data-baseweb="select"] label,
    .stSelectbox label {
        color: #6A1B9A !important;
        font-weight: 600;
    }
    
    .stAlert {
        border-left: 4px solid #E91E63;
    }
    
    .stSuccess {
        border-left: 4px solid #4CAF50;
    }
    
    .stWarning {
        border-left: 4px solid #FF9800;
    }
    
    .stError {
        border-left: 4px solid #E91E63;
    }
</style>
"""

def inject_paris_2024_style():
    """Inject Paris 2024 brand styling into Streamlit page"""
    import streamlit as st
    st.markdown(PARIS_2024_CSS, unsafe_allow_html=True)

