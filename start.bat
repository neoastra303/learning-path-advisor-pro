@echo off
REM Windows batch script to run Learning Path Advisor

echo ============================================================
echo   Learning Path Advisor - Quick Start
echo ============================================================
echo.

if not exist "venv\" (
    echo Virtual environment not found. Running setup...
    python setup.py
    if errorlevel 1 (
        echo Setup failed. Please check the errors above.
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Starting server...
python run.py

pause
