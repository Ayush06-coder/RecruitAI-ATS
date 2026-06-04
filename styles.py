def load_css():
    return """
    <style>
    /* ============ GLOBAL ============ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #030c10;
        color: #e2e8f0;
    }

    /* ============ SIDEBAR ============ */
    [data-testid="stSidebar"] {
        background: #050f15 !important;
        border-right: 1px solid #0a2a35 !important;
    }

    [data-testid="stSidebar"] .stMarkdown p {
        color: #a0aec0 !important;
    }

    [data-testid="stSidebarNav"] a {
        color: #a0aec0 !important;
        font-size: 0.9rem !important;
        padding: 0.5rem 1rem !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stSidebarNav"] a:hover {
        background: #0a2535 !important;
        color: #22d3ee !important;
    }

    [data-testid="stSidebarNav"] a[aria-selected="true"] {
        background: linear-gradient(135deg, #0891b2, #0e7490) !important;
        color: white !important;
    }

    /* ============ HEADINGS ============ */
    h1 {
        background: linear-gradient(135deg, #22d3ee, #67e8f9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        font-size: 2.2rem !important;
    }

    h2, h3 {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }

    /* ============ CARDS ============ */
    .card {
        background: #061a20;
        border: 1px solid #0a2a35;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }

    .card:hover {
        border-color: #0891b2;
        box-shadow: 0 0 20px rgba(8, 145, 178, 0.15);
        transform: translateY(-2px);
    }

    .card-title {
        font-size: 1rem;
        font-weight: 600;
        color: #22d3ee;
        margin-bottom: 0.5rem;
    }

    .card-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #e2e8f0;
    }

    /* ============ METRIC CARDS ============ */
    .metric-card {
        background: linear-gradient(135deg, #061a20, #0a2030);
        border: 1px solid #0e3a45;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
    }

    .metric-label {
        font-size: 0.8rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #22d3ee;
        margin-top: 0.3rem;
    }

    /* ============ BUTTONS ============ */
    .stButton > button {
        background: linear-gradient(135deg, #0891b2, #0e7490) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(8, 145, 178, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(8, 145, 178, 0.5) !important;
    }

    /* ============ INPUTS ============ */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #061a20 !important;
        border: 1px solid #0e3a45 !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #0891b2 !important;
        box-shadow: 0 0 0 3px rgba(8, 145, 178, 0.2) !important;
    }

    /* ============ FILE UPLOADER ============ */
    [data-testid="stFileUploader"] {
        background: #061a20 !important;
        border: 2px dashed #0e3a45 !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #0891b2 !important;
        background: #061820 !important;
    }

    /* ============ DATAFRAME ============ */
    [data-testid="stDataFrame"] {
        border: 1px solid #0a2a35 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* ============ EXPANDER ============ */
    .streamlit-expanderHeader {
        background: #061a20 !important;
        border: 1px solid #0a2a35 !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-weight: 500 !important;
    }

    .streamlit-expanderContent {
        background: #040e14 !important;
        border: 1px solid #0a2a35 !important;
        border-top: none !important;
    }

    /* ============ PROGRESS BAR ============ */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #0891b2, #67e8f9) !important;
        border-radius: 10px !important;
    }

    .stProgress > div > div {
        background: #0a2a35 !important;
        border-radius: 10px !important;
    }

    /* ============ ALERTS ============ */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 10px !important;
        color: #10b981 !important;
    }

    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 10px !important;
        color: #f59e0b !important;
    }

    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 10px !important;
        color: #ef4444 !important;
    }

    .stInfo {
        background: rgba(8, 145, 178, 0.1) !important;
        border: 1px solid rgba(8, 145, 178, 0.3) !important;
        border-radius: 10px !important;
        color: #22d3ee !important;
    }

    /* ============ DIVIDER ============ */
    hr {
        border-color: #0a2a35 !important;
        margin: 1.5rem 0 !important;
    }

    /* ============ SELECTBOX ============ */
    .stSelectbox > div > div {
        background: #061a20 !important;
        border: 1px solid #0e3a45 !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }

    /* ============ CAPTION ============ */
    .stCaption {
        color: #64748b !important;
        font-size: 0.85rem !important;
    }

    /* ============ BADGE ============ */
    .badge {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0.15rem;
    }

    .badge-purple {
        background: rgba(34, 211, 238, 0.15);
        color: #22d3ee;
        border: 1px solid rgba(34, 211, 238, 0.3);
    }

    .badge-green {
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .badge-red {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    .badge-yellow {
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    /* ============ HERO SECTION ============ */
    .hero {
        background: linear-gradient(135deg, #061a20 0%, #0a2535 100%);
        border: 1px solid #0e3a45;
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
    }

    .hero-subtitle {
        color: #64748b;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }

    /* ============ FEATURE CARD ============ */
    .feature-card {
        background: #061a20;
        border: 1px solid #0a2a35;
        border-radius: 14px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }

    .feature-card:hover {
        border-color: #0891b2;
        box-shadow: 0 0 25px rgba(8, 145, 178, 0.2);
        transform: translateY(-3px);
    }

    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.8rem;
    }

    .feature-title {
        font-size: 1rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 0.5rem;
    }

    .feature-desc {
        font-size: 0.85rem;
        color: #64748b;
        line-height: 1.5;
    }

    /* ============ RANK CARD ============ */
    .rank-card {
        background: #061a20;
        border: 1px solid #0a2a35;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }

    .rank-card:hover {
        border-color: #0891b2;
        box-shadow: 0 0 20px rgba(8, 145, 178, 0.15);
    }

    .rank-number {
        font-size: 2rem;
        font-weight: 700;
        color: #0891b2;
    }

    /* ============ LOGIN CARD ============ */
    .login-card {
        background: #061a20;
        border: 1px solid #0e3a45;
        border-radius: 20px;
        padding: 3rem 2.5rem;
        max-width: 420px;
        margin: 0 auto;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
    }

    .login-title {
        font-size: 1.8rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #22d3ee, #67e8f9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .login-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }

    /* ============ SCROLLBAR ============ */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }

    ::-webkit-scrollbar-track {
        background: #030c10;
    }

    ::-webkit-scrollbar-thumb {
        background: #0e3a45;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #0891b2;
    }
    </style>
    """

def inject_css():
    import streamlit as st
    st.markdown(load_css(), unsafe_allow_html=True)