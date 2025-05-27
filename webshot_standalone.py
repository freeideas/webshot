#!/usr/bin/env python3
"""
Standalone webshot with automatic browser download
"""

from playwright.sync_api import sync_playwright
import sys
import os
import subprocess

def ensure_browser_installed():
    """Ensure Chromium is installed for Playwright"""
    # Check if running as PyInstaller bundle
    if hasattr(sys, '_MEIPASS'):
        # Use system browsers instead of trying to install them
        # Set the browser path to the system location
        import os
        import platform
        
        if platform.system() == "Windows":
            system_browser_path = os.path.expanduser("~\\AppData\\Local\\ms-playwright")
        else:
            # Linux/macOS
            system_browser_path = os.path.expanduser("~/.cache/ms-playwright")
            
        if os.path.exists(system_browser_path):
            os.environ['PLAYWRIGHT_BROWSERS_PATH'] = system_browser_path
            print("Using system-installed Playwright browsers...")
        else:
            print("Error: Playwright browsers not found in system location.")
            print("Please run 'playwright install chromium' first.")
            sys.exit(1)
        return
    else:
        # Running in normal Python environment - check if browsers are installed
        try:
            # Try to find chromium installation
            with sync_playwright() as p:
                # This will fail if browsers aren't installed
                browser = p.chromium.launch(headless=True)
                browser.close()
        except Exception:
            print("Installing browser components...")
            try:
                subprocess.run([sys.executable, '-m', 'playwright', 'install', 'chromium'],
                             check=True)
                print("Browser installation complete!")
            except subprocess.CalledProcessError as e:
                print(f"Error installing browser: {e}")
                print("Please run: playwright install chromium")
                sys.exit(1)

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

    # Ensure browser is installed
    ensure_browser_installed()

    try:
        with sync_playwright() as p:
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