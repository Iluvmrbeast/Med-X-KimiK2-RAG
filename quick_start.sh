#!/bin/bash
# MedeX Quick Start Script
# Quick setup and launch for local testing

echo "🏥 MedeX - Quick Start Script"
echo "=============================="
echo ""

# Check if we're in the right directory
if [ ! -f "streamlit_app.py" ]; then
    echo "❌ Error: streamlit_app.py not found"
    echo "Please run this script from the MedeX-main directory"
    exit 1
fi

# Check Python version
echo "1️⃣ Checking Python version..."
python3 --version || { echo "❌ Python 3 not found"; exit 1; }
echo "✅ Python found"
echo ""

# Check if virtual environment exists
if [ ! -d "medex_venv" ]; then
    echo "2️⃣ Creating virtual environment..."
    python3 -m venv medex_venv
    echo "✅ Virtual environment created"
else
    echo "2️⃣ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "3️⃣ Activating virtual environment..."
source medex_venv/bin/activate || { echo "❌ Failed to activate venv"; exit 1; }
echo "✅ Virtual environment activated"
echo ""

# Install/Update dependencies
echo "4️⃣ Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✅ Dependencies installed"
echo ""

# Run pre-deployment tests
echo "5️⃣ Running pre-deployment tests..."
python test_deployment.py
echo ""

# Ask if user wants to continue
read -p "Continue to launch Streamlit? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Exiting. Run 'streamlit run streamlit_app.py' when ready."
    exit 0
fi

# Launch Streamlit
echo "6️⃣ Launching MedeX Streamlit Interface..."
echo ""
echo "🌐 Opening browser at http://localhost:8501"
echo "⌨️  Press Ctrl+C to stop"
echo ""

streamlit run streamlit_app.py

# Cleanup message
echo ""
echo "👋 MedeX stopped. Goodbye!"
