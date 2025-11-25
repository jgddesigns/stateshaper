@echo off
REM Change directory to the directory this .bat file is in (project root)
cd /d "%~dp0"

REM Make src a top-level import location so `import mse` works
set PYTHONPATH=%cd%\src;%PYTHONPATH%

REM Run the module
@REM python -m modules.programming.examples.python.quiz.Build
@REM python -m modules.personalization.Personalization
@REM @REM python -m modules.databases.examples.DynamoDB
@REM @REM python -m modules.databases.examples.Firebase
@REM python -m modules.databases.examples.MySQL
@REM python -m modules.databases.examples.MongoDB
streamlit run "E:\coding\mse project\morphic_semantic_engine\streamlit_app.py"
pause
