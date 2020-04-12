# coda-clfb
Automatization tool for the central library for the blind, IL

Libraries to pip install:

- python-docx	0.8.10
- PySimpleGUI	4.18.0
- pyinstaller


Create app for Windows end user:

- Copy this project to a Windows OS
- Install Python3 (if missing) and the libraries mentioned above
- run the below command from within the /coda directory
pyinstaller --onefile -wF --add-data 'template.docx;.' gui.py

This will create a 'dist' folder containing an .exe file you can distribute to the end-user.