@echo off
REM Quick Setup Script for MCP-Enhanced BA CrewAI (Windows)
REM This script helps you set up the environment

echo ================================================
echo   MCP-Enhanced BA CrewAI - Quick Setup
echo ================================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Please install Python 3.10+ from python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python %PYTHON_VERSION% detected

echo.
echo Installing dependencies...
pip install crewai>=0.28.0 anthropic>=0.18.0 python-dotenv>=1.0.0 pyyaml>=6.0 pydantic>=2.0.0

if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully

echo.
echo Setting up environment variables...
if not exist .env (
    copy .env.template .env
    echo Created .env file from template
    echo.
    echo IMPORTANT: Edit .env and add your ANTHROPIC_API_KEY
    echo Get your key from: https://console.anthropic.com/
    echo.
) else (
    echo .env file already exists, skipping...
)

echo.
echo ================================================
echo           Setup Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Edit .env and add your ANTHROPIC_API_KEY
echo 2. Run: python main_updated.py
echo 3. Try the sample: sample_compliance_requirement.txt
echo.
echo For more details, see: MCP_INTEGRATION_GUIDE.md
echo.
pause
