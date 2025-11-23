@echo off
REM Change directory to the directory this .bat file is in (project root)
cd /d "%~dp0"

REM Make src a top-level import location so `import mse` works
set PYTHONPATH=%cd%\src;%PYTHONPATH%

REM Run the module
python -m modules.programming.examples.python.quiz.Build
@REM python -m modules.personalization.Personalization
pause
