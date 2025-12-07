# web_app/components/sidebar.py
"""
Sidebar component for Masgent Web Application.
Handles navigation, API key configuration, and session management.
"""
import streamlit as st
import os
from pathlib import Path


def render_api_keys_section():
    """Render API key input section in sidebar."""
    st.markdown("### 🔑 API Keys")
    
    # Gemini API Key
    gemini_key = st.text_input(
        "Gemini API Key",
        type="password",
        help="Required for AI Agent features",
        key="gemini_key_input"
    )
    if gemini_key:
        os.environ["GEMINI_API_KEY"] = gemini_key
        st.session_state.gemini_key_set = True
    
    # Materials Project API Key
    mp_key = st.text_input(
        "Materials Project Key",
        type="password",
        help="Required for generating structures from MP database",
        key="mp_key_input"
    )
    if mp_key:
        os.environ["MP_API_KEY"] = mp_key
        st.session_state.mp_key_set = True
    
    # Status indicators
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.get("gemini_key_set"):
            st.success("Gemini ✓", icon="✅")
        else:
            st.warning("Gemini ✗", icon="⚠️")
    with col2:
        if st.session_state.get("mp_key_set"):
            st.success("MP ✓", icon="✅")
        else:
            st.warning("MP ✗", icon="⚠️")


def render_session_files_section(session_path: str):
    """Render session files section in sidebar."""
    st.markdown("### 📁 Session Files")
    
    if os.path.exists(session_path):
        files = [f for f in os.listdir(session_path) if os.path.isfile(os.path.join(session_path, f))]
        if files:
            for f in sorted(files)[:10]:  # Show max 10 files
                st.text(f"📄 {f}")
            if len(files) > 10:
                st.caption(f"... and {len(files) - 10} more files")
        else:
            st.caption("No files yet. Run a tool to generate files.")
    else:
        st.caption("Session directory not created yet.")


def render_sidebar():
    """Render the complete sidebar."""
    with st.sidebar:
        # Logo and title with modern styling
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="font-size: 2rem; margin: 0;">⚛️</h1>
            <h2 style="font-size: 1.5rem; margin: 0.5rem 0 0 0;">Masgent</h2>
            <p style="color: #888; font-size: 0.9rem; margin: 0.25rem 0 0 0;">Materials Simulation</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Session info with modern card
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 12px; margin-bottom: 1rem;">
            <p style="margin: 0; font-size: 0.85rem; color: rgba(255,255,255,0.8);">Session ID</p>
            <p style="margin: 0.25rem 0 0 0; font-size: 1.1rem; font-weight: 600; color: white;">
                {st.session_state.get('session_id', 'N/A')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mode selection with icons
        st.markdown("### 🎯 Select Mode")
        mode = st.radio(
            "Choose your workflow",
            ["🛠️ Manual Tools", "🤖 AI Agent"],
            label_visibility="collapsed",
            key="mode_selector"
        )
        
        st.divider()
        
        # API Keys section
        render_api_keys_section()
        
        st.divider()
        
        # Session Files with count
        session_path = st.session_state.get('session_path', '')
        file_count = 0
        if os.path.exists(session_path):
            file_count = len([f for f in os.listdir(session_path) if os.path.isfile(os.path.join(session_path, f))])
        
        st.markdown(f"### 📁 Session Files ({file_count})")
        
        render_session_files_section(session_path)
        
        st.divider()
        
        # Quick Stats
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Tools", "24", delta=None)
        with col2:
            st.metric("Categories", "6", delta=None)
        
        st.divider()
        
        # Footer with links
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; color: #666;">
            <p style="font-size: 0.85rem; margin: 0;">Masgent Web v1.0</p>
            <p style="font-size: 0.75rem; margin: 0.5rem 0 0 0;">
                <a href="https://github.com/aguang5241/masgent" style="color: #667eea; text-decoration: none;">
                    GitHub
                </a> • 
                <a href="https://github.com/aguang5241/masgent#readme" style="color: #667eea; text-decoration: none;">
                    Docs
                </a>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        return mode
