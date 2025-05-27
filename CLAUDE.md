# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WebShot is a CLI tool that renders web pages to image files and produces standalone executables for Windows, Linux, and macOS. It uses Playwright with embedded Chromium for zero-dependency operation.

## Environment Setup

This project uses Miniconda to create an isolated Python environment named "webshot".

### Initial Setup
```bash
# Linux/macOS
./setup.sh

# Windows
setup.bat
```

The setup script will:
1. Install Miniconda if not present (Linux/macOS only)
2. Create a conda environment named "webshot" with Python 3.11
3. Install all dependencies (playwright, pyinstaller)
4. Install Chromium browser for Playwright

### Activate Environment
```bash
conda activate webshot
```

## Build Commands

### Build Standalone Executables
```bash
# Linux/macOS
./build.sh

# Windows
build.bat
```

### Test Executable
```bash
# Linux/macOS
./dist/webshot http://example.com test.png 1280x720

# Windows
dist\webshot.exe http://example.com test.png 1280x720
```

## Implementation Details

The core implementation uses Playwright's sync API to:
1. Launch a headless Chromium browser
2. Set viewport dimensions from command-line arguments (format: WIDTHxHEIGHT)
3. Navigate to the specified URL
4. Capture a full-page screenshot
5. Save to the specified output file (PNG/JPEG)

Command-line argument order: `webshot [URL] [output-file] [WIDTHxHEIGHT]`

## Key Considerations

- PyInstaller's `--onefile` flag creates single executable bundles
- The executable includes embedded Chromium (approx. 80-88MB depending on platform)
- No additional browser installations required by end users
- Supports custom viewport sizing and full-page captures