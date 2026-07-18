#!/bin/bash

# Setup virtual environment for gistBackup
# This script creates a venv and installs all required dependencies

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/venv"

echo "📦 Creating virtual environment..."
python3 -m venv "$VENV_DIR"

echo "✓ Virtual environment created at: $VENV_DIR"

# Activate virtual environment
source "$VENV_DIR/bin/activate"

echo "✓ Virtual environment activated"

echo "📥 Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install requests

echo "✓ Dependencies installed successfully"

echo ""
echo "==========================================="
echo "✔ Setup complete!"
echo "==========================================="
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To deactivate, run:"
echo "  deactivate"
echo ""
echo "To run the backup script:"
echo "  python backup.py"
echo ""
