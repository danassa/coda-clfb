# coda-clfb
Automatization tool for the Central Library For the Blind, IL

### How to create an app for Windows end user

1. Copy this project to a Windows OS

2. Install Python3 (if missing) and pip install the libraries:
    - python-docx	0.8.10
    - PySimpleGUI	4.18.0
    - pyinstaller
    - pywin32
    
3. Open terminal and cd into /coda-clfb directory

4. Run:
pyi-makespec --onefile  -wF --add-data "default.docx;." --name bookPrepare main.py

5. Edit the file created (bookPrepare.spec) - add at the end:
import shutil
shutil.copyfile('config.ini', '{0}/config.ini'.format(DISTPATH))

6. Run:
pyinstaller --clean bookPrepare.spec


This will create a 'dist' folder containing an EXE file with a config file you can distribute to the end user.