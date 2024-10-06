@echo off

REM Check for Python installation
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.
    exit /b
)

REM Check for pip installation
where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo pip is not installed. Please install pip.
    exit /b
)

REM Create a virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r app\requirements.txt

REM Create .env file if it doesn't exist
if not exist "app\.env" (
    echo Creating .env file. Please add your API key.
    echo HUGGINGFACE_API_KEY=your_actual_api_key_here > app\.env
    echo Please edit app\.env to add your actual API key.
) else (
    echo .env file already exists.
)

REM Run the FastAPI application
echo Starting the FastAPI application...
uvicorn app.main:app --reload

