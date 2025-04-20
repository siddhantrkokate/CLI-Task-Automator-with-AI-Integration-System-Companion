# Import required libraries
import os
import sys
import pip
from rembg.bg import remove

# Function to install required packages
def install_packages():
    try:
        # Install rembg package
        pip.main(['install', 'rembg'])
        with open('D://System Companion//sub//data.txt', 'a', encoding='utf-8') as f:
            f.write("rembg package installed successfully\n")
    except Exception as e:
        with open('D://System Companion//sub//data.txt', 'a', encoding='utf-8') as f:
            f.write(f"Error installing rembg package: {e}\n")

# Function to remove background from image
def remove_background(input_path, output_path):
    try:
        with open(input_path, 'rb') as i:
            result = remove(i.read())
            with open(output_path, 'wb') as o:
                o.write(result)
        with open('D://System Companion//sub//data.txt', 'a', encoding='utf-8') as f:
            f.write(f"Background removed from {input_path} and saved to {output_path}\n")
    except Exception as e:
        with open('D://System Companion//sub//data.txt', 'a', encoding='utf-8') as f:
            f.write(f"Error removing background: {e}\n")

# Main function
def main():
    with open('D://System Companion//sub//data.txt', 'a', encoding='utf-8') as f:
        f.write("Program started\n")
    
    # Check if rembg package is installed
    try:
        import rembg
        with open('D://System Companion//sub//data.txt', 'a', encoding='utf-8') as f:
            f.write("rembg package is already installed\n")
    except ImportError:
        install_packages()

    # Get input and output paths from user
    input_path = input("Enter the path to the input image: ")
    output_path = input("Enter the path to the output image: ")
    with open('D://System Companion//sub//data.txt', 'a', encoding='utf-8') as f:
        f.write(f"Input path: {input_path}\n")
        f.write(f"Output path: {output_path}\n")

    # Remove background from image
    remove_background(input_path, output_path)

    with open('D://System Companion//sub//data.txt', 'a', encoding='utf-8') as f:
        f.write("Program finished\n")

if __name__ == "__main__":
    main()