from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os
from pathlib import Path

# Collect all playwright data
datas = collect_data_files('playwright')

# Add browser binaries
home = Path.home()
browser_path = home / '.cache' / 'ms-playwright'
if browser_path.exists():
    datas.append((str(browser_path), 'playwright/driver/package/.local-browsers'))

hiddenimports = collect_submodules('playwright')