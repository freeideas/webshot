# WebShot CLI Tool

Renders web pages to image files via CLI. Produces standalone executables for Windows/Linux/macOS.

## Features
- Single-file executable output (`webshot.exe` or `webshot`)
- Supports PNG/JPEG output formats
- Headless browser operation
- Custom viewport sizing (e.g., `1024x768`)
- Full-page captures

## Requirements
- Python 3.11+
- Playwright
- PyInstaller

## Installation

### Clone the repository
```bash
git clone https://github.com/yourusername/webshot.git
cd webshot
```

### Set up the environment

#### Linux/macOS
```bash
./setup.sh
```

#### Windows
```batch
setup.bat
```

The setup script will:
1. Install Miniconda if not present (Linux/macOS only)
2. Create a conda environment named "webshot" with Python 3.11
3. Install all dependencies (playwright, pyinstaller)
4. Install Chromium browser for Playwright

## Building Standalone Executables

### Build Commands

#### Linux/macOS
```bash
./build.sh
```

#### Windows
```batch
build.bat
```

### Output
- Windows: `dist/webshot.exe` (≈80MB)
- Linux: `dist/webshot` (≈85MB) 
- macOS: `dist/webshot` (≈88MB)

Includes embedded Chromium - no additional browser installations required.

## Usage
```bash
webshot [URL] [output-file] [WIDTHxHEIGHT]
```

### Examples
```bash
# Capture example.com as a 1280x720 PNG
./dist/webshot http://example.com example.png 1280x720

# Capture a full-page screenshot
./dist/webshot https://github.com github.png 1920x1080
```

## Development

### Running from source
```bash
conda activate webshot
python webshot.py http://example.com test.png 1280x720
```

### Project Structure
- `webshot.py` - Main application script
- `webshot_standalone.py` - PyInstaller-compatible version
- `setup.sh` / `setup.bat` - Environment setup scripts
- `build.sh` / `build.bat` - Build scripts for creating executables

## License
MIT