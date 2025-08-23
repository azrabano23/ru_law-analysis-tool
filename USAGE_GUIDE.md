# Quick Usage Guide

## 🚀 Get Started in 3 Steps

### 1. Setup (One-time)
```bash
# Install dependencies
pip install -r requirements.txt

# Run setup script
python setup.py
```

### 2. Configure (Optional but Recommended)
Get a free Bing Search API key:
1. Go to: https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
2. Click "Try now" 
3. Sign in with Microsoft account
4. Create a new resource
5. Copy your API key

Set the environment variable:
```bash
export BING_API_KEY="your_api_key_here"
```

### 3. Run
```bash
# Quick test (first 5 faculty)
python bing_search_tracker.py --quick-test

# Full search (all faculty)
python bing_search_tracker.py
```

## 📊 Results

The tool generates two files:
- **Excel**: `CSRR_Faculty_Media_Report.xlsx` (detailed data)
- **Word**: `CSRR_Faculty_Op-Eds.docx` (formatted for website)

Both files are saved to your Downloads folder.

## ⚙️ Customize

Edit `config.yaml` to change:
- **Date range**: `start_date` and `end_date`
- **Search types**: op-ed, interview, commentary, etc.
- **Results per faculty**: `max_results_per_faculty`

## 🔧 Troubleshooting

**No articles found?**
- Check your API key: `echo $BING_API_KEY`
- Try different date range
- Run with `--quick-test` first

**Rate limiting?**
- The tool automatically handles delays
- Bing API gives 1,000 free searches/month

**Need help?**
- Check README.md for detailed instructions
- Run `python bing_search_tracker.py --setup-api` for API help

## 📅 Monthly Usage

1. Update dates in `config.yaml`
2. Run the search
3. Review results in generated files
4. Post selected articles to CSRR website

That's it! 🎉
