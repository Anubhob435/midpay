"""
Initialize application requirements before startup
This script ensures all necessary directories and files exist
"""

import os
import json

# Ensure flask_session directory exists for session storage
session_dir = 'flask_session'
if not os.path.exists(session_dir):
    os.makedirs(session_dir)
    print(f"Created {session_dir} directory for session storage")

# Create a placeholder file to ensure the directory is included in Git
placeholder_path = os.path.join(session_dir, '.keep')
if not os.path.exists(placeholder_path):
    with open(placeholder_path, 'w') as f:
        f.write("# This directory is used for Flask session storage\n")
    print(f"Created placeholder file in {session_dir}")

# Ensure static directories exist
static_dirs = ['static/css', 'static/js', 'static/images']
for directory in static_dirs:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created {directory} directory")

# Create empty validkeys.json file if it doesn't exist
validkeys_path = 'validkeys.json'
if not os.path.exists(validkeys_path):
    with open(validkeys_path, 'w') as f:
        json.dump({}, f)
    print(f"Created empty {validkeys_path} file")

print("Initialization complete!")
