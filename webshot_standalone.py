#!/usr/bin/env python3
"""
Standalone webshot with automatic browser download and argparse CLI
"""

from playwright.sync_api import sync_playwright
import sys
import os
import subprocess
import logging
import argparse
import re
from urllib.parse import urlparse
from datetime import datetime

def url_to_filename(url):
    """Convert URL to a safe filename"""
    parsed = urlparse(url)
    domain = parsed.netloc or 'localhost'
    # Remove www. prefix if present
    if domain.startswith('www.'):
        domain = domain[4:]
    # Replace dots and special chars with underscores
    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', domain)
    return f"{safe_name}.png"

def create_console_filename(output_path):
    """Create console log filename based on output path"""
    base, ext = os.path.splitext(output_path)
    return f"{base}_console.txt"

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Render web pages to image files with optional console log capture (standalone version)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''Examples:
  %(prog)s https://example.com
  %(prog)s https://example.com --output screenshot.png
  %(prog)s https://example.com --size 1920x1080 --console-log
  %(prog)s https://example.com --delay 2000 --console-output logs.txt'''
    )
    
    parser.add_argument('url', help='URL to capture')
    parser.add_argument('--output', '-o', help='Output image file (default: auto-generated from URL)')
    parser.add_argument('--size', '-s', default='1280x720', 
                       help='Screenshot dimensions in WIDTHxHEIGHT format (default: 1280x720)')
    parser.add_argument('--delay', '-d', type=int, default=0, metavar='MS',
                       help='Delay in milliseconds after page load (default: 0)')
    parser.add_argument('--console-log', '-c', action='store_true',
                       help='Capture console logs to text file')
    parser.add_argument('--console-output', metavar='FILE',
                       help='Console log output file (default: auto-generated from image name)')
    parser.add_argument('--format', '-f', choices=['png', 'jpg', 'jpeg'], default='png',
                       help='Output image format (default: png)')
    
    return parser.parse_args()

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
    
    # Parse command line arguments
    args = parse_arguments()
    
    logger.debug(f"Starting webshot_standalone with arguments: {vars(args)}")
    
    # Set output filename if not provided
    if not args.output:
        args.output = url_to_filename(args.url)
        # Add format extension if needed
        if not args.output.endswith(f'.{args.format}'):
            base = os.path.splitext(args.output)[0]
            args.output = f"{base}.{args.format}"
    
    # Set console output filename if console logging is enabled
    console_output_path = None
    if args.console_log or args.console_output:
        if args.console_output:
            console_output_path = args.console_output
        else:
            console_output_path = create_console_filename(args.output)
    
    logger.debug(f"URL: {args.url}")
    logger.debug(f"Output path: {args.output}")
    logger.debug(f"Dimensions: {args.size}")
    logger.debug(f"Delay: {args.delay}ms")
    logger.debug(f"Console logging: {args.console_log or bool(args.console_output)}")
    if console_output_path:
        logger.debug(f"Console output path: {console_output_path}")
    
    # Parse dimensions
    try:
        width, height = args.size.split('x')
        width = int(width)
        height = int(height)
        logger.debug(f"Parsed dimensions: width={width}, height={height}")
    except ValueError:
        print(f"Error: Invalid dimensions format '{args.size}'. Use WIDTHxHEIGHT (e.g., 1280x720)")
        logger.error(f"Failed to parse dimensions: {args.size}")
        sys.exit(1)
    
    # Validate output file extension
    output_ext = os.path.splitext(args.output)[1].lower()
    if output_ext not in ['.png', '.jpg', '.jpeg']:
        # Auto-add extension based on format
        args.output = f"{os.path.splitext(args.output)[0]}.{args.format}"
        logger.debug(f"Added extension to output path: {args.output}")

    # Ensure browser is installed
    logger.info("Ensuring browser is installed...")
    ensure_browser_installed()

    # Console message storage
    console_messages = []
    
    def handle_console_message(msg):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        console_messages.append(f"[{timestamp}] {msg.type.upper()}: {msg.text}")
        logger.debug(f"Console {msg.type}: {msg.text}")

    try:
        logger.debug("Initializing Playwright...")
        with sync_playwright() as p:
            logger.debug("Launching Chromium browser...")
            browser = p.chromium.launch(headless=True)
            logger.debug(f"Creating new page with viewport: {width}x{height}")
            page = browser.new_page(viewport={'width': width, 'height': height})

            # Set up console message capture if requested
            if console_output_path:
                page.on('console', handle_console_message)
                logger.debug("Console message capture enabled")

            print(f"Loading {args.url}...")
            logger.info(f"Navigating to URL: {args.url}")
            page.goto(args.url, wait_until='networkidle')
            logger.debug("Page loaded successfully, network is idle")

            if args.delay > 0:
                print(f"Waiting {args.delay}ms after network idle...")
                logger.debug(f"Applying delay of {args.delay}ms after network idle")
                page.wait_for_timeout(args.delay)

            print(f"Capturing screenshot to {args.output}...")
            logger.info(f"Taking screenshot to: {args.output}")
            page.screenshot(path=args.output, full_page=True)
            logger.debug("Screenshot captured successfully")

            # Save console messages if any were captured
            if console_output_path and console_messages:
                with open(console_output_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(console_messages))
                print(f"Console logs saved to {console_output_path}")
                logger.info(f"Console logs written to: {console_output_path}")
            elif console_output_path:
                # Create empty file if no console messages
                with open(console_output_path, 'w', encoding='utf-8') as f:
                    f.write(f"# Console logs for {args.url}\n# No console messages captured\n")
                print(f"Console log file created: {console_output_path} (no messages)")
                logger.info(f"Empty console log file created: {console_output_path}")

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