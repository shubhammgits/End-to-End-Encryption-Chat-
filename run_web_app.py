"""
Run this script to start the web-based secure chat application
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages if not already installed"""
    print("Checking and installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        sys.exit(1)

def start_web_server():
    """Start the web server"""
    print("Starting secure chat web application...")
    print("Open your browser and go to http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([sys.executable, "web_server.py"])
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    # Change to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Install requirements
    install_requirements()
    
    # Start the web server
    start_web_server()