# CLI Task Automator using AI

## 🧠 Project Overview

This project solves the problem of manually performing routine and repetitive system tasks such as installations, updates, and generating small utility scripts. Using AI, the system allows users to enter a simple natural language prompt through the command line, automatically generates relevant Python code, and runs it in the background. If any errors occur, it retries by regenerating a corrected version until successful.

The goal is to reduce unnecessary clicks and automate everyday tasks using open-source tools and AI.


## 🚀 Features

- Natural language to Python code conversion

- Background execution of tasks

- Auto-correction and re-execution on error

Handles system-level operations like:

Software version checks

Small tool creation (e.g., arithmetic calculator)

Utility execution (e.g., background remover for images)

🛠️ Technologies Used

Python: Core programming language for logic and execution

subprocess & os modules: For running background processes and system-level tasks

Google Gemini 2.0 Flash (Free version): For quick and lightweight AI code generation

Meta Llama 3.3 (70B) via Ola Krutrim Cloud: Main model used for accurate code generation and correction

📦 Requirements

Before running the project, ensure the following are installed:

Python 3.8+

Required Python packages:

pip install google-generativeai

Additional requirements (if needed) can be added to a requirements.txt.

📽️ Demonstration

The project demonstrates three use-cases:

Check PHP Version – A simple version-check script

Arithmetic Calculator – Takes user input and performs basic math

Image Background Remover – Removes background from a given image file and saves output

These are shown in the accompanying video, along with explanations of the code and AI integration.

📚 Learnings

Deepened understanding of subprocess handling and error logging in Python

Learned to set up AI model configurations and deal with the limitations of free-tier AI tools

Gained experience automating end-to-end task flows with fallback correction logic

💡 Future Improvements

Enable direct installation or uninstallation of applications via prompt (e.g., install whatsapp)

Integrate AI with more everyday software to make interactions more intuitive and powerful

📄 Summary

This project demonstrates how natural language and AI can simplify routine system operations, helping bridge the gap between human intent and machine execution without needing clicks or detailed technical commands.

