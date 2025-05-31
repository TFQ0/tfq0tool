# TFQ0tool

**A powerful command-line utility for extracting text from various file formats, including PDFs, Word documents, spreadsheets, and code files.**

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI Version](https://img.shields.io/pypi/v/tfq0tool)](https://pypi.org/project/tfq0tool/)

## Features ✨

- 📂 **Multi-format Support**
  - PDF files (including scanned PDFs with OCR)
  - Word documents (DOCX)
  - Excel spreadsheets (XLSX)
  - Text and code files
  - Support for password-protected PDFs

- 🚀 **Advanced Processing**
  - Multi-threaded parallel processing
  - Automatic encoding detection
  - Memory-efficient large file handling
  - Text preprocessing options
  - OCR support for scanned documents

- 📊 **Progress Tracking**
  - Real-time progress bars
  - Detailed success/failure reporting
  - Comprehensive logging system

- 🛡️ **Robust Error Handling**
  - Graceful handling of corrupted files
  - Clear error messages
  - Detailed debug logging

## Installation 💻

### From PyPI (Recommended)




1. Download from pipx

     ```bash
     pipx install tfq0tool

1. Download from pip

   ```bash
   pip install tfq0tool




2. Used by repository
   ```bash
      git clone https://github.com/tfq0/TFQ0tool.git
      cd tfq-tool
      pip install -r requirements.txt
      python tfq-tool.py



3. Usage 🛠️

    ```bash

         "Basic Command"
          tfq0tool [FILES] [OPTIONS] 

         "Single file extraction" 
         tfq0tool document.pdf --output results.txt 

         "Batch processing with 4 threads"
         tfq0tool *.pdf *.docx --threads 4 --output ./extracted_texts


         "Force overwrite existing files"  
         tfq0tool data.xlsx --output output.txt --force



## Options⚙️


- **Flag	Description**
- -o, --output	Output path (file or directory)
- -t, --threads	Thread count (default: 1)
- -v, --verbose	Show detailed processing logs
- -f, --force  	Overwrite files without confirmation

