# WebShot Standalone Executable

## Build Results

Successfully created a standalone executable for WebShot!

### Executable Details
- **Location**: `dist/webshot` (Linux)
- **Size**: ~56MB (without bundled browser)
- **Python**: Not required on target system
- **Dependencies**: Chromium browser must be installed

### Important Note on Browser Dependencies

The standalone executable requires Playwright's Chromium browser to be installed on the target system. This is because bundling the entire Chromium browser (150MB+) would make the executable impractically large.

### Usage on Target System

1. **First-time setup** (one-time only):
   ```bash
   # Install Playwright and browser
   pip install playwright
   playwright install chromium
   ```

2. **Run the executable**:
   ```bash
   ./webshot https://example.com screenshot.png 1280x720
   ```

### Alternative: Full Bundle

If you need a truly standalone executable without any dependencies, consider:
1. Using a different screenshot library (like Selenium with a system Chrome)
2. Creating a Docker container with all dependencies
3. Using a web service API for screenshots

### Distribution

The executable at `dist/webshot` can be distributed to any Linux x86_64 system. Users will need to install Playwright's Chromium browser as shown above.

### Testing Status

✅ Python script works correctly in conda environment
✅ Standalone executable builds successfully  
✅ Executable runs (requires Playwright browser installation)
⚠️ Full browser bundling not implemented due to size constraints