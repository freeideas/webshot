#!/bin/bash

echo "Building WebShot standalone executable..."

# Activate conda environment
source ~/miniconda3/bin/activate webshot

if [ $? -ne 0 ]; then
    echo "Error: Could not activate 'webshot' environment"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OUTPUT_NAME="webshot"
    echo "Building for Linux..."
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OUTPUT_NAME="webshot-mac"
    echo "Building for macOS..."
else
    echo "Unsupported OS for this script. Use build.bat for Windows."
    exit 1
fi

# Clean previous builds
rm -rf build dist *.spec

# Build with PyInstaller
echo "Note: The standalone executable will require Playwright browsers to be installed on the target system."
echo "Users can install them with: playwright install chromium"
echo ""

pyinstaller --onefile \
    --name $OUTPUT_NAME \
    --add-data "$(python -c 'import playwright; print(playwright.__path__[0])')/driver:playwright/driver" \
    --hidden-import playwright.sync_api \
    --hidden-import playwright.async_api \
    webshot_standalone.py

if [ $? -eq 0 ]; then
    echo ""
    echo "Build successful!"
    echo "Executable created: dist/$OUTPUT_NAME"
    echo ""
    echo "Test with: ./dist/$OUTPUT_NAME http://example.com test.png 1280x720"
else
    echo "Build failed!"
    exit 1
fi