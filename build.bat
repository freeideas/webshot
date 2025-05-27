@echo off
echo Building WebShot standalone executable for Windows...

:: Activate conda environment
call conda activate webshot

if %ERRORLEVEL% NEQ 0 (
    echo Error: Could not activate 'webshot' environment
    echo Please run setup.bat first
    pause
    exit /b 1
)

:: Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

:: Get playwright path
for /f "delims=" %%i in ('python -c "import playwright; print(playwright.__path__[0])"') do set PLAYWRIGHT_PATH=%%i

:: Build with PyInstaller
pyinstaller --onefile ^
    --name webshot.exe ^
    --add-data "%PLAYWRIGHT_PATH%\driver;playwright\driver" ^
    --hidden-import playwright.sync_api ^
    --hidden-import playwright.async_api ^
    webshot_standalone.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Build successful!
    echo Executable created: dist\webshot.exe
    echo.
    echo Test with: dist\webshot.exe http://example.com test.png 1280x720
) else (
    echo Build failed!
    pause
    exit /b 1
)

pause