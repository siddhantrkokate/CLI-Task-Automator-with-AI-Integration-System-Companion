import os
from modules import gemini
from modules import file

# 1
# take input
userTask = str(input("Give me Task: "));
print("Okay! Thinking about feasability.")
# insert task into the data file
file.empty_file(r'D:\System Companion\data.txt')
file.append_to_file(r"D:\System Companion\data.txt","Task From User: "+userTask)


# 2
# give it the task and write a detailed prompt to find error can occured and say to write just python code
promptToGenerateDetailedPrompt = f"""User Task: [{userTask}]
.You are a detail prompt writer and software thinker you have to think how we can complete following user task on CLI.
And also you have to generate instructions which can help others to write python code.
You have to understand more deeply what user wants to do and just have to do that nothing else and for that you need to metion detail instructions which can help somone to write code.
Instructions included permissions, packages or modules installation, dependancies, possibilities, error handling, exception handling and more.
Use bestest python packages for performing packages if needed do not ask for api keys or anything and if there is any file for results then give it's complete absolute path.
If any dependacies are there it can a module or anything first download it and then remaining code.
"""
detailedPrompt = gemini.generate_text(promptToGenerateDetailedPrompt)
print("It is possible and now writing code for you!")


# 3
# generate python code from detailed input
codeGeneratorPrompt = f"""User Task: [{userTask}] 
Detailed Prompt Message: [{detailedPrompt}].
You are a python code writer as an response you have to write code in python which can perform user task only.
Also you have given Detailed Prompt Message which you have to check and follow for writing code.
Also you have to append data in this file 'D://System Companion//sub//data.txt' which included print statments, inputs from user, errors, exceptions and more and everything.
This code is going to run on CLI so write accordingly.
Download and check all dependecies like python modules are downloaded or not if not then using pip commands download it first and then begin the code.
As an response just return python code nothing else.
And make sure utf-x coding required while appending data to the file give above.
"""
generatedCode = gemini.generate_text(codeGeneratorPrompt)
refinedCode = str(file.extract_python_code(generatedCode))
# # save in run file
print("Running.. Code.")
file.empty_file(r'D:\System Companion\sub\run.py')
file.append_to_file(r'D:\System Companion\sub\run.py', refinedCode)



# # 4
# # run that code and save that data dynamically to the data.txt file of responses
import subprocess
file.empty_file(r'D:\System Companion\sub\data.txt')
subprocess.run(["python", "sub/run.py"])

# # if error occured the with task and code call gemini and ask for correction.
data = str(file.read_file('D:\\System Companion\\sub\\data.txt'));
checkPrompt = f"""
User Task: [{userTask}],
Log Data of Below code after running: [{data}],
Code: [{generatedCode}].
You are detector where you as an reponse just return true or false now you have to detect that for given user task the log data of given code after running code 
is saying this task is complted or not if yes then return true and if not then false. Note as an response just true or false nothing extra
Make sure if nothing is problem in program while running and user exited the code consider it as success and return true.
and user task should 100% completed if not then also return false
"""
checkWithAi = gemini.generate_text(checkPrompt)
checkWithAi = str(file.process_string(checkWithAi))
# print(checkWithAi)
# print("Length : " + str(len(checkWithAi)))
# print(type(checkWithAi))

while True:
    if "true" in checkWithAi:
        print("Code SuccessFully Completed Task! Thank You!")
        break
    else:
        print("Error detected! Rewriting new approach for you!")
        data = str(file.read_file('D:\\System Companion\\sub\\data.txt'));
        promptToWriteCodeOfErrors = f"""
        Task: [{userTask}],
        Privious Code: [{refinedCode}],
        Error in the Privious Code: [{data}].
        You are a python code writer and you have given privious python code and task want to complete using CLI.
        And it has error which has not completed task now you have to write again a complete code which can complete the task.
        Also you have to append data in this file 'D://System Companion//sub//data.txt' which included print statments, inputs from user, errors, exceptions and more and everything.
        If error is coming because of module is not found then download that module using `python -m pip install xx` and then other code there.
        As an resopnse return python code nothing else and in program do not include sub processes like do not create any subprocess in the program.
        """
        codeInError = gemini.generate_text(promptToWriteCodeOfErrors)
        refinedCodeSolvedErros = file.extract_python_code(codeInError)
        print("Running... Code.")
        file.empty_file(r'D:\System Companion\sub\run.py')
        # file.empty_file(r'D:\System Companion\sub\data.txt')
        file.append_to_file(r'D:\System Companion\sub\run.py', refinedCodeSolvedErros)

        import subprocess
        subprocess.run(["python", "sub/run.py"])

        checkAgainPrompt = f"""
        User Task: [{userTask}],
        Log Data of Below code after running: [{file.read_file(r'D:\System Companion\sub\data.txt')}],
        Code: [{refinedCodeSolvedErros}].
        You are detector where you as an reponse just return true or false now you have to detect that for given user task the log data of given code after running code 
        is saying this task is complted or not if yes then return true and if not then false. Note as an response just true or false nothing extra
        and user task should 100% completed if not then also return false
        """
        checkWithAi = gemini.generate_text(checkAgainPrompt)
        checkWithAi = str(file.process_string(checkWithAi))

        refinedCode = refinedCodeSolvedErros



# # if not dont
# while checkWithAi.strip().lower() != "true":
#     
#     # if error occured the with task and code call gemini and ask for correction.
#     checkPrompt = f"""
#     User Task: [{userTask}],
#     Log Data of Below code after running: [{file.read_file(r'D:\System Companion\sub\data.txt')}],
#     Code: [{generatedCode}].
#     You are detector where you as an reponse just return true or false now you have to detect that for given user task the log data of given code after running code 
#     is saying this task is complted or not if yes then return true and if not then false. Note as an response just true or false nothing extra
#     and user task should 100% completed if not then also return false
#     """
#     checkWithAi = gemini.generate_text(checkPrompt)
#     checkWithAi = str(file.process_string(checkWithAi))


# # Things to rem