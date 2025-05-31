# WebShot CLI Tool

Renders web pages to image files via CLI. Produces standalone executables for Windows/Linux/macOS.

## Features
- Single-file executable output (`webshot.exe` or `webshot`)
- Supports PNG/JPEG output formats
- Headless browser operation
- Custom viewport sizing (e.g., `1024x768`)
- Full-page captures
- Console log capture (JavaScript console.log, console.error, etc.)
- Smart defaults with auto-generated filenames
- Modern command-line interface with optional arguments

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
- Windows: `dist/webshot.exe` (≈56MB)
- Linux: `dist/webshot` (≈56MB) 
- macOS: `dist/webshot` (≈56MB)

Includes embedded Chromium - no additional browser installations required.

## Usage

```bash
webshot <URL> [options]
```

### Command-line Options

- `URL` - The web page to capture (required)
- `--output, -o` - Output image file (default: auto-generated from URL)
- `--size, -s` - Screenshot dimensions as WIDTHxHEIGHT (default: 1280x720)
- `--format, -f` - Output format: png, jpg, jpeg (default: png)
- `--delay, -d` - Delay in milliseconds after page load (default: 0)
- `--console-log, -c` - Capture console logs to text file
- `--console-output` - Custom console log filename
- `--help, -h` - Show help message

### Basic Examples

```bash
# Minimal usage - auto-generates filename
./dist/webshot https://example.com

# Custom output filename and size
./dist/webshot https://example.com --output screenshot.png --size 1920x1080

# Capture with console logging
./dist/webshot https://github.com --console-log

# Custom format and delay
./dist/webshot https://example.com --format jpg --delay 2000
```

### Advanced Examples

```bash
# Full control with all options
./dist/webshot https://example.com \
  --output custom_name.png \
  --size 1600x900 \
  --format png \
  --delay 1000 \
  --console-output logs.txt

# Console logging with auto-generated filenames
./dist/webshot https://github.com --console-log
# Creates: github_com.png and github_com_console.txt
```

### Console Logging

When `--console-log` is used, WebShot captures all JavaScript console output (console.log, console.error, console.warn, etc.) and saves it to a text file. The console log file is automatically named based on the screenshot filename, or you can specify a custom name with `--console-output`.

Example console log format:
```
[2024-01-01 12:00:00.123] LOG: Page loaded successfully
[2024-01-01 12:00:00.456] ERROR: Failed to load resource
[2024-01-01 12:00:00.789] WARN: Deprecated API usage
```

## Development

### Running from source
```bash
conda activate webshot
python webshot.py https://example.com --output test.png --size 1280x720
```

### Project Structure
- `webshot.py` - Main application script
- `webshot_standalone.py` - PyInstaller-compatible version
- `setup.sh` / `setup.bat` - Environment setup scripts
- `build.sh` / `build.bat` - Build scripts for creating executables

## License
MIT