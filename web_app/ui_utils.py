# web_app/ui_utils.py
"""
Core utility module for dynamically converting Pydantic schemas to Streamlit widgets.
This is the engine that powers automatic form generation from schemas.
"""
import streamlit as st
from pydantic import BaseModel, ValidationError
from typing import get_args, get_origin, Literal, List, Dict, Optional, Union, Any
import os
import json


def get_session_files(session_path: str, extensions: List[str] = None) -> List[str]:
    """
    List files in the session directory, optionally filtered by extension.
    
    Args:
        session_path: Path to session directory
        extensions: Optional list of extensions to filter (e.g., ['.cif', '.vasp'])
    
    Returns:
        List of filenames in the directory
    """
    if not os.path.exists(session_path):
        return []
    
    files = [f for f in os.listdir(session_path) if os.path.isfile(os.path.join(session_path, f))]
    
    if extensions:
        files = [f for f in files if any(f.lower().endswith(ext.lower()) for ext in extensions)]
    
    return sorted(files)


def save_uploaded_file(uploaded_file, session_path: str) -> str:
    """
    Save an uploaded file to the session directory.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        session_path: Path to save the file
    
    Returns:
        Full path to the saved file
    """
    if uploaded_file is None:
        return None
    
    os.makedirs(session_path, exist_ok=True)
    save_path = os.path.join(session_path, uploaded_file.name)
    
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return save_path


def render_file_input(field_name: str, field_info, session_path: str, key_prefix: str = "") -> str:
    """
    Render a file input with two options: upload new or use existing session file.
    
    Args:
        field_name: Name of the field
        field_info: Pydantic field info
        session_path: Path to session directory
        key_prefix: Prefix for widget keys to avoid conflicts
    
    Returns:
        Selected file path or None
    """
    label = field_name.replace('_', ' ').title()
    help_text = field_info.description if field_info.description else ""
    default_val = field_info.default if field_info.default is not ... else ""
    
    st.markdown(f"**{label}**")
    if help_text:
        st.caption(help_text)
    
    tab1, tab2 = st.tabs(["📂 Session Files", "⬆️ Upload New"])
    
    selected_path = None
    
    with tab1:
        files = get_session_files(session_path)
        if files:
            selected_file = st.selectbox(
                f"Select file for {field_name}",
                ["(none)"] + files,
                key=f"{key_prefix}_{field_name}_select",
                label_visibility="collapsed"
            )
            if selected_file and selected_file != "(none)":
                selected_path = os.path.join(session_path, selected_file)
        else:
            st.info("No files in session. Upload a file or run a tool first.")
    
    with tab2:
        uploaded = st.file_uploader(
            f"Upload file for {field_name}",
            key=f"{key_prefix}_{field_name}_upload",
            label_visibility="collapsed"
        )
        if uploaded:
            saved_path = save_uploaded_file(uploaded, session_path)
            if saved_path:
                st.success(f"✅ Saved: {uploaded.name}")
                selected_path = saved_path
    
    # Return selected path or default
    return selected_path if selected_path else (default_val if isinstance(default_val, str) else "")


def render_list_input(field_name: str, field_info, item_type, key_prefix: str = "") -> List:
    """
    Render input for List types.
    
    Args:
        field_name: Name of the field
        field_info: Pydantic field info
        item_type: Type of items in the list
        key_prefix: Prefix for widget keys
    
    Returns:
        Parsed list value
    """
    label = field_name.replace('_', ' ').title()
    help_text = field_info.description if field_info.description else ""
    default_val = field_info.default if field_info.default is not ... else []
    
    default_str = str(default_val).replace("'", '"') if default_val else "[]"
    
    if item_type == int:
        st.markdown(f"**{label}** (comma-separated integers)")
        text = st.text_input(
            label,
            value=", ".join(map(str, default_val)) if default_val else "",
            help=help_text,
            key=f"{key_prefix}_{field_name}",
            label_visibility="collapsed"
        )
        try:
            return [int(x.strip()) for x in text.split(",") if x.strip()]
        except:
            return default_val
    
    elif item_type == float:
        st.markdown(f"**{label}** (comma-separated numbers)")
        text = st.text_input(
            label,
            value=", ".join(map(str, default_val)) if default_val else "",
            help=help_text,
            key=f"{key_prefix}_{field_name}",
            label_visibility="collapsed"
        )
        try:
            return [float(x.strip()) for x in text.split(",") if x.strip()]
        except:
            return default_val
    
    else:
        # Generic list as JSON
        st.markdown(f"**{label}** (JSON format)")
        text = st.text_area(
            label,
            value=default_str,
            help=help_text,
            key=f"{key_prefix}_{field_name}",
            label_visibility="collapsed"
        )
        try:
            return json.loads(text)
        except:
            return default_val


def render_dict_input(field_name: str, field_info, key_prefix: str = "") -> Dict:
    """
    Render input for Dict types using JSON text area.
    
    Args:
        field_name: Name of the field
        field_info: Pydantic field info
        key_prefix: Prefix for widget keys
    
    Returns:
        Parsed dictionary value
    """
    label = field_name.replace('_', ' ').title()
    help_text = field_info.description if field_info.description else ""
    default_val = field_info.default if field_info.default is not ... else {}
    
    default_str = json.dumps(default_val, indent=2) if default_val else "{}"
    
    st.markdown(f"**{label}** (JSON format)")
    if help_text:
        st.caption(help_text)
    
    text = st.text_area(
        label,
        value=default_str,
        height=150,
        key=f"{key_prefix}_{field_name}",
        label_visibility="collapsed"
    )
    
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON: {e}")
        return default_val


def render_pydantic_input(field_name: str, field_info, session_path: str, key_prefix: str = "") -> Any:
    """
    Map a single Pydantic field to appropriate Streamlit widget.
    
    Args:
        field_name: Name of the field
        field_info: Pydantic FieldInfo object
        session_path: Path to session directory for file handling
        key_prefix: Prefix for widget keys to avoid conflicts
    
    Returns:
        Value entered by user
    """
    field_type = field_info.annotation
    default_val = field_info.default
    help_text = field_info.description if field_info.description else ""
    label = field_name.replace('_', ' ').title()
    
    # Handle Optional types - extract inner type
    origin = get_origin(field_type)
    if origin is Union:
        args = get_args(field_type)
        # Check if it's Optional (Union with None)
        non_none_args = [a for a in args if a is not type(None)]
        if len(non_none_args) == 1:
            field_type = non_none_args[0]
            origin = get_origin(field_type)
        # Handle Union[float, int] case
        elif set(non_none_args) == {float, int}:
            field_type = float
            origin = None

    # 1. Literal types -> Selectbox
    if origin is Literal:
        options = list(get_args(field_type))
        default_idx = 0
        if default_val is not ... and default_val in options:
            default_idx = options.index(default_val)
        return st.selectbox(
            label,
            options,
            index=default_idx,
            help=help_text,
            key=f"{key_prefix}_{field_name}"
        )
    
    # 2. Boolean -> Checkbox
    elif field_type is bool:
        default = default_val if default_val is not ... else False
        return st.checkbox(
            label,
            value=default,
            help=help_text,
            key=f"{key_prefix}_{field_name}"
        )
    
    # 3. Integer -> Number input
    elif field_type is int:
        default = default_val if default_val is not ... else 0
        return st.number_input(
            label,
            value=int(default),
            step=1,
            help=help_text,
            key=f"{key_prefix}_{field_name}"
        )
    
    # 4. Float -> Number input
    elif field_type is float:
        default = default_val if default_val is not ... else 0.0
        return st.number_input(
            label,
            value=float(default),
            step=0.01,
            format="%.4f",
            help=help_text,
            key=f"{key_prefix}_{field_name}"
        )
    
    # 5. List types
    elif origin is list or origin is List:
        args = get_args(field_type)
        item_type = args[0] if args else str
        return render_list_input(field_name, field_info, item_type, key_prefix)
    
    # 6. Dict types
    elif origin is dict or origin is Dict:
        return render_dict_input(field_name, field_info, key_prefix)
    
    # 7. String - check if it's a file path
    elif field_type is str:
        # Detect file path fields by name
        if any(kw in field_name.lower() for kw in ['path', 'file', 'poscar', 'cif']):
            return render_file_input(field_name, field_info, session_path, key_prefix)
        else:
            # Use smart input helper for special fields
            from input_helpers import render_smart_text_input, FIELD_HELPERS
            
            default = default_val if default_val is not ... else ""
            
            # Check if this field has a helper
            if field_name in FIELD_HELPERS:
                return render_smart_text_input(
                    field_name=field_name,
                    label=label,
                    help_text=help_text,
                    default=default,
                    key=f"{key_prefix}_{field_name}"
                )
            else:
                # Standard text input
                return st.text_input(
                    label,
                    value=default,
                    help=help_text,
                    key=f"{key_prefix}_{field_name}",
                    placeholder=f"Enter {label.lower()}..."
                )
    
    # 8. Fallback - generic text input
    else:
        default = str(default_val) if default_val is not ... else ""
        return st.text_input(
            f"{label} (Complex Type)",
            value=default,
            help=help_text,
            key=f"{key_prefix}_{field_name}"
        )


def render_schema_form(schema_class: type, session_path: str, key_prefix: str = "") -> Dict[str, Any]:
    """
    Automatically generate a Streamlit form from a Pydantic model class.
    
    Args:
        schema_class: The Pydantic BaseModel class (not instance)
        session_path: Path to session directory for file handling
        key_prefix: Prefix for widget keys to avoid conflicts
    
    Returns:
        Dictionary of field names to entered values
    """
    form_data = {}
    
    # Get the model fields
    if not hasattr(schema_class, 'model_fields'):
        st.error("Invalid schema: not a Pydantic model")
        return form_data
    
    # Group fields: required first, then optional
    required_fields = []
    optional_fields = []
    
    for name, field in schema_class.model_fields.items():
        if field.default is ... and field.default_factory is None:
            required_fields.append((name, field))
        else:
            optional_fields.append((name, field))
    
    # Render required fields
    if required_fields:
        st.markdown("### Required Parameters")
        for name, field in required_fields:
            val = render_pydantic_input(name, field, session_path, key_prefix)
            if val is not None and val != "":
                form_data[name] = val
    
    # Render optional fields in expander
    if optional_fields:
        with st.expander("⚙️ Optional Parameters", expanded=False):
            for name, field in optional_fields:
                val = render_pydantic_input(name, field, session_path, key_prefix)
                if val is not None and val != "":
                    form_data[name] = val
    
    return form_data


def validate_form_data(schema_class: type, form_data: Dict[str, Any]) -> tuple:
    """
    Validate form data against Pydantic schema.
    
    Args:
        schema_class: The Pydantic BaseModel class
        form_data: Dictionary of form values
    
    Returns:
        Tuple of (is_valid: bool, result_or_error: model instance or error string)
    """
    try:
        validated = schema_class(**form_data)
        return True, validated
    except ValidationError as e:
        error_messages = []
        for error in e.errors():
            field = ".".join(str(loc) for loc in error['loc'])
            msg = error['msg']
            error_messages.append(f"**{field}**: {msg}")
        return False, "\n".join(error_messages)
    except Exception as e:
        return False, str(e)


def display_result(result: Any, session_path: str):
    """
    Display tool execution result in a formatted way.
    
    Args:
        result: The result from tool execution
        session_path: Session directory path
    """
    if result is None:
        st.warning("Tool returned no output.")
        return
    
    if isinstance(result, str):
        # Check if it's a file path that was created
        if os.path.exists(result):
            st.success(f"✅ File created: `{os.path.basename(result)}`")
            
            # Show file content for small text files
            if result.endswith(('.vasp', '.poscar', '.cif', '.xyz', '.txt', '.sh')):
                with st.expander("📄 View File Contents"):
                    with open(result, 'r') as f:
                        st.code(f.read(), language="text")
                
                # Download button
                with open(result, 'rb') as f:
                    st.download_button(
                        "⬇️ Download File",
                        f.read(),
                        file_name=os.path.basename(result),
                        mime="text/plain"
                    )
        else:
            st.info(result)
    
    elif isinstance(result, dict):
        st.json(result)
    
    elif isinstance(result, (list, tuple)):
        if all(isinstance(item, str) and os.path.exists(item) for item in result):
            st.success(f"✅ Created {len(result)} files")
            for item in result:
                st.write(f"- `{os.path.basename(item)}`")
        else:
            st.write(result)
    
    else:
        st.write(result)


def render_structure_visualizer(file_path: str):
    """
    Render 3D visualization of a crystal structure file.
    
    Args:
        file_path: Path to structure file (POSCAR, CIF, XYZ)
    """
    if not os.path.exists(file_path):
        st.warning(f"File not found: {file_path}")
        return
    
    try:
        import py3Dmol
        from stmol import showmol
        from ase.io import read
        from ase import Atoms
        
        # Read structure
        atoms = read(file_path)
        
        # Convert to XYZ string for py3Dmol
        xyz_str = f"{len(atoms)}\n"
        xyz_str += f"Generated from {os.path.basename(file_path)}\n"
        
        for atom in atoms:
            xyz_str += f"{atom.symbol} {atom.position[0]:.6f} {atom.position[1]:.6f} {atom.position[2]:.6f}\n"
        
        # Create 3D viewer
        view = py3Dmol.view(width=600, height=400)
        view.addModel(xyz_str, "xyz")
        view.setStyle({'sphere': {'radius': 0.4}, 'stick': {'radius': 0.1}})
        view.setBackgroundColor('#0e1117')
        view.zoomTo()
        
        showmol(view, height=400, width=600)
        
        # Show structure info
        st.caption(f"**Formula:** {atoms.get_chemical_formula()} | **Atoms:** {len(atoms)}")
        
    except ImportError:
        st.warning("3D visualization requires `stmol` and `py3Dmol`. Install with: `pip install stmol py3Dmol`")
    except Exception as e:
        st.error(f"Error visualizing structure: {e}")
