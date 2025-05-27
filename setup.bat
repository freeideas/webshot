@echo off
echo Setting up WebShot with Miniconda environment...

:: Check if conda is installed
where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Miniconda not found. Please install Miniconda from:
    echo https://docs.conda.io/en/latest/miniconda.html
    echo.
    echo After installation, run this script again.
    pause
    exit /b 1
)

:: Create webshot environment
echo Creating 'webshot' conda environment with Python 3.11...
call conda create -n webshot python=3.11 -y

:: Activate environment
echo Activating 'webshot' environment...
call conda activate webshot

:: Install Python dependencies
echo Installing Python packages...
pip install -r requirements.txt

:: Install Chromium for Playwright
echo Installing Chromium browser...
playwright install chromium
playwright install-deps

echo.
echo Setup complete!
echo.
echo To use WebShot:
echo 1. Activate the environment: conda activate webshot
echo 2. Run: python webshot.py [URL] [output-file] [WIDTHxHEIGHT]
echo.
echo Example: python webshot.py http://example.com example.png 1280x720
pause