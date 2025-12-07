@echo off
REM Windows installation script for distributed inference framework
REM This script sets up the environment and installs all dependencies

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Distributed Inference Framework Setup
echo Windows Edition
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.12 or later from https://www.python.org
    pause
    exit /b 1
)

echo [1/5] Checking Python version...
python --version

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%

echo.
echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo.
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo [4/5] Upgrading pip...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo Warning: Failed to upgrade pip
)

echo.
echo [5/5] Installing dependencies...
pip install -e .
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo To start the framework, run:
echo   venv\Scripts\activate.bat
echo   exo
echo.
echo For more information, see README.md
echo.

pause
