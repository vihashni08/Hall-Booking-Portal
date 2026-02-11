import sys
import os

# Add the root directory to the sys.path so we can import from 'backend'
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.app import create_app

app = create_app()
