#!/usr/bin/env python3

from playwright.sync_api import sync_playwright
import sys
import os

def get_browser_path():
    """Get the path to the bundled browser for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        # Running in PyInstaller bundle
        return os.path.join(sys._MEIPASS, 'ms-playwright')
    else:
        # Running in normal Python environment
        return None

def main():
    if len(sys.argv) != 4:
        print("Usage: webshot [URL] [output-file] [WIDTHxHEIGHT]")
        print("Example: webshot http://example.com example.png 1280x720")
        sys.exit(1)
    
    url = sys.argv[1]
    output_path = sys.argv[2]
    dimensions = sys.argv[3]
    
    try:
        width, height = dimensions.split('x')
        width = int(width)
        height = int(height)
    except ValueError:
        print(f"Error: Invalid dimensions format '{dimensions}'. Use WIDTHxHEIGHT (e.g., 1280x720)")
        sys.exit(1)
    
    output_ext = os.path.splitext(output_path)[1].lower()
    if output_ext not in ['.png', '.jpg', '.jpeg']:
        print("Error: Output file must be .png, .jpg, or .jpeg")
        sys.exit(1)
    
    try:
        with sync_playwright() as p:
            # Set browser path if running as PyInstaller bundle
            browser_path = get_browser_path()
            if browser_path:
                os.environ['PLAYWRIGHT_BROWSERS_PATH'] = browser_path
            
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': width, 'height': height})
            
            print(f"Loading {url}...")
            page.goto(url, wait_until='networkidle')
            
            print(f"Capturing screenshot to {output_path}...")
            page.screenshot(path=output_path, full_page=True)
            
            browser.close()
            print("Screenshot saved successfully!")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()