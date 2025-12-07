#!/usr/bin/env python3
"""
Quick dependency installer for Masgent Web App
Run this before starting the Streamlit app
"""
import subprocess
import sys

def install_package(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])

print("🔧 Installing Masgent Web App dependencies...")
print()

# Core dependencies
packages = [
    "colorama",
    "ase",
    "pymatgen",
    "numpy",
    "pandas",
    "scipy",
    "scikit-learn",
    "matplotlib",
    "seaborn",
    "pydantic-ai",
    "mp-api",
    "python-dotenv",
    "bullet",
    "yaspin",
    "streamlit",
    "stmol",
    "py3Dmol",
    "plotly",
]

total = len(packages)
for i, package in enumerate(packages, 1):
    print(f"[{i}/{total}] Installing {package}...", end=" ")
    try:
        install_package(package)
        print("✅")
    except Exception as e:
        print(f"❌ Error: {e}")

print()
print("✅ Installation complete!")
print()
print("🚀 To run the app:")
print("   streamlit run web_app/app.py")
