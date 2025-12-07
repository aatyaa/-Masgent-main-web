# web_app/input_helpers.py
"""
Advanced Input Helper System
Provides examples, hints, validation, and smart suggestions for all input types.
"""
import streamlit as st
from typing import Dict, Any, List, Optional
import re


# ============================================================================
# FIELD-SPECIFIC HELPERS AND EXAMPLES
# ============================================================================

FIELD_HELPERS = {
    'scaling_matrix': {
        'examples': [
            ('2x2x2 supercell', '2 0 0; 0 2 0; 0 0 2'),
            ('3x3x1 supercell', '3 0 0; 0 3 0; 0 0 1'),
            ('2x1x1 supercell', '2 0 0; 0 1 0; 0 0 1'),
        ],
        'format': 'a b c; d e f; g h i (semicolon-separated rows)',
        'validation': lambda x: validate_scaling_matrix(x),
        'hint': '💡 Use semicolons to separate rows, spaces for numbers'
    },
    
    'formula': {
        'examples': [
            ('Silicon', 'Si'),
            ('Sodium Chloride', 'NaCl'),
            ('Titanium Dioxide', 'TiO2'),
            ('Perovskite', 'SrTiO3'),
        ],
        'format': 'Chemical formula (e.g., NaCl, TiO2)',
        'validation': lambda x: validate_formula(x),
        'hint': '💡 Use element symbols with optional numbers'
    },
    
    'mp_id': {
        'examples': [
            ('Silicon', 'mp-149'),
            ('NaCl', 'mp-22862'),
            ('Diamond', 'mp-66'),
        ],
        'format': 'mp-XXXXX (Materials Project ID)',
        'validation': lambda x: validate_mp_id(x),
        'hint': '💡 Find IDs at materialsproject.org'
    },
    
    'kpoints': {
        'examples': [
            ('Standard', '4 4 4'),
            ('Dense', '8 8 8'),
            ('Anisotropic', '6 6 4'),
        ],
        'format': 'kx ky kz (space-separated integers)',
        'validation': lambda x: validate_kpoints(x),
        'hint': '💡 Higher values = more accurate but slower'
    },
}


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_scaling_matrix(value: str) -> tuple[bool, str]:
    """Validate scaling matrix format."""
    if not value or not value.strip():
        return False, "Scaling matrix cannot be empty"
    
    try:
        rows = value.split(';')
        if len(rows) != 3:
            return False, f"Expected 3 rows, got {len(rows)}"
        
        for i, row in enumerate(rows):
            nums = row.strip().split()
            if len(nums) != 3:
                return False, f"Row {i+1}: Expected 3 numbers, got {len(nums)}"
            
            for num in nums:
                int(num)  # Check if it's an integer
        
        return True, "✅ Valid scaling matrix"
    except ValueError:
        return False, "All values must be integers"
    except Exception as e:
        return False, f"Invalid format: {str(e)}"


def validate_formula(value: str) -> tuple[bool, str]:
    """Validate chemical formula."""
    if not value or not value.strip():
        return False, "Formula cannot be empty"
    
    # Basic check: starts with capital letter, contains only letters and numbers
    if not re.match(r'^[A-Z][a-zA-Z0-9]*$', value):
        return False, "Formula must start with capital letter and contain only letters/numbers"
    
    return True, "✅ Valid formula"


def validate_mp_id(value: str) -> tuple[bool, str]:
    """Validate Materials Project ID."""
    if not value or not value.strip():
        return False, "MP ID cannot be empty"
    
    if not re.match(r'^mp-\d+$', value):
        return False, "MP ID must be in format: mp-XXXXX"
    
    return True, "✅ Valid MP ID"


def validate_kpoints(value: str) -> tuple[bool, str]:
    """Validate k-points format."""
    if not value or not value.strip():
        return False, "K-points cannot be empty"
    
    try:
        nums = value.strip().split()
        if len(nums) != 3:
            return False, f"Expected 3 numbers, got {len(nums)}"
        
        for num in nums:
            k = int(num)
            if k < 1:
                return False, "K-points must be positive integers"
        
        return True, "✅ Valid k-points"
    except ValueError:
        return False, "K-points must be integers"


# ============================================================================
# SMART INPUT WIDGETS
# ============================================================================

def render_smart_text_input(
    field_name: str,
    label: str,
    help_text: str = "",
    default: str = "",
    key: str = None
) -> str:
    """
    Render a smart text input with examples, hints, and real-time validation.
    """
    # Get helper info if available
    helper = FIELD_HELPERS.get(field_name, None)
    
    # Create columns for label and examples
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**{label}**")
        if help_text:
            st.caption(help_text)
    
    with col2:
        if helper and 'examples' in helper:
            # Example selector
            example_labels = [ex[0] for ex in helper['examples']]
            selected_example = st.selectbox(
                "Quick Examples",
                ["(none)"] + example_labels,
                key=f"{key}_example",
                label_visibility="collapsed"
            )
            
            if selected_example != "(none)":
                # Find the example value
                for ex_label, ex_value in helper['examples']:
                    if ex_label == selected_example:
                        default = ex_value
                        break
    
    # Show format hint
    if helper and 'format' in helper:
        st.caption(f"📋 Format: {helper['format']}")
    
    # Main input
    value = st.text_input(
        label,
        value=default,
        key=key,
        label_visibility="collapsed",
        placeholder=f"Enter {label.lower()}..."
    )
    
    # Real-time validation
    if value and helper and 'validation' in helper:
        is_valid, message = helper['validation'](value)
        if is_valid:
            st.success(message, icon="✅")
        else:
            st.error(message, icon="❌")
    
    # Show hint
    if helper and 'hint' in helper:
        st.info(helper['hint'], icon="💡")
    
    return value


def render_smart_number_input(
    label: str,
    help_text: str = "",
    default: float = 0.0,
    min_value: float = None,
    max_value: float = None,
    step: float = 0.01,
    key: str = None,
    is_int: bool = False
) -> float:
    """
    Render a smart number input with range hints and validation.
    """
    st.markdown(f"**{label}**")
    if help_text:
        st.caption(help_text)
    
    # Show range if specified
    if min_value is not None or max_value is not None:
        range_text = "Range: "
        if min_value is not None:
            range_text += f"min={min_value}"
        if max_value is not None:
            if min_value is not None:
                range_text += ", "
            range_text += f"max={max_value}"
        st.caption(f"📊 {range_text}")
    
    value = st.number_input(
        label,
        value=int(default) if is_int else float(default),
        min_value=min_value,
        max_value=max_value,
        step=int(step) if is_int else step,
        key=key,
        label_visibility="collapsed"
    )
    
    return value


def render_smart_selectbox(
    label: str,
    options: List[str],
    help_text: str = "",
    default_index: int = 0,
    key: str = None,
    descriptions: Dict[str, str] = None
) -> str:
    """
    Render a smart selectbox with option descriptions.
    """
    st.markdown(f"**{label}**")
    if help_text:
        st.caption(help_text)
    
    value = st.selectbox(
        label,
        options,
        index=default_index,
        key=key,
        label_visibility="collapsed"
    )
    
    # Show description for selected option
    if descriptions and value in descriptions:
        st.info(descriptions[value], icon="ℹ️")
    
    return value


def render_input_summary(form_data: Dict[str, Any]):
    """
    Display a summary of all entered data before submission.
    """
    if not form_data:
        return
    
    with st.expander("📋 Input Summary", expanded=False):
        st.markdown("### Review Your Inputs")
        
        for key, value in form_data.items():
            formatted_key = key.replace('_', ' ').title()
            st.markdown(f"**{formatted_key}:** `{value}`")


# ============================================================================
# VALIDATION SUMMARY
# ============================================================================

def show_validation_summary(schema_class: type, form_data: Dict[str, Any]):
    """
    Show a comprehensive validation summary before submission.
    """
    from pydantic import ValidationError
    
    try:
        # Try to validate
        validated = schema_class(**form_data)
        
        st.success("✅ All inputs are valid!", icon="✅")
        
        # Show what will be executed
        with st.expander("🔍 Execution Preview"):
            st.json(form_data)
        
        return True, validated
        
    except ValidationError as e:
        st.error("❌ Validation Errors Found", icon="❌")
        
        for error in e.errors():
            field = ".".join(str(loc) for loc in error['loc'])
            msg = error['msg']
            
            st.markdown(f"**{field}:** {msg}")
        
        return False, None
