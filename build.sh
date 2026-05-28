#!/usr/bin/env bash
# Build script for MarkItDown App (Linux/macOS)
set -e

echo "============================================"
echo "  MarkItDown App - Build Script"
echo "============================================"
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    exit 1
fi

# Create virtual environment
echo "[1/4] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install dependencies
echo "[2/4] Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
pip install -e . > /dev/null 2>&1

# Build executable
echo "[3/4] Building executable with PyInstaller..."
pyinstaller build.spec --distpath dist --workpath build_temp --clean -y

# Cleanup
echo "[4/4] Cleaning up..."
rm -rf build_temp

echo
echo "============================================"
echo "  Build complete!"
echo "  Executable: dist/MarkItDown"
echo "============================================"
