#!/usr/bin/env python3

from playwright.sync_api import sync_playwright
import sys
import os
import logging

def get_browser_path():
    """Get the path to the bundled browser for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        # Running in PyInstaller bundle
        return os.path.join(sys._MEIPASS, 'ms-playwright')
    else:
        # Running in normal Python environment
        return None

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    logger.debug(f"Starting webshot with arguments: {sys.argv}")
    
    if len(sys.argv) < 4:
        print("Usage: webshot [URL] [output-file] [WIDTHxHEIGHT] [--delay MILLISECONDS]")
        print("Example: webshot http://example.com example.png 1280x720")
        print("Example: webshot http://example.com example.png 1280x720 --delay 5000")
        logger.error("Invalid number of arguments provided")
        sys.exit(1)
    
    url = sys.argv[1]
    output_path = sys.argv[2]
    dimensions = sys.argv[3]
    
    # Parse optional delay parameter
    delay_ms = 0
    if len(sys.argv) > 4:
        if sys.argv[4] == "--delay" and len(sys.argv) > 5:
            try:
                delay_ms = int(sys.argv[5])
                logger.debug(f"Delay specified: {delay_ms}ms")
            except ValueError:
                print(f"Error: Invalid delay value '{sys.argv[5]}'. Must be a number in milliseconds.")
                sys.exit(1)
    
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
    
    try:
        logger.debug("Initializing Playwright...")
        with sync_playwright() as p:
            # Set browser path if running as PyInstaller bundle
            browser_path = get_browser_path()
            if browser_path:
                logger.debug(f"Setting browser path for PyInstaller bundle: {browser_path}")
                os.environ['PLAYWRIGHT_BROWSERS_PATH'] = browser_path
            else:
                logger.debug("Running in normal Python environment")
            
            logger.debug("Launching Chromium browser...")
            browser = p.chromium.launch(headless=True)
            logger.debug(f"Creating new page with viewport: {width}x{height}")
            page = browser.new_page(viewport={'width': width, 'height': height})
            
            print(f"Loading {url}...")
            logger.info(f"Navigating to URL: {url}")
            page.goto(url, wait_until='networkidle')
            logger.debug("Page loaded successfully, network is idle")
            
            if delay_ms > 0:
                print(f"Waiting {delay_ms}ms after network idle...")
                logger.debug(f"Applying delay of {delay_ms}ms after network idle")
                page.wait_for_timeout(delay_ms)
            
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