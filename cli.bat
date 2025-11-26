@echo off
REM Change directory to the directory this .bat file is in (project root)
cd /d "%~dp0"

REM Make src a top-level import location so `import mse` works
set PYTHONPATH=%cd%\src;%PYTHONPATH%


@REM python src\mse_db\mse_db.py encode test_data\dummy.csv -o seed.json

python src\mse_db\mse_db.py decode mse_seed.json 