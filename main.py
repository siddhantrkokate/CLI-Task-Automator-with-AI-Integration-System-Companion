import os
from modules import gemini
from modules import file

# 1
# take input
userTask = str(input("Give me Task: "));
# insert task into the data file
file.empty_file(r'D:\System Companion\data.txt')
file.append_to_file(r"D:\System Companion\data.txt","Task From User: "+userTask)


# 2
# give it the task and write a detailed prompt to find error can occured and say to write just python code
promptToGenerateDetailedPrompt = f"""User Task: [{userTask}]
.You are a prompt writer and you have given the task that user wants to perform on CLI so you have to make detailed prompt
which can contain what user wants to create and also in the code generation or in codes all possible reasons the code may
occures and for those you have to suggest multiple ways as possible as and also that promgram should handle all
dependancies and permission by its own. and you this prompt is going to help another to generate a python code.
always ask user before doing anything like installation ask in which directory
"""
detailedPrompt = gemini.generate_text(promptToGenerateDetailedPrompt)


# 3
# generate python code from detailed input
codeGeneratorPrompt = f"""
User Task: [{userTask}] 
Detailed Prompt Message: [{detailedPrompt}]

You are a Python code writer. Your response should be Python code that completes the user task on the command line interface (CLI). 
Consider the instructions provided in the detailed prompt message.

Requirements:
2. Log all program data, including:
   - User inputs
   - Print statements
   - Exceptions
   - Errors
to the file 'D:\\System Companion\\sub\\data.txt' or 'D:/System Companion/sub/data.txt'.
3. Ensure the code continues running even if exceptions or errors occur.
4. Install all required dependencies automatically without asking for user input.
"""
generatedCode = gemini.generate_text(codeGeneratorPrompt)
refinedCode = str(file.extract_python_code(generatedCode))
# save in run file
file.empty_file(r'D:\System Companion\sub\run.py')
file.append_to_file(r'D:\System Companion\sub\run.py', refinedCode)



# 4
# run that code and save that data dynamically to the data.txt file of responses
import subprocess
file.empty_file(r'D:\System Companion\sub\data.txt')
subprocess.run(["python", "sub/run.py"])

# if error occured the with task and code call gemini and ask for correction.
checkPrompt = f"""
User Task: [{userTask}],
Log Data of Below code after running: [{file.read_file(r'D:\System Companion\sub\data.txt')}],
Code: [{generatedCode}].
You are detector where you as an reponse just return true or false now you have to detect that for given user task the log data of given code after running code 
is saying this task is complted or not if yes then return true and if not then false. Note as an response just true or false nothing extra
"""
checkWithAi = gemini.generate_text(checkPrompt)
checkWithAi = file.process_string(checkWithAi)
print(checkWithAi)

# if not dont
while checkWithAi=="false":
    promptForError = f"""
    User Task: {userTask},
    Code: {generatedCode},
    Log Error File Data: {file.read_file(r'D:\System Companion\sub\data.txt')}.
    You have give user task and code which has error and also given you error log data now you have to rewrite the complete code
    which can solve that error and makesure the code sure perform task completely and as an response just return python complete code
    always ask user before doing anything like installation ask in which directory
    """
    generateCodeError = gemini.generate_text(promptForError)
    refinedCodeError = file.extract_python_code(generateCodeError)
    file.empty_file(r'D:\System Companion\sub\run.py')
    file.append_to_file(r'D:\System Companion\sub\run.py', refinedCodeError)
    import subprocess
    file.empty_file(r'D:\System Companion\sub\data.txt')
    subprocess.run(["python", "sub/run.py"])
    # if error occured the with task and code call gemini and ask for correction.
    checkPrompt = f"""
    User Task: [{userTask}],
    Log Data of Below code after running: [{file.read_file(r'D:\System Companion\sub\data.txt')}],
    Code: [{generatedCode}].
    You are detector where you as an reponse just return true or false now you have to detect that for given user task the log data of given code after running code 
    is saying this task is complted or not if yes then return true and if not then false. Note as an response just true or false nothing extra
    """
    checkWithAi = gemini.generate_text(checkPrompt)
    checkWithAi = file.process_string(checkWithAi)


# Things to rem