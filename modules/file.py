import os
import re

def append_to_file(file_path, data):
    # Create parent directories if they don't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'a') as file:
        file.write(data)

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def empty_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    open(file_path, 'w').close()

def extract_python_code(text):
    match = re.search(r"```python(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None
