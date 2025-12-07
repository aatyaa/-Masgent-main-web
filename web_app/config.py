# web_app/config.py
"""
Configuration and Tool Registry for Masgent Web Application.
Maps tool names to their corresponding functions and Pydantic schemas.
"""
import os
import sys
from pathlib import Path

# Add src directory to path for imports
SRC_DIR = Path(__file__).parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Import tools from Masgent
from masgent.tools import (
    generate_vasp_poscar,
    generate_vasp_inputs_from_poscar,
    generate_vasp_inputs_hpc_slurm_script,
    convert_structure_format,
    convert_poscar_coordinates,
    customize_vasp_kpoints_with_accuracy,
    generate_vasp_poscar_with_vacancy_defects,
    generate_vasp_poscar_with_substitution_defects,
    generate_vasp_poscar_with_interstitial_defects,
    generate_supercell_from_poscar,
    generate_sqs_from_poscar,
    generate_surface_slab_from_poscar,
    generate_interface_from_poscars,
    generate_vasp_workflow_of_convergence_tests,
    generate_vasp_workflow_of_eos,
    generate_vasp_workflow_of_elastic_constants,
    generate_vasp_workflow_of_aimd,
    generate_vasp_workflow_of_neb,
    run_simulation_using_mlps,
    analyze_features_for_machine_learning,
    reduce_dimensions_for_machine_learning,
    augment_data_for_machine_learning,
    design_model_for_machine_learning,
    train_model_for_machine_learning,
)

# Import Pydantic schemas from Masgent
from masgent.schemas import (
    GenerateVaspPoscarSchema,
    GenerateVaspInputsFromPoscar,
    GenerateVaspInputsHpcSlurmScript,
    ConvertStructureFormatSchema,
    ConvertPoscarCoordinatesSchema,
    CustomizeVaspKpointsWithAccuracy,
    GenerateVaspPoscarWithVacancyDefects,
    GenerateVaspPoscarWithSubstitutionDefects,
    GenerateVaspPoscarWithInterstitialDefects,
    GenerateSupercellFromPoscar,
    GenerateSqsFromPoscar,
    GenerateSurfaceSlabFromPoscar,
    GenerateInterfaceFromPoscars,
    GenerateVaspWorkflowOfConvergenceTests,
    GenerateVaspWorkflowOfEos,
    GenerateVaspWorkflowOfElasticConstants,
    GenerateVaspWorkflowOfAimd,
    GenerateVaspWorkflowOfNeb,
    RunSimulationUsingMlps,
    AnalyzeFeaturesForMachineLearning,
    ReduceDimensionsForMachineLearning,
    AugmentDataForMachineLearning,
    DesignModelForMachineLearning,
    TrainModelForMachineLearning,
)

# App Configuration
APP_TITLE = "Masgent Web"
APP_ICON = "⚛️"
SESSION_DIR_NAME = "masgent_sessions"
BASE_DIR = Path(os.getcwd())

# Tool Registry: Maps category -> tool name -> {func, schema, desc, icon}
TOOL_REGISTRY = {
    "🧪 Structure Preparation": {
        "Generate POSCAR": {
            "func": generate_vasp_poscar,
            "schema": GenerateVaspPoscarSchema,
            "desc": "Generate a POSCAR file from chemical formula using Materials Project database.",
            "icon": "🔮"
        },
        "Convert Structure Format": {
            "func": convert_structure_format,
            "schema": ConvertStructureFormatSchema,
            "desc": "Convert between CIF, POSCAR, and XYZ formats.",
            "icon": "🔄"
        },
        "Convert POSCAR Coordinates": {
            "func": convert_poscar_coordinates,
            "schema": ConvertPoscarCoordinatesSchema,
            "desc": "Convert between Direct and Cartesian coordinates.",
            "icon": "📐"
        },
        "Generate Supercell": {
            "func": generate_supercell_from_poscar,
            "schema": GenerateSupercellFromPoscar,
            "desc": "Create supercell from POSCAR using scaling matrix.",
            "icon": "🔳"
        },
        "Generate Surface Slab": {
            "func": generate_surface_slab_from_poscar,
            "schema": GenerateSurfaceSlabFromPoscar,
            "desc": "Generate surface slab from bulk structure.",
            "icon": "🪨"
        },
        "Generate Interface": {
            "func": generate_interface_from_poscars,
            "schema": GenerateInterfaceFromPoscars,
            "desc": "Generate interface structure from two POSCAR files.",
            "icon": "🔗"
        },
        "Generate SQS": {
            "func": generate_sqs_from_poscar,
            "schema": GenerateSqsFromPoscar,
            "desc": "Generate Special Quasirandom Structures for alloys.",
            "icon": "🎲"
        },
    },
    "🔧 Defect Generation": {
        "Vacancy Defects": {
            "func": generate_vasp_poscar_with_vacancy_defects,
            "schema": GenerateVaspPoscarWithVacancyDefects,
            "desc": "Create POSCAR with vacancy defects.",
            "icon": "⭕"
        },
        "Substitution Defects": {
            "func": generate_vasp_poscar_with_substitution_defects,
            "schema": GenerateVaspPoscarWithSubstitutionDefects,
            "desc": "Create POSCAR with substitutional defects.",
            "icon": "🔀"
        },
        "Interstitial Defects": {
            "func": generate_vasp_poscar_with_interstitial_defects,
            "schema": GenerateVaspPoscarWithInterstitialDefects,
            "desc": "Create POSCAR with interstitial defects.",
            "icon": "➕"
        },
    },
    "📁 VASP Input Preparation": {
        "Full VASP Inputs": {
            "func": generate_vasp_inputs_from_poscar,
            "schema": GenerateVaspInputsFromPoscar,
            "desc": "Generate complete VASP input files (INCAR, KPOINTS, POTCAR).",
            "icon": "📦"
        },
        "Customize KPOINTS": {
            "func": customize_vasp_kpoints_with_accuracy,
            "schema": CustomizeVaspKpointsWithAccuracy,
            "desc": "Generate KPOINTS with specified accuracy level.",
            "icon": "🎯"
        },
        "HPC Slurm Script": {
            "func": generate_vasp_inputs_hpc_slurm_script,
            "schema": GenerateVaspInputsHpcSlurmScript,
            "desc": "Generate SLURM job submission script.",
            "icon": "🖥️"
        },
    },
    "📊 VASP Workflows": {
        "Convergence Tests": {
            "func": generate_vasp_workflow_of_convergence_tests,
            "schema": GenerateVaspWorkflowOfConvergenceTests,
            "desc": "Setup ENCUT and KPOINTS convergence tests.",
            "icon": "📈"
        },
        "Equation of State": {
            "func": generate_vasp_workflow_of_eos,
            "schema": GenerateVaspWorkflowOfEos,
            "desc": "Setup EOS calculations for bulk modulus.",
            "icon": "📉"
        },
        "Elastic Constants": {
            "func": generate_vasp_workflow_of_elastic_constants,
            "schema": GenerateVaspWorkflowOfElasticConstants,
            "desc": "Setup elastic constants calculations.",
            "icon": "💪"
        },
        "AIMD Simulation": {
            "func": generate_vasp_workflow_of_aimd,
            "schema": GenerateVaspWorkflowOfAimd,
            "desc": "Setup Ab-initio Molecular Dynamics.",
            "icon": "🔥"
        },
        "NEB Calculation": {
            "func": generate_vasp_workflow_of_neb,
            "schema": GenerateVaspWorkflowOfNeb,
            "desc": "Setup Nudged Elastic Band calculations.",
            "icon": "🛤️"
        },
    },
    "⚡ ML Potentials": {
        "Run ML Simulation": {
            "func": run_simulation_using_mlps,
            "schema": RunSimulationUsingMlps,
            "desc": "Fast simulations using ML potentials (CHGNet, SevenNet, Orb-v3, MatSim).",
            "icon": "🚀"
        },
    },
    "🤖 Machine Learning": {
        "Feature Analysis": {
            "func": analyze_features_for_machine_learning,
            "schema": AnalyzeFeaturesForMachineLearning,
            "desc": "Analyze feature correlations for ML.",
            "icon": "📊"
        },
        "Dimensionality Reduction": {
            "func": reduce_dimensions_for_machine_learning,
            "schema": ReduceDimensionsForMachineLearning,
            "desc": "Reduce feature dimensions using PCA.",
            "icon": "📉"
        },
        "Data Augmentation": {
            "func": augment_data_for_machine_learning,
            "schema": AugmentDataForMachineLearning,
            "desc": "Augment training data using VAE.",
            "icon": "📈"
        },
        "Model Design": {
            "func": design_model_for_machine_learning,
            "schema": DesignModelForMachineLearning,
            "desc": "Design ML model with Optuna optimization.",
            "icon": "🏗️"
        },
        "Model Training": {
            "func": train_model_for_machine_learning,
            "schema": TrainModelForMachineLearning,
            "desc": "Train and evaluate ML model.",
            "icon": "🎓"
        },
    },
}

# Get all category names
def get_categories():
    return list(TOOL_REGISTRY.keys())

# Get tools for a category
def get_tools_for_category(category: str):
    return list(TOOL_REGISTRY.get(category, {}).keys())

# Get tool config
def get_tool_config(category: str, tool_name: str):
    return TOOL_REGISTRY.get(category, {}).get(tool_name, None)
