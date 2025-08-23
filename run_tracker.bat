@echo off
echo ============================================================
echo CSRR Automated Faculty Media Tracker
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if config file exists
if not exist "config.yaml" (
    echo Creating configuration file...
    python automated_faculty_media_tracker.py --create-config
    echo.
    echo Please edit config.yaml to set your desired date range
    echo Then run this script again.
    pause
    exit /b 0
)

REM Run the tracker
echo Starting faculty media search...
python automated_faculty_media_tracker.py

echo.
echo Search completed! Check the generated files.
pause
