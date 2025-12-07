# web_app/app.py
"""
Masgent Web Application - Main Entry Point
==========================================

A production-grade Streamlit web application for materials simulation.
Wraps the Masgent CLI tool with a modern, interactive web interface.

Run with: streamlit run web_app/app.py
"""
import streamlit as st
import os
import sys
import uuid
from pathlib import Path

# ============================================================================
# PATH SETUP - Add necessary directories to Python path
# ============================================================================
WEBAPP_DIR = Path(__file__).parent
PROJECT_DIR = WEBAPP_DIR.parent
SRC_DIR = PROJECT_DIR / "src"

# Add paths for imports
if str(WEBAPP_DIR) not in sys.path:
    sys.path.insert(0, str(WEBAPP_DIR))
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# ============================================================================
# PAGE CONFIGURATION - Must be first Streamlit command
# ============================================================================
st.set_page_config(
    page_title="Masgent Web - Materials Simulation Agent",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/aguang5241/masgent/issues',
        'Report a bug': 'https://github.com/aguang5241/masgent/issues',
        'About': """
        ## Masgent Web
        **Materials Simulation Agent**
        
        A Streamlit-based web interface for DFT workflows, ML potentials, 
        and machine learning for materials science.
        
        © 2025 Guangchen Liu | MIT License
        """
    }
)

# ============================================================================
# CUSTOM CSS STYLING - Clean Light Theme
# ============================================================================
st.markdown("""
<style>
    /* ============================================
       DESIGN SYSTEM - COLOR PALETTE & VARIABLES
       ============================================ */
    :root {
        --primary: #4F46E5;
        --primary-hover: #4338CA;
        --secondary: #06B6D4;
        --success: #10B981;
        --error: #EF4444;
        --warning: #F59E0B;
        
        --text-dark: #111827;
        --text-medium: #374151;
        --text-light: #6B7280;
        
        --bg-white: #FFFFFF;
        --bg-gray-50: #F9FAFB;
        --bg-gray-100: #F3F4F6;
        
        --border-light: #E5E7EB;
        --border-medium: #D1D5DB;
        
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        
        --radius-sm: 6px;
        --radius-md: 8px;
        --radius-lg: 12px;
        
        --spacing-xs: 0.25rem;
        --spacing-sm: 0.5rem;
        --spacing-md: 1rem;
        --spacing-lg: 1.5rem;
        --spacing-xl: 2rem;
    }
    
    /* ============================================
       BASE STYLES
       ============================================ */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main {
        background-color: var(--bg-gray-50);
        padding: var(--spacing-xl);
    }
    
    /* ============================================
       TYPOGRAPHY - CLEAR HIERARCHY
       ============================================ */
    h1 {
        color: var(--text-dark);
        font-size: 2rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: var(--spacing-md);
        letter-spacing: -0.02em;
    }
    
    h2 {
        color: var(--text-dark);
        font-size: 1.5rem;
        font-weight: 600;
        line-height: 1.3;
        margin-bottom: var(--spacing-md);
    }
    
    h3 {
        color: var(--text-medium);
        font-size: 1.125rem;
        font-weight: 600;
        line-height: 1.4;
        margin-bottom: var(--spacing-sm);
    }
    
    p {
        color: var(--text-medium);
        font-size: 0.9375rem;
        line-height: 1.6;
    }
    
    /* ============================================
       SIDEBAR - CLEAN & ORGANIZED
       ============================================ */
    [data-testid="stSidebar"] {
        background-color: var(--bg-white);
        border-right: 1px solid var(--border-light);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: var(--spacing-lg);
    }
    
    /* ============================================
       CARDS & CONTAINERS
       ============================================ */
    .stExpander, .stForm {
        background-color: var(--bg-white) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: var(--radius-md) !important;
        padding: var(--spacing-lg) !important;
        margin: var(--spacing-md) 0 !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    /* ============================================
       BUTTONS - CLEAR & CLICKABLE
       ============================================ */
    .stButton > button {
        background-color: var(--primary);
        color: white;
        border: none;
        border-radius: var(--radius-sm);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.9375rem;
        transition: all 0.15s ease;
        box-shadow: var(--shadow-sm);
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background-color: var(--primary-hover);
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* ============================================
       FORM INPUTS - CLEAN & SPACIOUS
       ============================================ */
    
    /* All Input Labels - NO OVERLAP */
    label {
        color: var(--text-dark) !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        margin-bottom: var(--spacing-sm) !important;
        display: block !important;
        line-height: 1.5 !important;
        padding-bottom: var(--spacing-xs) !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: var(--bg-white) !important;
        border: 1.5px solid var(--border-medium) !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.75rem !important;
        color: var(--text-dark) !important;
        font-size: 0.9375rem !important;
        line-height: 1.5 !important;
        transition: all 0.2s ease !important;
        margin-top: var(--spacing-xs) !important;
    }
    
    /* Input Focus State */
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
        outline: none !important;
    }
    
    /* Help Text */
    .stTextInput small,
    .stNumberInput small,
    .stSelectbox small {
        color: var(--text-light) !important;
        font-size: 0.8125rem !important;
        margin-top: var(--spacing-xs) !important;
        display: block !important;
        line-height: 1.4 !important;
    }
    
    /* ============================================
       SELECT BOXES - CLEAR DROPDOWN
       ============================================ */
    .stSelectbox > div > div {
        margin-top: var(--spacing-xs) !important;
    }
    
    .stSelectbox label {
        margin-bottom: var(--spacing-sm) !important;
    }
    
    /* ============================================
       RADIO & CHECKBOX
       ============================================ */
    .stRadio > label,
    .stCheckbox > label {
        color: var(--text-dark) !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        margin-bottom: var(--spacing-sm) !important;
    }
    
    .stRadio > div,
    .stCheckbox > div {
        margin-top: var(--spacing-sm) !important;
    }
    
    /* ============================================
       TABS - CLEAN NAVIGATION
       ============================================ */
    .stTabs [data-baseweb="tab-list"] {
        gap: var(--spacing-sm);
        background: transparent;
        border-bottom: 2px solid var(--border-light);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        border-bottom: 2px solid transparent;
        padding: var(--spacing-md);
        color: var(--text-light);
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--primary);
        background-color: rgba(79, 70, 229, 0.05);
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--primary);
        border-bottom-color: var(--primary);
        font-weight: 600;
    }
    
    /* ============================================
       ALERTS - SOFT COLORS
       ============================================ */
    .stSuccess {
        background-color: #ECFDF5;
        border-left: 4px solid var(--success);
        border-radius: var(--radius-sm);
        padding: var(--spacing-md);
        color: #065F46;
    }
    
    .stError {
        background-color: #FEF2F2;
        border-left: 4px solid var(--error);
        border-radius: var(--radius-sm);
        padding: var(--spacing-md);
        color: #991B1B;
    }
    
    .stWarning {
        background-color: #FFFBEB;
        border-left: 4px solid var(--warning);
        border-radius: var(--radius-sm);
        padding: var(--spacing-md);
        color: #92400E;
    }
    
    /* ============================================
       FILE UPLOADER
       ============================================ */
    [data-testid="stFileUploader"] {
        background-color: var(--bg-white);
        border: 2px dashed var(--border-medium);
        border-radius: var(--radius-md);
        padding: var(--spacing-xl);
        transition: all 0.2s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--primary);
        background-color: rgba(79, 70, 229, 0.02);
    }
    
    /* ============================================
       DIVIDER
       ============================================ */
    hr {
        border: none;
        height: 1px;
        background-color: var(--border-light);
        margin: var(--spacing-lg) 0;
    }
    
    /* ============================================
       CHAT MESSAGES
       ============================================ */
    .stChatMessage {
        background-color: var(--bg-white);
        border: 1px solid var(--border-light);
        border-radius: var(--radius-md);
        padding: var(--spacing-md);
        margin: var(--spacing-sm) 0;
    }
    
    /* ============================================
       SCROLLBAR - MINIMAL
       ============================================ */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-gray-50);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-medium);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-light);
    }
    
    /* ============================================
       CODE BLOCKS
       ============================================ */
    code {
        background-color: var(--bg-gray-100);
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        color: #DC2626;
        font-family: 'Monaco', 'Courier New', monospace;
        font-size: 0.875rem;
    }
    
    pre {
        background-color: var(--bg-gray-50);
        border: 1px solid var(--border-light);
        border-radius: var(--radius-sm);
        padding: var(--spacing-md);
    }
    
    /* ============================================
       EXPANDER
       ============================================ */
    .streamlit-expanderHeader {
        background-color: var(--bg-white);
        color: var(--text-dark);
        font-weight: 600;
        padding: var(--spacing-md);
        border-radius: var(--radius-sm);
    }
    
    /* ============================================
       METRICS
       ============================================ */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        color: var(--text-light);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* ============================================
       REMOVE STREAMLIT BRANDING
       ============================================ */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ============================================
       LOADING SPINNER
       ============================================ */
    .stSpinner > div {
        border-top-color: var(--primary) !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
def init_session_state():
    """Initialize all session state variables."""
    
    # Session ID
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())[:8]
    
    # Session directory path
    if "session_path" not in st.session_state:
        session_dir = PROJECT_DIR / "masgent_sessions" / st.session_state.session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        st.session_state.session_path = str(session_dir)
        
        # Set environment variable for Masgent tools
        os.environ['MASGENT_SESSION_RUNS_DIR'] = str(session_dir)
    
    # API key status
    if "gemini_key_set" not in st.session_state:
        st.session_state.gemini_key_set = bool(os.environ.get("GEMINI_API_KEY"))
    
    if "mp_key_set" not in st.session_state:
        st.session_state.mp_key_set = bool(os.environ.get("MP_API_KEY"))
    
    # Chat history for AI mode
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "pending_plan" not in st.session_state:
        st.session_state.pending_plan = None


# Initialize session state
init_session_state()

# ============================================================================
# IMPORT COMPONENTS (after path setup)
# ============================================================================
try:
    from components.sidebar import render_sidebar
    from components.tool_forms import render_tool_forms
    from components.ai_chat import render_ai_chat
    from components.visualizer import render_visualizer_panel
except ImportError as e:
    st.error(f"Error importing components: {e}")
    st.info("Make sure you're running from the project root: `streamlit run web_app/app.py`")
    st.stop()

# ============================================================================
# SIDEBAR
# ============================================================================
mode = render_sidebar()

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================
# Clean, Simple Header
st.markdown("""
<div style="padding: 1rem 0 2rem 0;">
    <h1 style="font-size: 2.25rem; font-weight: 700; margin: 0; color: #1F2937;">
        ⚛️ Masgent Web
    </h1>
    <p style="font-size: 1rem; color: #6B7280; margin: 0.5rem 0 0 0;">
        Materials Simulation Platform
    </p>
</div>
""", unsafe_allow_html=True)

# Route based on selected mode
if mode == "🛠️ Manual Tools":
    # Manual Tools Mode
    render_tool_forms()
    
    # Show visualizer if files exist
    session_path = st.session_state.get('session_path', '')
    if os.path.exists(session_path):
        structure_files = [f for f in os.listdir(session_path) 
                         if any(f.lower().endswith(ext) for ext in ['.vasp', '.poscar', '.cif', '.xyz']) 
                         or 'poscar' in f.lower()]
        if structure_files:
            st.divider()
            render_visualizer_panel()

elif mode == "🤖 AI Agent":
    # AI Agent Mode
    render_ai_chat()

else:
    st.warning("Unknown mode selected.")

# ============================================================================
# FOOTER
# ============================================================================
st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.caption("📁 **Session:** " + st.session_state.session_id)
with col2:
    st.caption("📂 **Files:** " + st.session_state.session_path)
with col3:
    st.caption("🔗 [GitHub](https://github.com/aguang5241/masgent) | [Documentation](https://github.com/aguang5241/masgent#readme)")
