@echo off
REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH. Please install Python.
    exit /b 1
)

REM Create a virtual environment in the "venv" folder
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment.
    exit /b 1
)

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment.
    exit /b 1
)

REM Install the packages in requirements.txt
if not exist requirements.txt (
    echo requirements.txt not found. Please make sure it exists in the current directory.
    exit /b 1
)
echo Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements. Check your requirements.txt file.
    exit /b 1
)

echo Installation success.
pause
