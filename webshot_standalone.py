#!/usr/bin/env python3
"""
Standalone webshot with automatic browser download
"""

from playwright.sync_api import sync_playwright
import sys
import os
import subprocess
import logging

def ensure_browser_installed():
    """Ensure Chromium is installed for Playwright"""
    logger = logging.getLogger(__name__)
    logger.debug("Checking browser installation...")
    
    # Check if running as PyInstaller bundle
    if hasattr(sys, '_MEIPASS'):
        logger.debug("Running as PyInstaller bundle")
        # Use system browsers instead of trying to install them
        # Set the browser path to the system location
        import os
        import platform
        
        if platform.system() == "Windows":
            system_browser_path = os.path.expanduser("~\\AppData\\Local\\ms-playwright")
        else:
            # Linux/macOS
            system_browser_path = os.path.expanduser("~/.cache/ms-playwright")
        
        logger.debug(f"Checking for system browser at: {system_browser_path}")
            
        if os.path.exists(system_browser_path):
            os.environ['PLAYWRIGHT_BROWSERS_PATH'] = system_browser_path
            print("Using system-installed Playwright browsers...")
            logger.info(f"Using system browsers from: {system_browser_path}")
        else:
            print("Error: Playwright browsers not found in system location.")
            print("Please run 'playwright install chromium' first.")
            logger.error(f"Browser path not found: {system_browser_path}")
            sys.exit(1)
        return
    else:
        logger.debug("Running in normal Python environment")
        # Running in normal Python environment - check if browsers are installed
        try:
            # Try to find chromium installation
            logger.debug("Testing browser availability...")
            with sync_playwright() as p:
                # This will fail if browsers aren't installed
                browser = p.chromium.launch(headless=True)
                browser.close()
            logger.debug("Browser found and working")
        except Exception as e:
            logger.warning(f"Browser not found: {e}")
            print("Installing browser components...")
            try:
                logger.info("Running playwright install chromium...")
                subprocess.run([sys.executable, '-m', 'playwright', 'install', 'chromium'],
                             check=True)
                print("Browser installation complete!")
                logger.info("Browser installation completed successfully")
            except subprocess.CalledProcessError as e:
                print(f"Error installing browser: {e}")
                print("Please run: playwright install chromium")
                logger.error(f"Browser installation failed: {e}")
                sys.exit(1)

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    logger.debug(f"Starting webshot_standalone with arguments: {sys.argv}")
    
    if len(sys.argv) != 4:
        print("Usage: webshot [URL] [output-file] [WIDTHxHEIGHT]")
        print("Example: webshot http://example.com example.png 1280x720")
        logger.error("Invalid number of arguments provided")
        sys.exit(1)

    url = sys.argv[1]
    output_path = sys.argv[2]
    dimensions = sys.argv[3]
    
    logger.debug(f"URL: {url}")
    logger.debug(f"Output path: {output_path}")
    logger.debug(f"Dimensions: {dimensions}")

    try:
        width, height = dimensions.split('x')
        width = int(width)
        height = int(height)
        logger.debug(f"Parsed dimensions: width={width}, height={height}")
    except ValueError:
        print(f"Error: Invalid dimensions format '{dimensions}'. Use WIDTHxHEIGHT (e.g., 1280x720)")
        logger.error(f"Failed to parse dimensions: {dimensions}")
        sys.exit(1)

    output_ext = os.path.splitext(output_path)[1].lower()
    logger.debug(f"Output file extension: {output_ext}")
    if output_ext not in ['.png', '.jpg', '.jpeg']:
        print("Error: Output file must be .png, .jpg, or .jpeg")
        logger.error(f"Invalid output file extension: {output_ext}")
        sys.exit(1)

    # Ensure browser is installed
    logger.info("Ensuring browser is installed...")
    ensure_browser_installed()

    try:
        logger.debug("Initializing Playwright...")
        with sync_playwright() as p:
            logger.debug("Launching Chromium browser...")
            browser = p.chromium.launch(headless=True)
            logger.debug(f"Creating new page with viewport: {width}x{height}")
            page = browser.new_page(viewport={'width': width, 'height': height})

            print(f"Loading {url}...")
            logger.info(f"Navigating to URL: {url}")
            page.goto(url, wait_until='networkidle')
            logger.debug("Page loaded successfully")

            print(f"Capturing screenshot to {output_path}...")
            logger.info(f"Taking screenshot to: {output_path}")
            page.screenshot(path=output_path, full_page=True)
            logger.debug("Screenshot captured successfully")

            logger.debug("Closing browser...")
            browser.close()
            print("Screenshot saved successfully!")
            logger.info("Webshot completed successfully")

    except Exception as e:
        print(f"Error: {str(e)}")
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()