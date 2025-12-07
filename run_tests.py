#!/usr/bin/env python3
"""
Comprehensive Test Suite for Masgent Web App
Tests all components and functionality
"""
import sys
import os
from pathlib import Path

# Setup paths
PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR / "web_app"))
sys.path.insert(0, str(PROJECT_DIR / "src"))

print("=" * 70)
print("🧪 MASGENT WEB APP - COMPREHENSIVE TEST SUITE")
print("=" * 70)
print()

# Test 1: Import all modules
print("📦 Test 1: Module Imports")
print("-" * 70)

test_results = []

try:
    from config import TOOL_REGISTRY, get_categories, get_tools_for_category
    print("✅ config.py imported successfully")
    test_results.append(("Config Import", True, None))
except Exception as e:
    print(f"❌ config.py import failed: {e}")
    test_results.append(("Config Import", False, str(e)))

try:
    from ui_utils import (
        render_pydantic_input,
        render_schema_form,
        validate_form_data,
        render_structure_visualizer
    )
    print("✅ ui_utils.py imported successfully")
    test_results.append(("UI Utils Import", True, None))
except Exception as e:
    print(f"❌ ui_utils.py import failed: {e}")
    test_results.append(("UI Utils Import", False, str(e)))

try:
    from components.sidebar import render_sidebar
    from components.tool_forms import render_tool_forms
    from components.ai_chat import render_ai_chat
    from components.visualizer import render_visualizer_panel
    print("✅ All components imported successfully")
    test_results.append(("Components Import", True, None))
except Exception as e:
    print(f"❌ Components import failed: {e}")
    test_results.append(("Components Import", False, str(e)))

print()

# Test 2: Tool Registry Validation
print("🔧 Test 2: Tool Registry Validation")
print("-" * 70)

try:
    categories = get_categories()
    print(f"✅ Found {len(categories)} categories:")
    for cat in categories:
        tools = get_tools_for_category(cat)
        print(f"   {cat}: {len(tools)} tools")
    
    total_tools = sum(len(get_tools_for_category(cat)) for cat in categories)
    print(f"✅ Total tools registered: {total_tools}")
    test_results.append(("Tool Registry", True, None))
except Exception as e:
    print(f"❌ Tool registry validation failed: {e}")
    test_results.append(("Tool Registry", False, str(e)))

print()

# Test 3: Schema Validation
print("📋 Test 3: Pydantic Schema Validation")
print("-" * 70)

try:
    from masgent.schemas import (
        GenerateVaspPoscarSchema,
        RunSimulationUsingMlps,
        GenerateVaspInputsFromPoscar
    )
    
    # Test schema instantiation
    test_schema = GenerateVaspPoscarSchema(formula="NaCl")
    print(f"✅ Schema validation works: {test_schema.formula}")
    
    # Test invalid schema
    try:
        invalid = GenerateVaspPoscarSchema(formula="InvalidFormula123")
        print("⚠️  Schema validation might be too lenient")
    except:
        print("✅ Schema validation catches invalid inputs")
    
    test_results.append(("Schema Validation", True, None))
except Exception as e:
    print(f"❌ Schema validation failed: {e}")
    test_results.append(("Schema Validation", False, str(e)))

print()

# Test 4: Masgent Tools Import
print("🛠️  Test 4: Masgent Tools Import")
print("-" * 70)

try:
    from masgent.tools import (
        generate_vasp_poscar,
        run_simulation_using_mlps,
        generate_vasp_inputs_from_poscar
    )
    print("✅ Core tools imported successfully")
    print(f"   - generate_vasp_poscar: {callable(generate_vasp_poscar)}")
    print(f"   - run_simulation_using_mlps: {callable(run_simulation_using_mlps)}")
    print(f"   - generate_vasp_inputs_from_poscar: {callable(generate_vasp_inputs_from_poscar)}")
    test_results.append(("Tools Import", True, None))
except Exception as e:
    print(f"❌ Tools import failed: {e}")
    test_results.append(("Tools Import", False, str(e)))

print()

# Test 5: Dependencies Check
print("📚 Test 5: Critical Dependencies")
print("-" * 70)

dependencies = [
    ("streamlit", "Streamlit framework"),
    ("stmol", "3D visualization"),
    ("py3Dmol", "3D molecule viewer"),
    ("plotly", "Interactive charts"),
    ("ase", "Atomic Simulation Environment"),
    ("pymatgen", "Materials analysis"),
    ("pydantic_ai", "AI agent framework"),
]

for module_name, description in dependencies:
    try:
        __import__(module_name)
        print(f"✅ {module_name:20s} - {description}")
        test_results.append((f"Dependency: {module_name}", True, None))
    except ImportError as e:
        print(f"❌ {module_name:20s} - {description} (MISSING)")
        test_results.append((f"Dependency: {module_name}", False, str(e)))

print()

# Test 6: File Structure
print("📁 Test 6: File Structure")
print("-" * 70)

required_files = [
    "web_app/app.py",
    "web_app/config.py",
    "web_app/ui_utils.py",
    "web_app/components/sidebar.py",
    "web_app/components/tool_forms.py",
    "web_app/components/ai_chat.py",
    "web_app/components/visualizer.py",
    "requirements_web.txt",
    "install_deps.py",
    "WEB_APP_GUIDE.md",
]

for file_path in required_files:
    full_path = PROJECT_DIR / file_path
    if full_path.exists():
        size = full_path.stat().st_size
        print(f"✅ {file_path:45s} ({size:,} bytes)")
        test_results.append((f"File: {file_path}", True, None))
    else:
        print(f"❌ {file_path:45s} (MISSING)")
        test_results.append((f"File: {file_path}", False, "File not found"))

print()

# Test 7: Session Directory Creation
print("💾 Test 7: Session Management")
print("-" * 70)

try:
    import uuid
    session_id = str(uuid.uuid4())[:8]
    session_dir = PROJECT_DIR / "masgent_sessions" / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    
    # Set environment variable
    os.environ['MASGENT_SESSION_RUNS_DIR'] = str(session_dir)
    
    print(f"✅ Session directory created: {session_dir}")
    print(f"✅ Environment variable set: MASGENT_SESSION_RUNS_DIR")
    
    # Cleanup test session
    session_dir.rmdir()
    
    test_results.append(("Session Management", True, None))
except Exception as e:
    print(f"❌ Session management failed: {e}")
    test_results.append(("Session Management", False, str(e)))

print()

# Test 8: Tool Configuration Validation
print("⚙️  Test 8: Tool Configuration Validation")
print("-" * 70)

try:
    from config import TOOL_REGISTRY
    
    issues = []
    for category, tools in TOOL_REGISTRY.items():
        for tool_name, config in tools.items():
            # Check required keys
            if 'func' not in config:
                issues.append(f"{category}/{tool_name}: Missing 'func'")
            if 'schema' not in config:
                issues.append(f"{category}/{tool_name}: Missing 'schema'")
            if 'desc' not in config:
                issues.append(f"{category}/{tool_name}: Missing 'desc'")
            
            # Check if func is callable
            if 'func' in config and not callable(config['func']):
                issues.append(f"{category}/{tool_name}: 'func' is not callable")
    
    if issues:
        print(f"⚠️  Found {len(issues)} configuration issues:")
        for issue in issues[:5]:  # Show first 5
            print(f"   - {issue}")
        test_results.append(("Tool Config", False, f"{len(issues)} issues"))
    else:
        print(f"✅ All {total_tools} tools properly configured")
        test_results.append(("Tool Config", True, None))
        
except Exception as e:
    print(f"❌ Tool configuration validation failed: {e}")
    test_results.append(("Tool Config", False, str(e)))

print()

# Summary
print("=" * 70)
print("📊 TEST SUMMARY")
print("=" * 70)

passed = sum(1 for _, success, _ in test_results if success)
failed = sum(1 for _, success, _ in test_results if not success)
total = len(test_results)

print(f"\n✅ Passed: {passed}/{total}")
print(f"❌ Failed: {failed}/{total}")
print(f"📈 Success Rate: {(passed/total)*100:.1f}%")

if failed > 0:
    print("\n❌ Failed Tests:")
    for name, success, error in test_results:
        if not success:
            print(f"   - {name}: {error}")

print()

if failed == 0:
    print("🎉 ALL TESTS PASSED! The web app is ready to use.")
    print()
    print("🚀 To run the app:")
    print("   streamlit run web_app/app.py")
    sys.exit(0)
else:
    print("⚠️  Some tests failed. Please review the errors above.")
    sys.exit(1)
