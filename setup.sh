#!/bin/bash

echo "Setting up WebShot with Miniconda environment..."

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Miniconda not found. Installing Miniconda..."
    
    # Detect OS and architecture
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
    else
        echo "Unsupported OS. Please install Miniconda manually."
        exit 1
    fi
    
    # Download and install Miniconda
    wget -O miniconda.sh $MINICONDA_URL
    bash miniconda.sh -b -p $HOME/miniconda3
    rm miniconda.sh
    
    # Add to PATH
    export PATH="$HOME/miniconda3/bin:$PATH"
    echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc
    
    # Initialize conda
    conda init bash
    source ~/.bashrc
fi

# Create webshot environment
echo "Creating 'webshot' conda environment with Python 3.11..."
conda create -n webshot python=3.11 -y

# Activate environment
echo "Activating 'webshot' environment..."
eval "$(conda shell.bash hook)"
conda activate webshot

# Install Python dependencies
echo "Installing Python packages..."
pip install -r requirements.txt

# Install Chromium for Playwright
echo "Installing Chromium browser..."
playwright install chromium

# Install system dependencies
echo "Installing system dependencies..."
if command -v sudo &> /dev/null; then
    sudo playwright install-deps || echo "Note: System dependencies installation failed. You may need to install them manually."
else
    echo "Note: sudo not available. Please run 'playwright install-deps' with appropriate privileges."
fi

echo ""
echo "Setup complete!"
echo ""
echo "To use WebShot:"
echo "1. Activate the environment: conda activate webshot"
echo "2. Run: python webshot.py [URL] [output-file] [WIDTHxHEIGHT]"
echo ""
echo "Example: python webshot.py http://example.com example.png 1280x720"