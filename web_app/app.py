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
    /* Import Clean Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Light Theme Colors - Easy on Eyes */
    :root {
        --primary: #4F46E5;
        --primary-light: #818CF8;
        --secondary: #06B6D4;
        --success: #10B981;
        --warning: #F59E0B;
        --error: #EF4444;
        --bg-main: #F9FAFB;
        --bg-card: #FFFFFF;
        --text-primary: #1F2937;
        --text-secondary: #6B7280;
        --border: #E5E7EB;
        --shadow: rgba(0, 0, 0, 0.05);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Background */
    .main {
        background-color: var(--bg-main);
        padding: 1.5rem;
    }
    
    /* Sidebar - Clean White */
    [data-testid="stSidebar"] {
        background-color: var(--bg-card);
        border-right: 1px solid var(--border);
        box-shadow: 2px 0 8px var(--shadow);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 1.5rem 1rem;
    }
    
    /* Headers - Clean Typography */
    h1 {
        color: var(--text-primary);
        font-weight: 700;
        font-size: 2rem;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    h2 {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    h3 {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 1.125rem;
        margin-bottom: 0.5rem;
    }
    
    /* Cards & Containers - Clean White */
    .stExpander, .stForm {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        box-shadow: 0 1px 3px var(--shadow);
    }
    
    /* Buttons - Clean Primary Color */
    .stButton > button {
        background-color: var(--primary);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.625rem 1.25rem;
        font-weight: 500;
        font-size: 0.9375rem;
        transition: all 0.2s ease;
        box-shadow: 0 1px 2px var(--shadow);
    }
    
    .stButton > button:hover {
        background-color: var(--primary-light);
        box-shadow: 0 2px 4px var(--shadow);
        transform: translateY(-1px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Primary Button Variant */
    .stButton > button[kind="primary"] {
        background-color: var(--secondary);
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #0891B2;
    }
    
    /* Input Fields - Clean & Simple */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 0.625rem 0.875rem;
        color: var(--text-primary);
        font-size: 0.9375rem;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        outline: none;
    }
    
    /* Tabs - Clean Design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
        border-bottom: 1px solid var(--border);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        border-bottom: 2px solid transparent;
        padding: 0.75rem 1rem;
        color: var(--text-secondary);
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
    }
    
    /* Alert Messages - Soft Colors */
    .stSuccess {
        background-color: #ECFDF5;
        border-left: 4px solid var(--success);
        border-radius: 6px;
        padding: 1rem;
        color: #065F46;
    }
    
    .stError {
        background-color: #FEF2F2;
        border-left: 4px solid var(--error);
        border-radius: 6px;
        padding: 1rem;
        color: #991B1B;
    }
    
    .stWarning {
        background-color: #FFFBEB;
        border-left: 4px solid var(--warning);
        border-radius: 6px;
        padding: 1rem;
        color: #92400E;
    }
    
    .stInfo {
        background-color: #EFF6FF;
        border-left: 4px solid: #3B82F6;
        border-radius: 6px;
        padding: 1rem;
        color: #1E40AF;
    }
    
    /* Metrics - Clean Display */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--primary);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-weight: 500;
    }
    
    /* File Uploader - Clean Border */
    [data-testid="stFileUploader"] {
        background-color: var(--bg-card);
        border: 2px dashed var(--border);
        border-radius: 8px;
        padding: 1.5rem;
        transition: all 0.2s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--primary);
        background-color: rgba(79, 70, 229, 0.02);
    }
    
    /* Divider - Subtle */
    hr {
        border: none;
        height: 1px;
        background-color: var(--border);
        margin: 1.5rem 0;
    }
    
    /* Chat Messages - Clean Cards */
    .stChatMessage {
        background-color: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Scrollbar - Minimal */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-main);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #D1D5DB;
    }
    
    /* Code Blocks - Subtle Background */
    code {
        background-color: #F3F4F6;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        color: #DC2626;
        font-family: 'Monaco', 'Courier New', monospace;
        font-size: 0.875rem;
    }
    
    pre {
        background-color: #F9FAFB;
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 1rem;
    }
    
    /* Radio & Checkbox - Clean */
    .stRadio > label, .stCheckbox > label {
        color: var(--text-primary);
        font-size: 0.9375rem;
    }
    
    /* Expander - Clean Arrow */
    .streamlit-expanderHeader {
        background-color: var(--bg-card);
        color: var(--text-primary);
        font-weight: 500;
    }
    
    /* Loading Spinner */
    .stSpinner > div {
        border-top-color: var(--primary) !important;
    }
    
    /* Caption Text */
    .caption {
        color: var(--text-secondary);
        font-size: 0.875rem;
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
