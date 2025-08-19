#!/usr/bin/env python3
"""
Setup script for CSRR Faculty Media Tracker
"""

import os
import sys
import subprocess

def install_requirements():
    """Install required Python packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies. Please run: pip install -r requirements.txt")
        return False
    return True

def create_config():
    """Create default configuration file if it doesn't exist"""
    if not os.path.exists("config.yaml"):
        print("⚙️  Creating default configuration file...")
        config_content = """# CSRR Faculty Media Tracker Configuration

search_period:
  start_date: '2025-06-01'
  end_date: '2025-07-31'

output:
  excel_filename: 'CSRR_Faculty_Media_Report.xlsx'
  word_filename: 'CSRR_Faculty_Op-Eds.docx'
  max_results_per_faculty: 15
  save_to_downloads: true

search:
  max_results_per_query: 10
  delay_between_searches: 1
  use_google_api: false
  use_bing_api: true
  search_types: ['op-ed', 'interview', 'commentary', 'podcast', 'video']

faculty:
  auto_fetch_from_website: true
  manual_list: []
"""
        with open("config.yaml", "w") as f:
            f.write(config_content)
        print("✅ Configuration file created: config.yaml")
    else:
        print("✅ Configuration file already exists: config.yaml")

def show_next_steps():
    """Show next steps for the user"""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Configure API keys (optional but recommended):")
    print("   - Bing Search API: https://www.microsoft.com/en-us/bing/apis/bing-web-search-api")
    print("   - Google Custom Search API: https://console.cloud.google.com/")
    print("\n2. Set environment variables:")
    print("   export BING_API_KEY='your_bing_api_key'")
    print("   export GOOGLE_API_KEY='your_google_api_key'")
    print("   export GOOGLE_CSE_ID='your_custom_search_engine_id'")
    print("\n3. Run the tool:")
    print("   python bing_search_tracker.py --quick-test")
    print("   python enhanced_faculty_media_tracker.py")
    print("\n📚 For more information, see README.md")

def main():
    print("🚀 CSRR Faculty Media Tracker Setup")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        return
    
    # Create config
    create_config()
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()
