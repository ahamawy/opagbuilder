#!/usr/bin/env python3
"""
Script to set up the Word template for the Operating Agreement Builder.
This will help users properly configure their ETFIG TWO template.
"""

import os
import sys
import shutil
from pathlib import Path

def main():
    # Get the path to the templates directory
    script_dir = Path(__file__).parent
    templates_dir = script_dir / "templates"
    
    # Create templates directory if it doesn't exist
    templates_dir.mkdir(exist_ok=True)
    
    print("Operating Agreement Template Setup")
    print("=" * 40)
    print()
    
    # Check if user provided a template file
    if len(sys.argv) > 1:
        template_path = Path(sys.argv[1])
        
        if not template_path.exists():
            print(f"Error: Template file not found: {template_path}")
            sys.exit(1)
        
        if not template_path.suffix.lower() == '.docx':
            print("Error: Template must be a .docx file")
            sys.exit(1)
        
        # Copy the template
        destination = templates_dir / "etfig_two.docx"
        shutil.copy2(template_path, destination)
        
        print(f"✓ Template copied successfully to: {destination}")
        print()
        print("The template is now available in the app as 'etfig_two'")
        
    else:
        print("Usage: python setup_template.py <path_to_your_template.docx>")
        print()
        print("Example:")
        print("  python setup_template.py ~/Downloads/ETFIG_TWO_Operating_Agreement.docx")
        print()
        print("Your template file location:")
        print("  /Users/ahmedelhamawy/Downloads/ETFIG_TWO_Operating Agreement_Final_250312.docx")
        print()
        print("To set up your template, run:")
        print('  python setup_template.py "/Users/ahmedelhamawy/Downloads/ETFIG_TWO_Operating Agreement_Final_250312.docx"')

if __name__ == "__main__":
    main()