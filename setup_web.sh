#!/bin/bash
# Quick setup script for Masgent Web App

echo "🔧 Installing Masgent dependencies..."
pip install -e . --quiet

echo "🌐 Installing web app dependencies..."
pip install streamlit stmol py3Dmol plotly --quiet

echo "✅ Setup complete!"
echo ""
echo "🚀 To run the app:"
echo "   streamlit run web_app/app.py"
