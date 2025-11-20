#!/bin/bash
# Setup script for OCR text extraction

echo "Setting up OCR text extraction environment..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Install Tesseract OCR engine
echo "Installing Tesseract OCR engine..."
if command -v apt-get &> /dev/null; then
    # Debian/Ubuntu
    sudo apt-get update
    sudo apt-get install -y tesseract-ocr tesseract-ocr-eng
elif command -v yum &> /dev/null; then
    # CentOS/RHEL
    sudo yum install -y tesseract tesseract-langpack-eng
elif command -v brew &> /dev/null; then
    # macOS with Homebrew
    brew install tesseract
else
    echo "Please install Tesseract OCR manually for your system:"
    echo "- Ubuntu/Debian: sudo apt-get install tesseract-ocr"
    echo "- CentOS/RHEL: sudo yum install tesseract"
    echo "- macOS: brew install tesseract"
    echo "- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo "Setup complete!"
echo ""
echo "Usage examples:"
echo "  python3 extract_text.py --help"
echo "  python3 extract_text.py --single 1/f1_png.rf.029996f845fcea2f1e17351ad88ed765.jpg"
echo "  python3 extract_text.py --batch --format console"
echo "  python3 extract_text.py --batch --format json --output-file results.json"