import cv2
import numpy as np
import os

def remove_background(image_path):
    try:
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            print("Error: Could not load the image.")
            with open('D:\\System Companion\\sub\\data.txt', 'a') as f:
                f.write("Error: Could not load the image.\n")
            return
        
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to segment out the background
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Apply the threshold to the original image to remove the background
        result = cv2.bitwise_and(image, image, mask=thresh)

        # Save the result
        cv2.imwrite('output.png', result)
        print("Background removed successfully.")
        with open('D:\\System Companion\\sub\\data.txt', 'a') as f:
            f.write("Background removed successfully.\n")

    except Exception as e:
        print(f"An error occurred: {e}")
        with open('D:\\System Companion\\sub\\data.txt', 'a') as f:
            f.write(f"An error occurred: {e}\n")

def main():
    with open('D:\\System Companion\\sub\\data.txt', 'a') as f:
        f.write("Program started.\n")
    print("Welcome to the background removal tool.")
    with open('D:\\System Companion\\sub\\data.txt', 'a') as f:
        f.write("Welcome to the background removal tool.\n")
    
    image_path = input("Please enter the path to the image: ")
    with open('D:\\System Companion\\sub\\data.txt', 'a') as f:
        f.write(f"User input: {image_path}\n")
    
    if not os.path.exists(image_path):
        print("Error: The image file does not exist.")
        with open('D:\\System Companion\\sub\\data.txt', 'a') as f:
            f.write("Error: The image file does not exist.\n")
        return
    
    remove_background(image_path)

if __name__ == "__main__":
    main()