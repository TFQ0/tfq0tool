#!/usr/bin/env python3

import os
from PyPDF2 import PdfReader
from docx import Document
import openpyxl

def extract_text_from_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == '.txt':
        return extract_text_from_txt(file_path)
    elif file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_path)
    elif file_extension == '.xlsx':
        return extract_text_from_xlsx(file_path)
    elif file_extension in ['.py', '.java', '.js', '.html', '.css', '.json', '.xml', '.c', '.cpp']:
        return extract_text_from_code(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_path):
    text = ""
    doc = Document(file_path)
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_xlsx(file_path):
    text = ""
    workbook = openpyxl.load_workbook(file_path)
    for sheet in workbook.sheetnames:
        worksheet = workbook[sheet]
        for row in worksheet.iter_rows(values_only=True):
            row_text = " ".join([str(cell) if cell is not None else '' for cell in row])
            text += row_text + "\n"
    return text

def extract_text_from_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="TFQ Tool: A simple text extraction tool for various file formats."
    )
    parser.add_argument("file", help="Path to the file to extract text from.")
    parser.add_argument("-o", "--output", help="Optional path to save the extracted text.")

    args = parser.parse_args()
    file_path = args.file
    output_path = args.output

    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return

    try:
        extracted_text = extract_text_from_file(file_path)
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(extracted_text)
            print(f"✅ Text successfully extracted and saved to '{output_path}'.")
        else:
            print("✅ Extracted Text:")
            print("=" * 40)
            print(extracted_text)
            print("=" * 40)
    except ValueError as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
