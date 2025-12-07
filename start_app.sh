#!/bin/bash
# Quick start script with API keys pre-configured

export GEMINI_API_KEY="AIzaSyAkdPLKkbQaK7QPujSAAnTuy3Cg7ekbKmM"
export MP_API_KEY="UG6QzjRKyF5GVXa8gwK40TgKztH3neFD"

echo "🚀 Starting Masgent Web App..."
echo "✅ API Keys configured"
echo ""
echo "Open your browser at: http://localhost:8501"
echo ""

streamlit run web_app/app.py
