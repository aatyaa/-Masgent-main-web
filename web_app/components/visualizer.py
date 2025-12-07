# web_app/components/visualizer.py
"""
3D Structure Visualization component for Masgent Web Application.
Uses stmol and py3Dmol for interactive crystal structure rendering.
"""
import streamlit as st
import os
from typing import Optional


# Element colors (CPK coloring scheme)
CPK_COLORS = {
    'H': '#FFFFFF', 'He': '#D9FFFF', 'Li': '#CC80FF', 'Be': '#C2FF00',
    'B': '#FFB5B5', 'C': '#909090', 'N': '#3050F8', 'O': '#FF0D0D',
    'F': '#90E050', 'Ne': '#B3E3F5', 'Na': '#AB5CF2', 'Mg': '#8AFF00',
    'Al': '#BFA6A6', 'Si': '#F0C8A0', 'P': '#FF8000', 'S': '#FFFF30',
    'Cl': '#1FF01F', 'Ar': '#80D1E3', 'K': '#8F40D4', 'Ca': '#3DFF00',
    'Sc': '#E6E6E6', 'Ti': '#BFC2C7', 'V': '#A6A6AB', 'Cr': '#8A99C7',
    'Mn': '#9C7AC7', 'Fe': '#E06633', 'Co': '#F090A0', 'Ni': '#50D050',
    'Cu': '#C88033', 'Zn': '#7D80B0', 'Ga': '#C28F8F', 'Ge': '#668F8F',
    'As': '#BD80E3', 'Se': '#FFA100', 'Br': '#A62929', 'Kr': '#5CB8D1',
    'Rb': '#702EB0', 'Sr': '#00FF00', 'Y': '#94FFFF', 'Zr': '#94E0E0',
    'Nb': '#73C2C9', 'Mo': '#54B5B5', 'Tc': '#3B9E9E', 'Ru': '#248F8F',
    'Rh': '#0A7D8C', 'Pd': '#006985', 'Ag': '#C0C0C0', 'Cd': '#FFD98F',
    'In': '#A67573', 'Sn': '#668080', 'Sb': '#9E63B5', 'Te': '#D47A00',
    'I': '#940094', 'Xe': '#429EB0', 'Cs': '#57178F', 'Ba': '#00C900',
    'La': '#70D4FF', 'Ce': '#FFFFC7', 'Pr': '#D9FFC7', 'Nd': '#C7FFC7',
    'Pm': '#A3FFC7', 'Sm': '#8FFFC7', 'Eu': '#61FFC7', 'Gd': '#45FFC7',
    'Tb': '#30FFC7', 'Dy': '#1FFFC7', 'Ho': '#00FF9C', 'Er': '#00E675',
    'Tm': '#00D452', 'Yb': '#00BF38', 'Lu': '#00AB24', 'Hf': '#4DC2FF',
    'Ta': '#4DA6FF', 'W': '#2194D6', 'Re': '#267DAB', 'Os': '#266696',
    'Ir': '#175487', 'Pt': '#D0D0E0', 'Au': '#FFD123', 'Hg': '#B8B8D0',
    'Tl': '#A6544D', 'Pb': '#575961', 'Bi': '#9E4FB5', 'Po': '#AB5C00',
    'At': '#754F45', 'Rn': '#428296', 'Fr': '#420066', 'Ra': '#007D00',
    'Ac': '#70ABFA', 'Th': '#00BAFF', 'Pa': '#00A1FF', 'U': '#008FFF',
    'Np': '#0080FF', 'Pu': '#006BFF', 'Am': '#545CF2', 'Cm': '#785CE3',
}


def get_element_color(symbol: str) -> str:
    """Get color for element symbol."""
    return CPK_COLORS.get(symbol, '#FF1493')  # Default to deep pink


def render_structure_3d(file_path: str, width: int = 600, height: int = 400):
    """
    Render 3D visualization of a crystal structure.
    
    Args:
        file_path: Path to structure file (POSCAR, CIF, XYZ)
        width: Width of the viewer
        height: Height of the viewer
    """
    if not os.path.exists(file_path):
        st.warning(f"Structure file not found: {file_path}")
        return
    
    try:
        import py3Dmol
        from stmol import showmol
        from ase.io import read
        from ase.data import covalent_radii, atomic_numbers
        
        # Read structure using ASE
        atoms = read(file_path)
        
        # Create the 3D model viewer
        view = py3Dmol.view(width=width, height=height)
        
        # Add atoms as spheres
        for atom in atoms:
            symbol = atom.symbol
            pos = atom.position
            color = get_element_color(symbol)
            
            # Get atomic radius (scaled down)
            radius = covalent_radii[atomic_numbers[symbol]] * 0.4
            
            view.addSphere({
                'center': {'x': pos[0], 'y': pos[1], 'z': pos[2]},
                'radius': radius,
                'color': color,
            })
        
        # Add unit cell if periodic
        if any(atoms.pbc):
            cell = atoms.get_cell()
            origin = [0, 0, 0]
            
            # Draw unit cell edges
            vertices = [
                origin,
                cell[0].tolist(),
                cell[1].tolist(),
                cell[2].tolist(),
                (cell[0] + cell[1]).tolist(),
                (cell[0] + cell[2]).tolist(),
                (cell[1] + cell[2]).tolist(),
                (cell[0] + cell[1] + cell[2]).tolist(),
            ]
            
            edges = [
                (0, 1), (0, 2), (0, 3),
                (1, 4), (1, 5), (2, 4), (2, 6),
                (3, 5), (3, 6), (4, 7), (5, 7), (6, 7)
            ]
            
            for i, j in edges:
                view.addLine({
                    'start': {'x': vertices[i][0], 'y': vertices[i][1], 'z': vertices[i][2]},
                    'end': {'x': vertices[j][0], 'y': vertices[j][1], 'z': vertices[j][2]},
                    'color': '#00FF00',
                    'opacity': 0.5,
                })
        
        # Style settings
        view.setBackgroundColor('#0e1117')
        view.zoomTo()
        view.spin(False)
        
        # Render
        showmol(view, height=height, width=width)
        
        # Structure information
        formula = atoms.get_chemical_formula()
        n_atoms = len(atoms)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Formula", formula)
        with col2:
            st.metric("Atoms", n_atoms)
        with col3:
            if any(atoms.pbc):
                vol = atoms.get_volume()
                st.metric("Volume", f"{vol:.2f} Å³")
        
        return True
        
    except ImportError as e:
        st.warning(f"""
        3D visualization requires additional packages. Install with:
        ```bash
        pip install stmol py3Dmol
        ```
        """)
        return False
        
    except Exception as e:
        st.error(f"Error rendering structure: {str(e)}")
        return False


def render_structure_info(file_path: str):
    """
    Render detailed structure information.
    
    Args:
        file_path: Path to structure file
    """
    if not os.path.exists(file_path):
        return
    
    try:
        from ase.io import read
        
        atoms = read(file_path)
        
        st.markdown("#### 📊 Structure Details")
        
        # Basic info
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Composition:**")
            from collections import Counter
            composition = Counter(atoms.get_chemical_symbols())
            comp_str = " ".join([f"{el}{count}" for el, count in sorted(composition.items())])
            st.code(comp_str)
        
        with col2:
            st.markdown("**Lattice Vectors (Å):**")
            cell = atoms.get_cell()
            cell_str = f"a = {cell[0]}\nb = {cell[1]}\nc = {cell[2]}"
            st.code(cell_str)
        
        # Lattice parameters
        st.markdown("**Lattice Parameters:**")
        from ase.geometry import cell_to_cellpar
        params = cell_to_cellpar(atoms.get_cell())
        
        cols = st.columns(6)
        labels = ['a (Å)', 'b (Å)', 'c (Å)', 'α (°)', 'β (°)', 'γ (°)']
        for i, (col, label) in enumerate(zip(cols, labels)):
            with col:
                st.metric(label, f"{params[i]:.3f}")
        
    except Exception as e:
        st.error(f"Error reading structure: {str(e)}")


def render_visualizer_panel(file_path: Optional[str] = None):
    """
    Render the complete visualizer panel with controls.
    
    Args:
        file_path: Optional path to structure file. If None, shows file selector.
    """
    st.markdown("### 🔮 Structure Visualization")
    
    session_path = st.session_state.get('session_path', '')
    
    # File selection if not provided
    if file_path is None:
        if os.path.exists(session_path):
            structure_files = [f for f in os.listdir(session_path) 
                             if f.lower().endswith(('.vasp', '.poscar', '.cif', '.xyz', 'poscar'))]
            
            if structure_files:
                selected = st.selectbox(
                    "Select structure file to visualize:",
                    structure_files,
                    key="viz_file_select"
                )
                file_path = os.path.join(session_path, selected)
            else:
                st.info("No structure files found in session. Upload or generate a structure first.")
                return
        else:
            st.info("Session directory not found.")
            return
    
    if file_path and os.path.exists(file_path):
        # Visualization controls
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**File:** `{os.path.basename(file_path)}`")
        with col2:
            show_info = st.checkbox("Show Details", value=False)
        
        # 3D Visualization
        success = render_structure_3d(file_path)
        
        # Show structure info if requested
        if show_info and success:
            render_structure_info(file_path)
        
        # Download button
        with open(file_path, 'rb') as f:
            st.download_button(
                "⬇️ Download Structure",
                f.read(),
                file_name=os.path.basename(file_path),
                mime="text/plain"
            )
