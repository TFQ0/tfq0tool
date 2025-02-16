
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tfq-tool",            
    version="2.0.0",            
    author="Your Name",
    author_email="your@email.com",
    description="Extract text from PDFs, Word docs, Excel sheets, and code files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/TFQ_tool",
    packages=find_packages(),
    install_requires=[
        "PyPDF2",
        "python-docx",
        "openpyxl",
        "pdfminer.six",
        
    ],
    entry_points={
        "console_scripts": [
            "tfq_tool=TFQ_tool.tfq_tool:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)