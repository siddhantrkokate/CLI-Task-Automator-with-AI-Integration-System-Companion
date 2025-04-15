import logging
import sys
import subprocess
from modules import file, gemini
from textblob import TextBlob
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Re-run the script with admin privileges
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# Rest of your script here

def analyze_log_with_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.1:
        return "Success detected"
    elif polarity < -0.1:
        return "Error detected"
    else:
        return "No clear outcome found"

file.empty_file('data/console_output.log')
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


############################################ code from here

# take input
inputFromUser = str(input("Enter task: "))
logger.info("User Input Task: [" + inputFromUser + "]")

print("Okay! Working and Thinking...")

# gemini to generate detail prompt
promptForGemini1 = "you are a prompt writer and you have to write a prompt which can generate a python code for this task ["+ inputFromUser +"] and you have to metion the reasons because of what the errors can occurs and then you have to do the things automatically on your end like dependacies has to add required one and make sure you have to take permissions from user and make easy for user to see on cmd"
detailPrompt = gemini.generate(inputFromUser)
logger.info(f"Detailed Approach or Prompt For Task: [{detailPrompt}]")

print("Got some idea! Generating enviroment for you!!!!")

# generate
promptToGenerateCode = f"""
You are a thoughtful and interactive coding assistant. A user gives you a high-level instruction (e.g., “set up Node.js”). You must:

Think step-by-step about what needs to be done.

Consider all dependencies, tools, permissions, and user inputs.

Build a complete Python script that:

Runs on the command line (CMD/Terminal).

Uses subprocess, os, or platform as needed.

Asks the user for confirmations or custom inputs.

Handles errors clearly using try/except.

Logs actions in a user-friendly way.

Only performs actions after user confirmation.

Make sure everything works fine handle errors and try to resolve those and write code accordingly.

And should work on PowerShell and use some commands in code which you can fire.


Return only the final Python code — no explanations, no text, no formatting, just code.

User request: "{inputFromUser}"
For help approach: "{detailPrompt}"

And include a 'hello.txt' file which will store all texts showing on console like errors, print, input and more
"""
code = gemini.generate(promptToGenerateCode)
logger.info(f"Code In Python Main Code: [{code}]")
codeNew = str(file.extract_python_code(code))

print("See the result: ")

# save the code in the file for subprocess
# consistent relative path
run_file_path = 'sub/run.py'

# save the code in the file for subprocess
file.empty_file(run_file_path)
file.append_to_file(run_file_path, codeNew)

# run subprocess
result = subprocess.run(['python', run_file_path])

# log the result
# sys.stdout.write(result.stdout)
# sys.stderr.write(result.stderr)

# use textblob and give 
dataFromLogFile = file.read_file('data/console_output.log')
result = analyze_log_with_sentiment(dataFromLogFile)
print(result)



print("Finished running run.py")