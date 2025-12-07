# web_app/components/tool_forms.py
"""
Tool Forms component for Masgent Web Application.
Handles dynamic form generation and tool execution.
"""
import streamlit as st
import os
from typing import Dict, Any

# Import from parent package
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import TOOL_REGISTRY, get_categories, get_tools_for_category, get_tool_config
from ui_utils import render_schema_form, validate_form_data, display_result, render_structure_visualizer


def render_tool_selector():
    """Render tool category and tool selection dropdowns."""
    col1, col2 = st.columns(2)
    
    with col1:
        category = st.selectbox(
            "📂 Category",
            get_categories(),
            key="tool_category"
        )
    
    with col2:
        tools = get_tools_for_category(category)
        tool_name = st.selectbox(
            "🔧 Tool",
            tools,
            key="tool_name"
        )
    
    return category, tool_name


def render_tool_header(tool_config: Dict[str, Any]):
    """Render tool header with icon and description."""
    icon = tool_config.get('icon', '🔧')
    desc = tool_config.get('desc', 'No description available.')
    
    st.markdown(f"### {icon} Tool Configuration")
    st.info(desc)


def execute_tool(tool_config: Dict[str, Any], validated_data) -> Any:
    """Execute the tool with validated data."""
    func = tool_config['func']
    
    # Convert Pydantic model to dict for function args
    kwargs = validated_data.model_dump()
    
    # Execute with spinner
    with st.spinner("🔄 Running tool..."):
        try:
            result = func(**kwargs)
            return result
        except Exception as e:
            raise e


def render_tool_forms():
    """Render the complete tool forms interface."""
    st.header("🛠️ Simulation Toolkit")
    
    # Tool selection
    category, tool_name = render_tool_selector()
    
    # Get tool configuration
    tool_config = get_tool_config(category, tool_name)
    
    if not tool_config:
        st.error("Tool not found in registry.")
        return
    
    st.divider()
    
    # Tool header
    render_tool_header(tool_config)
    
    # Get the schema class
    schema_class = tool_config['schema']
    session_path = st.session_state.get('session_path', '')
    
    # Render form
    with st.form(key=f"tool_form_{category}_{tool_name}"):
        form_data = render_schema_form(
            schema_class,
            session_path,
            key_prefix=f"{category}_{tool_name}"
        )
        
        st.divider()
        
        col1, col2 = st.columns([3, 1])
        with col1:
            submitted = st.form_submit_button("🚀 Execute Tool", use_container_width=True, type="primary")
        with col2:
            clear = st.form_submit_button("🗑️ Clear", use_container_width=True)
    
    # Handle submission
    if submitted:
        st.divider()
        st.markdown("### 📊 Results")
        
        # Validate
        is_valid, result = validate_form_data(schema_class, form_data)
        
        if not is_valid:
            st.error("**Validation Error:**")
            st.markdown(result)
        else:
            try:
                # Execute tool
                exec_result = execute_tool(tool_config, result)
                
                st.success("✅ Tool executed successfully!")
                
                # Display result
                display_result(exec_result, session_path)
                
                # Try to visualize if it's a structure file
                if isinstance(exec_result, str) and os.path.exists(exec_result):
                    if any(exec_result.lower().endswith(ext) for ext in ['.vasp', '.poscar', '.cif', '.xyz']):
                        st.divider()
                        st.markdown("### 🔮 Structure Visualization")
                        render_structure_visualizer(exec_result)
                
            except Exception as e:
                st.error(f"**Execution Error:** {str(e)}")
                
                # Show traceback in expander
                import traceback
                with st.expander("🔍 Full Error Details"):
                    st.code(traceback.format_exc())
