#!/bin/bash

echo "============================================================"
echo "CSRR Automated Faculty Media Tracker"
echo "============================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if config file exists
if [ ! -f "config.yaml" ]; then
    echo "Creating configuration file..."
    python3 automated_faculty_media_tracker.py --create-config
    echo
    echo "Please edit config.yaml to set your desired date range"
    echo "Then run this script again."
    exit 0
fi

# Run the tracker
echo "Starting faculty media search..."
python3 automated_faculty_media_tracker.py

echo
echo "Search completed! Check the generated files."
