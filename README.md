# CMSC-124-Project

## How to Run the LOLCode Interpreter

Welcome to LOLCode! It is an esoteric programming language with keywords that sound much like text and meme language, but correspond to actual programming keywords.
Here is how to run this LOLCode Interpreter.

### 1) Download all the necessary files.
#### a. Python
Since this interpreter is created using Python, make sure you have Python installed on your device. You can get it from the official Python Website.
#### b. Pip
Usually, Pip (the Python package manager) comes with the download package for Python. You can check if Pip is installed by typing "pip -V" on your terminal.
#### c. Tkinter
Pip can be used to install Tkinter. It is arguably the simplest Python tool used for creating interfaces. To install Tkinter, type "pip install tk" on your terminal.

### 2) Setup your working analyzer.
The analyzer has two main files: one for the lexical analysis and the other for the syntax analysis. For them to show up on Tkinter, there is a GUI Python file, where both main files and Tkinter are imported. Set your location on the terminal to the source code folder, where all the Python files and the LOLCode files are.

### 3) Run LOLCode.
Once you are in the correct directory, run the GUI file on Python. In this version, it will be run as "python3 gui.py" since we should be on Python 3, the latest version.
In the analyzer, you should see a space for LOLCode, a lexical table, a symbol table, and a console where the output will be displayed. You can also find two buttons: one to browse for LOLCode files and another to run the analyzer.
To use it, click Browse. It should lead you to a pop-up window set inside the source code directory. The LOLCode files are in the testcases folder, so you can click on that folder and select a LOLCode file of your choice. Once selected, the LOLCode code will show up on the working space. You can run it to show the lexemes on the lexical folder, the variables and corresponding values on the symbol table, and the output on the console. If necessary, a pop-up window will appear, asking you for the values of the variables (you can be aware of that if you see a GIMMEH keyword on the LOLCode code, which stands for input() in Python), before the output and variable values show up.

## Enjoy working with LOLCode!
