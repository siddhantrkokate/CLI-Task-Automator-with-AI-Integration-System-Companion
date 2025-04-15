import subprocess
import os
import platform
import sys

def log_to_file(message):
    """Logs a message to hello.txt."""
    try:
        with open("hello.txt", "a") as f:
            f.write(message + "\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")

def run_command(command, shell=False):
    """Runs a command and returns the output and error."""
    try:
        log_to_file(f"Running command: {command}")
        process = subprocess.Popen(
            command,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        stdout, stderr = process.communicate()
        log_to_file(f"Command output: {stdout}")
        if stderr:
            log_to_file(f"Command error: {stderr}")
        return stdout, stderr, process.returncode
    except FileNotFoundError as e:
        log_to_file(f"FileNotFoundError: {e}")
        return None, str(e), 127  # Mimic shell return code for "command not found"
    except Exception as e:
        log_to_file(f"Exception running command: {e}")
        return None, str(e), 1

def check_admin_permissions():
    """Checks if the script is running with administrator privileges."""
    if platform.system() == "Windows":
        try:
            # Check if the user is an administrator
            return os.getuid() == 0
        except AttributeError:
            # os.getuid() doesn't exist on Windows, try another approach
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
    else:
        return os.geteuid() == 0

def update_npm():
    """Updates npm using the recommended method."""
    print("Attempting to update npm using 'npm install -g npm@latest'")
    log_to_file("Attempting to update npm using 'npm install -g npm@latest'")
    stdout, stderr, returncode = run_command(["npm", "install", "-g", "npm@latest"])

    if returncode == 0:
        print("npm updated successfully.")
        log_to_file("npm updated successfully.")
    else:
        print(f"npm update failed with error:\n{stderr}")
        log_to_file(f"npm update failed with error:\n{stderr}")
        return False
    
    # Verify the updated version
    print("Verifying npm version...")
    stdout, stderr, returncode = run_command(["npm", "-v"])
    if returncode == 0:
        print(f"npm version: {stdout.strip()}")
        log_to_file(f"npm version: {stdout.strip()}")
    else:
        print(f"Failed to verify npm version: {stderr}")
        log_to_file(f"Failed to verify npm version: {stderr}")

    return True

def handle_permission_issues():
    """Guides the user on how to resolve permission issues."""
    print("\nIt seems like you might be facing permission issues.")
    log_to_file("\nIt seems like you might be facing permission issues.")
    print("Try the following solutions:")
    log_to_file("Try the following solutions:")
    print("1. Run the script as an administrator (right-click and 'Run as administrator').")
    log_to_file("1. Run the script as an administrator (right-click and 'Run as administrator').")
    print("2. Use Node Version Manager (nvm) to manage Node.js and npm versions (recommended).")
    log_to_file("2. Use Node Version Manager (nvm) to manage Node.js and npm versions (recommended).")
    print("3. Change the ownership of the .npm directory to your user (if you know what you're doing).")
    log_to_file("3. Change the ownership of the .npm directory to your user (if you know what you're doing).")
    print("4. Clear npm cache using 'npm cache clean --force' (use with caution).")
    log_to_file("4. Clear npm cache using 'npm cache clean --force' (use with caution).")
    print("Please try these solutions and run the script again.")
    log_to_file("Please try these solutions and run the script again.")

def main():
    """Main function to update npm."""
    try:
        # Initialize the log file
        with open("hello.txt", "w") as f:
            f.write("Starting npm update script...\n")

        print("This script will update npm to the latest version.")
        log_to_file("This script will update npm to the latest version.")
        
        confirmation = input("Do you want to proceed? (y/n): ").lower()
        log_to_file(f"User confirmation: {confirmation}")

        if confirmation != "y":
            print("Update cancelled.")
            log_to_file("Update cancelled.")
            return

        if not check_admin_permissions() and platform.system() == "Windows":
            print("Warning: It is recommended to run this script with administrator privileges to avoid potential permission issues.")
            log_to_file("Warning: It is recommended to run this script with administrator privileges to avoid potential permission issues.")
            permission_choice = input("Continue without administrator privileges? (y/n): ").lower()
            log_to_file(f"User choice to continue without admin: {permission_choice}")
            if permission_choice != 'y':
                print("Please run the script as administrator.")
                log_to_file("Please run the script as administrator.")
                return
        
        if not update_npm():
            handle_permission_issues()
        

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        log_to_file(f"An unexpected error occurred: {e}")
    finally:
        print("Script finished. Check hello.txt for logs.")
        if 'log_to_file' in locals():
             log_to_file("Script finished.")
        else:
            try:
                with open("hello.txt", "a") as f:
                    f.write("Script finished.\n")
            except:
                pass

if __name__ == "__main__":
    main()