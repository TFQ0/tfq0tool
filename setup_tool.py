
from setuptools import setup, find_packages

setup(
    name="TFQ_tool",
    version="1.0",
    description="Extract text from various file formats.",
    packages=find_packages(),
    install_requires=[
        'PyPDF2',
        'python-docx',
        'openpyxl',
    ],
    entry_points={
        'console_scripts': [
            'tfq_tool=TFQ_tool:main',  # Updated to reflect the new name
        ],
    },
)
