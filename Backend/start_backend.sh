#!/bin/bash

echo "==============================================="
echo "  SmartEval AI — Backend Startup"
echo "==============================================="
echo ""

# Go to Backend folder
cd "$(dirname "$0")"

echo "[1/3] Installing required packages..."
pip install flask flask-cors PyMuPDF Pillow google-generativeai
echo ""

echo "[2/3] Checking API key..."
if [ -z "$GEMINI_API_KEY" ]; then
    echo ""
    echo "-----------------------------------------------"
    echo " IMPORTANT: Set your Gemini API key!"
    echo "-----------------------------------------------"
    read -p "Paste your Gemini API key: " GEMINI_API_KEY
    export GEMINI_API_KEY
    echo ""
fi

echo "[3/3] Starting Flask server on http://127.0.0.1:5000"
echo ""
echo " Keep this terminal open while using SmartEval."
echo " Open your browser at:  Frontend/index.html"
echo ""
echo "-----------------------------------------------"

python app.py
