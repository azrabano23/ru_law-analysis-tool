# CSRR Faculty Media Tracker

An automated tool to track op-eds, interviews, and media appearances by CSRR faculty affiliates. This tool searches for faculty media mentions and generates comprehensive reports in both Excel and Word formats.

## 🚀 Features

- **Automated Faculty Discovery**: Fetches faculty list directly from the CSRR website
- **Multi-Source Search**: Uses Google Custom Search API, Bing Search API, or basic web scraping
- **Comprehensive Reports**: Generates both Excel and Word documents
- **Date Range Filtering**: Search for media within specific date ranges
- **Duplicate Detection**: Automatically removes duplicate articles
- **Faculty Validation**: Ensures faculty names are actually mentioned in results
- **Downloads Integration**: Saves reports directly to your Downloads folder

## 📋 Requirements

- Python 3.7+
- Internet connection
- Optional: API keys for enhanced search capabilities

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ru_law-analysis-tool-1
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the setup script:**
   ```bash
   python setup.py
   ```

## 🔧 Configuration

### Basic Setup

The tool works out of the box with basic web scraping. For enhanced search capabilities, you can configure API keys:

### Google Custom Search API (Recommended but requires billing)
- **Free tier**: 100 queries/day (insufficient for 154 faculty)
- **Paid tier**: $5 per 1,000 queries (~$2.31 per search)
- **Setup**: [Google Cloud Console](https://console.cloud.google.com/)

### Bing Search API (Alternative - More Generous Free Tier)
- **Free tier**: 1,000 searches/month
- **Paid tier**: $3 per 1,000 searches
- **Setup**: [Microsoft Bing Web Search API](https://www.microsoft.com/en-us/bing/apis/bing-web-search-api)

### Environment Variables

Set your API keys as environment variables:

```bash
# For Google Custom Search API
export GOOGLE_API_KEY="your_google_api_key"
export GOOGLE_CSE_ID="your_custom_search_engine_id"

# For Bing Search API
export BING_API_KEY="your_bing_api_key"
```

## 🚀 Usage

### Basic Usage

```bash
# Run with default settings (basic search)
python enhanced_faculty_media_tracker.py

# Run with Bing Search API
python bing_search_tracker.py

# Quick test with first 5 faculty members
python enhanced_faculty_media_tracker.py --quick-test
```

### Advanced Usage

```bash
# Use custom configuration file
python enhanced_faculty_media_tracker.py --config my_config.yaml

# Show API setup instructions
python enhanced_faculty_media_tracker.py --setup-api
```

### Configuration Options

Edit `config.yaml` to customize:

```yaml
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
  use_google_api: true
  use_bing_api: false
  search_types: ['op-ed', 'interview', 'commentary', 'podcast', 'video']
```

## 📊 Output

The tool generates two types of reports:

### Excel Report (`CSRR_Faculty_Media_Report.xlsx`)
- Faculty name
- Article title
- Source
- Publication date
- URL
- Search method used

### Word Report (`CSRR_Faculty_Op-Eds.docx`)
- Formatted for easy reading
- Organized by faculty member
- Includes all article details
- Saved to Downloads folder

## ⚠️ Important Notes

### Rate Limiting Issues

**Google Custom Search API:**
- Free tier: 100 queries/day (insufficient for 154 faculty)
- You'll hit rate limits quickly
- Requires billing setup for full functionality

**Bing Search API:**
- Free tier: 1,000 searches/month (much more generous)
- Better option for regular use
- No billing required for basic usage

### Recommended Approach

1. **Start with Bing Search API** - More generous free tier
2. **Use basic search as fallback** - No API limits
3. **Consider Google API only if you set up billing** - Better results but costs money

## 🔍 Search Capabilities

The tool searches for:
- **Op-eds and opinion pieces**
- **Print and television interviews**
- **Commentary and analysis**
- **Podcast appearances**
- **Video content**

## 🛡️ Error Handling

- **Rate limiting**: Automatic delays and retry logic
- **API failures**: Falls back to basic search
- **Network issues**: Graceful error handling
- **Invalid results**: Faculty name validation

## 📁 File Structure

```
ru_law-analysis-tool-1/
├── enhanced_faculty_media_tracker.py  # Main Google API tracker
├── bing_search_tracker.py             # Bing API alternative
├── config.yaml                        # Configuration file
├── requirements.txt                   # Python dependencies
├── setup.py                          # Installation script
├── README.md                         # This file
├── USAGE_GUIDE.md                    # Quick start guide
└── API_SETUP_GUIDE.md               # Detailed API setup
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**"No articles found"**
- Check your API keys
- Verify date range settings
- Try different search terms

**Rate limiting errors**
- Switch to Bing Search API
- Use basic search mode
- Increase delays between searches

**Configuration errors**
- Verify `config.yaml` format
- Check file permissions
- Ensure all dependencies are installed

### Getting Help

1. Check the troubleshooting section above
2. Review the API setup guides
3. Test with `--quick-test` flag
4. Check the generated log files

## 📈 Performance

- **Basic search**: ~2-3 minutes for 154 faculty
- **Bing API**: ~5-10 minutes for 154 faculty
- **Google API**: ~3-5 minutes for 154 faculty (with billing)

## 🔄 Updates

- **v2.0**: Added Bing Search API support
- **v1.5**: Fixed rate limiting issues
- **v1.0**: Initial release with Google API

---

**Note**: This tool is designed for CSRR faculty media tracking. For other use cases, modify the faculty list and search parameters accordingly.
