# bhang_bhsa

Image Text Extraction Repository using OCR (Optical Character Recognition)

This repository contains 100 image files (academic documents, markscards, etc.) and provides a comprehensive Python script to extract text from these images using OCR technology.

## 📁 Repository Structure

```
bhang_bhsa/
├── 1/              # Directory containing 63 images (various academic documents)
├── 2/              # Directory containing 37 images (markscards and certificates)
├── extract_text.py # Main OCR text extraction script
├── requirements.txt # Python dependencies
├── setup.sh        # Setup script for installing dependencies
└── README.md       # This file
```

## 🚀 Quick Start

### 1. Setup and Installation

#### Automatic Setup (Linux/macOS)
```bash
chmod +x setup.sh
./setup.sh
```

#### Manual Setup

**Install Tesseract OCR Engine:**
- Ubuntu/Debian: `sudo apt-get install tesseract-ocr tesseract-ocr-eng`
- CentOS/RHEL: `sudo yum install tesseract tesseract-langpack-eng`
- macOS: `brew install tesseract`
- Windows: Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

**Install Python Dependencies:**
```bash
pip3 install -r requirements.txt
```

### 2. Usage Examples

#### Extract Text from a Single Image
```bash
python3 extract_text.py --single "1/f1_png.rf.029996f845fcea2f1e17351ad88ed765.jpg"
```

#### Batch Process All Images (Console Output)
```bash
python3 extract_text.py --batch --format console
```

#### Save Results as JSON
```bash
python3 extract_text.py --batch --format json --output-file "results.json"
```

#### Save Individual Text Files
```bash
python3 extract_text.py --batch --format text --output-dir "extracted_text/"
```

#### Process Specific Directory
```bash
python3 extract_text.py --batch --source-dir "1/" --format console
```

## 📖 Script Features

- **Multiple Input Modes**: Single image or batch processing
- **Multiple Output Formats**: 
  - Console output for quick viewing
  - JSON format for structured data
  - Individual text files for each image
- **Comprehensive Error Handling**: Graceful handling of corrupted or unreadable images
- **Progress Tracking**: Real-time progress updates during batch processing
- **Configurable OCR Settings**: Customizable Tesseract configuration
- **Supported Image Formats**: JPG, JPEG, PNG, TIFF, BMP, GIF

## 🔧 Command Line Options

```
python3 extract_text.py [options]

Required (choose one):
  --single IMAGE_PATH    Extract text from a single image
  --batch               Extract text from multiple images

Optional:
  --source-dir DIR      Source directory for batch processing (default: current directory)
  --format FORMAT       Output format: console, json, text (default: console)
  --output-file FILE    Output file path (for json format)
  --output-dir DIR      Output directory path (for text format)
  --tesseract-config    Tesseract configuration string (default: --oem 3 --psm 6)
  --verbose, -v         Enable verbose logging
  --help, -h           Show help message
```

## 📊 Sample Output

### Console Format
```
==================================================
File: f1_png.rf.029996f845fcea2f1e17351ad88ed765.jpg
==================================================
*GRADE CARD 00557497
B.E. Computer Science & Engineering August 2020
BINA INSTITUTE OF TECHNOLOGY, BANGALORE
...extracted text content...
```

### JSON Format
```json
[
  {
    "file_path": "1/f1_png.rf.029996f845fcea2f1e17351ad88ed765.jpg",
    "file_name": "f1_png.rf.029996f845fcea2f1e17351ad88ed765.jpg",
    "success": true,
    "text": "*GRADE CARD 00557497\nB.E. Computer Science & Engineering...",
    "error": null,
    "image_size": [640, 640],
    "image_mode": "RGB"
  }
]
```

## 🎯 Use Cases

- **Academic Document Processing**: Extract text from markscards, certificates, transcripts
- **Document Digitization**: Convert image-based documents to searchable text
- **Data Mining**: Extract structured information from scanned documents
- **Archive Processing**: Batch process large collections of document images

## 🔍 Technical Details

- **OCR Engine**: Tesseract 4.0+ with configurable parameters
- **Image Processing**: PIL/Pillow for image handling and preprocessing
- **Text Extraction**: Advanced OCR with customizable page segmentation modes
- **Error Recovery**: Robust error handling for various image quality issues

## 📋 Dependencies

- Python 3.6+
- pytesseract >= 0.3.10
- Pillow >= 10.0.0
- Tesseract OCR engine

## 🐛 Troubleshooting

### Common Issues

1. **"tesseract is not installed" error**
   - Install Tesseract OCR engine for your operating system
   - Ensure tesseract is in your system PATH

2. **"No text found" for clear images**
   - Try different tesseract configurations: `--tesseract-config "--oem 1 --psm 3"`
   - Check if image contains actual text content

3. **Poor text quality**
   - Images may have low resolution or poor quality
   - Consider image preprocessing for better results

### Getting Help
```bash
python3 extract_text.py --help
```

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.