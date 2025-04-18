import os
import subprocess
from pathlib import Path
import logging
import argparse
import sys

# Set up logging
logging.basicConfig(filename='D:/System Companion/sub/data.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def open_in_default(path):
    try:
        # Function to open file/directory in default application
        if os.name == 'nt':  # Windows
            os.startfile(path)
        elif os.name == 'posix':  # Linux, macOS
            if sys.platform == 'darwin':  # macOS
                subprocess.call(('open', path))
            else:  # Linux
                subprocess.call(('xdg-open', path))
        logging.info(f"Opened {path} in default application")
    except Exception as e:
        logging.error(f"Error opening {path} in default application: {e}")

def open_in_studio(path, studio_app):
    try:
        # Function to open file in a studio application
        if studio_app == 'Visual Studio Code':
            subprocess.call((f'code', path))
        elif studio_app == 'IntelliJ IDEA':
            subprocess.call((f'idea', path))
        elif studio_app == 'PyCharm':
            subprocess.call((f'pycharm', path))
        logging.info(f"Opened {path} in {studio_app}")
    except Exception as e:
        logging.error(f"Error opening {path} in {studio_app}: {e}")

def install_dependencies():
    try:
        # Function to check and install necessary dependencies
        # Install required dependencies automatically
        subprocess.call((sys.executable, '-m', 'pip', 'install', 'argparse'))
        logging.info("Installed required dependencies")
    except Exception as e:
        logging.error(f"Error installing dependencies: {e}")

def handle_permissions():
    try:
        # Function to handle permissions issues
        # Request elevated privileges if necessary
        if os.name == 'nt':  # Windows
            subprocess.call(('powershell', '-Command', 'Start-Process', 'python', '-Verb', 'RunAs'))
        elif os.name == 'posix':  # Linux, macOS
            subprocess.call(('sudo', 'python'))
        logging.info("Handled permissions issues")
    except Exception as e:
        logging.error(f"Error handling permissions: {e}")

def main():
    try:
        # Main function to orchestrate the script's functionality
        parser = argparse.ArgumentParser(description='Open a file or directory in either an open or studio environment')
        parser.add_argument('--path', help='Path to the file or directory to be opened')
        parser.add_argument('--env', choices=['open', 'studio'], help='Environment in which to open the file or directory')
        args = parser.parse_args()
        
        logging.info(f"User input: {args}")
        
        if args.env == 'open':
            open_in_default(args.path)
        elif args.env == 'studio':
            # Provide a list of supported studio applications
            studio_apps = ['Visual Studio Code', 'IntelliJ IDEA', 'PyCharm']
            # Choose a default studio application
            studio_app = studio_apps[0]
            open_in_studio(args.path, studio_app)
        
        logging.info("Program execution completed")
    except Exception as e:
        logging.error(f"Error in main function: {e}")

if __name__ == "__main__":
    install_dependencies()
    main()