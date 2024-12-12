"""
Entry point for the EECP GESYS application.
"""

import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.main import App

if __name__ == "__main__":
    app = App()
    app.run()
