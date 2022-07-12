

REM call .venv\Scripts\activate.bat
REM streamlit run main.py %*
@echo off
cmd /k "cd /d .\.venv\Scripts & activate & cd /d ..\..\ & streamlit run main.py"