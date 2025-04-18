import subprocess
import os
import platform
import logging
import sys
from textblob import TextBlob

# Create directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists('sub'):
    os.makedirs('sub')

# Set up logging
logging.basicConfig(filename='data/console_output.log', level=logging.DEBUG)

class StreamToLogger:
    def __init__(self, logger, level, orig_stream):
        self.logger = logger
        self.level = level
        self.orig_stream = orig_stream
        self.buf = ''

    def write(self, buf):
        self.buf += buf
        self.orig_stream.write(buf)  # Write to original stream (console)
        self.orig_stream.flush()
        if '\n' in buf:
            self.logger.log(self.level, self.buf.strip())
            self.buf = ''

    def flush(self):
        self.orig_stream.flush()
        if self.buf:
            self.logger.log(self.level, self.buf.strip())
            self.buf = ''

# Save original stdout and stderr
orig_stdout = sys.stdout
orig_stderr = sys.stderr

# Redirect stdout and stderr to logger
logger = logging.getLogger()
sys.stdout = StreamToLogger(logger, logging.INFO, orig_stdout)
sys.stderr = StreamToLogger(logger, logging.ERROR, orig_stderr)

# Helper functions for file operations
class FileHelper:
    @staticmethod
    def empty_file(file_path):
        try:
            with open(file_path, 'w'):  # Open in write mode to clear the file
                pass  # Do nothing, just clear the file
        except Exception as e:
            print(f"Error emptying file {file_path}: {e}")
            logger.error(f"Error emptying file {file_path}: {e}")

    @staticmethod
    def append_to_file(file_path, content):
        try:
            with open(file_path, 'a') as file:
                file.write(content + '\n')
        except Exception as e:
            print(f"Error appending to file {file_path}: {e}")
            logger.error(f"Error appending to file {file_path}: {e}")

    @staticmethod
    def read_file(file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            logger.error(f"Error reading file {file_path}: {e}")
            return ""

    @staticmethod
    def extract_python_code(text):
        start_tag = '```python'
        end_tag = '```'
        start_index = text.find(start_tag)
        if start_index == -1:
            start_tag = '```py'
            start_index = text.find(start_tag)
        if start_index == -1:
            return text  # If no code block found, return the original text

        start_index += len(start_tag)
        end_index = text.find(end_tag, start_index)

        if end_index == -1:
            return text  # If no end tag found, return original text

        return text[start_index:end_index].strip()

def analyze_log_with_sentiment(log_content):
    analysis = TextBlob(log_content)
    polarity = analysis.sentiment.polarity
    subjectivity = analysis.sentiment.subjectivity

    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return f"Sentiment: {sentiment}, Polarity: {polarity}, Subjectivity: {subjectivity}"

# Initialize the FileHelper
file = FileHelper()


def check_node_npm():
    """Checks if Node.js and npm are installed."""
    try:
        subprocess.run(['node', '-v'], check=True, capture_output=True)
        subprocess.run(['npm', '-v'], check=True, capture_output=True)
        logging.info("Node.js and npm are installed.")
        return True
    except FileNotFoundError:
        logging.warning("Node.js or npm not found.")
        return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Error checking Node.js/npm: {e}")
        return False


def install_node_npm():
    """Prompts the user to install Node.js and npm."""
    print("Node.js and npm are required to create a React app.")
    install = input("Do you want to proceed with automatic installation of Node.js? (y/n): ").lower()

    if install == 'y':
        try:
            os_name = platform.system()
            if os_name == "Windows":
                print("Automatic installation of Node.js on Windows is not yet supported by this script. Please install manually and rerun.")
                logging.error("Automatic Node.js installation on Windows not supported.")
                return False
            elif os_name == "Darwin":  # macOS
                try:
                    subprocess.run(['brew', 'install', 'node'], check=True)
                    print("Node.js installed successfully via Homebrew.")
                    logging.info("Node.js installed via Homebrew.")
                    return True
                except FileNotFoundError:
                    print("Homebrew not found. Please install Homebrew first, then rerun this script, or install Node.js manually.")
                    logging.error("Homebrew not found.")
                    return False
                except subprocess.CalledProcessError as e:
                    print(f"Error installing Node.js via Homebrew: {e}")
                    logging.error(f"Error installing Node.js via Homebrew: {e}")
                    return False
            elif os_name == "Linux":
                try:
                    subprocess.run(['sudo', 'apt-get', 'update'], check=True)
                    subprocess.run(['sudo', 'apt-get', 'install', 'nodejs', 'npm'], check=True)
                    print("Node.js and npm installed successfully via apt-get.")
                    logging.info("Node.js installed via apt-get.")
                    return True
                except subprocess.CalledProcessError as e:
                    print(f"Error installing Node.js and npm via apt-get: {e}")
                    logging.error(f"Error installing Node.js via apt-get: {e}")
                    return False
            else:
                print("Unsupported operating system for automatic Node.js installation.")
                logging.error("Unsupported OS for Node.js auto-install.")
                return False

        except Exception as e:
            print(f"An error occurred during Node.js installation: {e}")
            logging.error(f"Error during Node.js installation: {e}")
            return False
    else:
        print("Please install Node.js and npm manually and rerun this script.")
        logging.info("Node.js installation skipped by user.")
        return False


def create_react_app(app_name):
    """Creates a React app using create-react-app."""
    try:
        confirmation = input(f"Do you want to create a React app named '{app_name}' in the current directory? (y/n): ").lower()
        if confirmation == 'y':
            try:
                # Check if npx is available, if not, try installing create-react-app globally
                try:
                    subprocess.run(['npx', 'create-react-app', app_name], check=True)
                except FileNotFoundError:
                    print("npx not found. Attempting to install create-react-app globally.")
                    try:
                        subprocess.run(['npm', 'install', '-g', 'create-react-app'], check=True)
                        subprocess.run(['create-react-app', app_name], check=True)
                    except subprocess.CalledProcessError as e:
                        print(f"Error installing or running create-react-app globally: {e}")
                        logging.error(f"Error installing or running create-react-app globally: {e}")
                        return False

                print(f"React app '{app_name}' created successfully.")
                logging.info(f"React app '{app_name}' created successfully.")
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error creating React app: {e}")
                logging.error(f"Error creating React app: {e}")
                return False
        else:
            print("React app creation cancelled.")
            logging.info("React app creation cancelled by user.")
            return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        logging.error(f"Unexpected error: {e}")
        return False