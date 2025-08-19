# GitHub Repository Files

## ✅ Files to Include (Essential)

### Core Scripts
- `enhanced_faculty_media_tracker.py` - Main Google API tracker
- `bing_search_tracker.py` - Bing API alternative
- `config.yaml` - Configuration file
- `requirements.txt` - Python dependencies
- `setup.py` - Installation script

### Documentation
- `README.md` - Main documentation
- `USAGE_GUIDE.md` - Quick start guide
- `API_SETUP_GUIDE.md` - API setup instructions
- `.gitignore` - Git ignore rules

### Optional (Include if you want)
- `run_tracker.bat` - Windows launcher
- `run_tracker.sh` - Mac/Linux launcher
- `csrr_production_search.py` - Original reference script
- `extract_faculty.py` - Faculty extraction utility

## ❌ Files to Exclude (Not needed on GitHub)

### Generated Reports
- `CSRR_Faculty_Media_Report.xlsx`
- `CSRR_Faculty_Op-Eds*.docx`
- `CSRR_Faculty_Media_*.docx`

### Debug/Temporary Files
- `debug_*.py`
- `analyze_format.py`
- `automated_faculty_media_tracker.py` (old version)

### API Keys/Sensitive Data
- Any files with API keys
- `.env` files
- Personal configuration files

## 🚀 GitHub Push Commands

```bash
# Add essential files
git add enhanced_faculty_media_tracker.py
git add bing_search_tracker.py
git add config.yaml
git add requirements.txt
git add setup.py
git add README.md
git add USAGE_GUIDE.md
git add API_SETUP_GUIDE.md
git add .gitignore

# Optional files
git add run_tracker.bat
git add run_tracker.sh

# Commit and push
git commit -m "Add CSRR Faculty Media Tracker v2.0"
git push origin main
```

## 📋 Repository Structure

```
ru_law-analysis-tool-1/
├── enhanced_faculty_media_tracker.py  # Main Google API tracker
├── bing_search_tracker.py             # Bing API alternative
├── config.yaml                        # Configuration file
├── requirements.txt                   # Python dependencies
├── setup.py                          # Installation script
├── README.md                         # Main documentation
├── USAGE_GUIDE.md                    # Quick start guide
├── API_SETUP_GUIDE.md               # API setup instructions
├── .gitignore                        # Git ignore rules
├── run_tracker.bat                   # Windows launcher (optional)
└── run_tracker.sh                    # Mac/Linux launcher (optional)
```

## 🎯 Key Features Highlighted

- **Multi-API Support**: Google Custom Search + Bing Search APIs
- **Rate Limiting Solutions**: Handles API limits gracefully
- **Easy Setup**: One-command installation
- **Comprehensive Documentation**: Multiple guides for different users
- **Production Ready**: Used by CSRR for monthly media tracking
