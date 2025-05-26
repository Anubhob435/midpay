import os
import sys

# Add the parent directory to the Python path so we can import from app.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Run initialization if needed
try:
    import init_app
except ImportError:
    pass  # init_app.py might not exist or might fail, that's okay

from app import app

# This is the entry point for Vercel
# It imports the Flask app from app.py

# Export the app for Vercel
application = app
