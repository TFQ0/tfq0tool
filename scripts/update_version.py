#!/usr/bin/env python3
"""Script to automatically update version numbers across the project."""

import re
from pathlib import Path
import sys

def update_version(new_version: str):
    """Update version in all relevant files."""
    if not new_version.startswith('v'):
        new_version = f"v{new_version}"
    version = new_version.lstrip('v')  # Remove 'v' prefix for file content

    root = Path(__file__).parent.parent
    files_to_update = {
        root / 'setup.py': r'version="[^"]*"',
        root / 'tfq0tool' / '__init__.py': r'__version__ = "[^"]*"'
    }

    for file_path, pattern in files_to_update.items():
        if not file_path.exists():
            print(f"Warning: {file_path} not found")
            continue

        content = file_path.read_text()
        if 'version' in pattern:
            new_content = re.sub(pattern, f'version="{version}"', content)
        else:
            new_content = re.sub(pattern, f'__version__ = "{version}"', content)
        
        file_path.write_text(new_content)
        print(f"Updated {file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_version.py <new_version>")
        print("Example: python update_version.py 2.1.0")
        sys.exit(1)
    
    update_version(sys.argv[1]) 