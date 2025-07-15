#!/usr/bin/env python3
"""
Setup script for Dance Edit Visualizer
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"  Error: {e.stderr}")
        return False

def main():
    print("Dance Edit Visualizer Setup")
    print("=" * 30)
    
    # Check if Python is available
    if not run_command("python --version", "Checking Python installation"):
        print("Python is not available. Please install Python 3.7+ first.")
        return False
    
    # Create virtual environment
    if not run_command("python -m venv venv", "Creating virtual environment"):
        print("Failed to create virtual environment.")
        return False
    
    # Determine the correct activation command based on OS
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Install requirements
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        print("Failed to install dependencies.")
        return False
    
    print("\n" + "=" * 30)
    print("Setup completed successfully!")
    print("\nTo run the visualizer:")
    if os.name == 'nt':  # Windows
        print("1. Activate virtual environment: venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("1. Activate virtual environment: source venv/bin/activate")
    print("2. Run the script: python visualize_edit_preferences.py")
    
    return True

if __name__ == "__main__":
    main() 