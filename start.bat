@echo off
chcp 65001 >nul
echo.
echo ========================================
echo Starting Super Job Wizard v3.0
echo ========================================
echo.
echo Starting the most powerful job tool...
echo.

REM Check virtual environment
if not exist "super_job_env_313" (
    echo Virtual environment not found, creating...
    python -m venv super_job_env_313
    echo Virtual environment created successfully
)

REM Activate virtual environment
echo Activating virtual environment...
call super_job_env_313\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt >nul 2>&1

echo.
echo ========================================
echo Super Job Wizard Started!
echo ========================================
echo.
echo Global data support - 150+ countries PPP data
echo AI intelligent analysis - Resume optimization, salary prediction
echo Big data support - Company intelligence, industry reports
echo Platform integration - LinkedIn analysis, multi-platform tracking
echo Smart decision - Decision tree analysis, risk assessment
echo Job value calculation - Real hourly wage, comprehensive evaluation
echo Job assistant - Resume analysis, salary negotiation
echo Water quality interview - Professional PPT, question bank, strategy
echo.
echo Ready to conquer the global job market!
echo.
echo ========================================

REM Start Super Job Wizard
python src\super_job_wizard.py

echo.
echo Super Job Wizard has stopped running
pause