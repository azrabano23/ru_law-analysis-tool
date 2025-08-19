# CSRR Faculty Media Tracker

An automated system for tracking op-eds, print interviews, and television interviews by CSRR faculty affiliates. This tool uses Google Custom Search API to find recent media appearances and generates comprehensive reports.

## 🚀 Features

- **Comprehensive Search**: Uses Google Custom Search API for thorough web searching
- **Strict Filtering**: Only returns legitimate news sources and recent content
- **Date Validation**: Ensures all results are within specified date ranges
- **Multiple Output Formats**: Generates both Excel and Word reports
- **Professional Formatting**: Clean, organized document output
- **Faculty Auto-Detection**: Automatically fetches current faculty list from CSRR website

## 📋 Requirements

- Python 3.7+
- Google Custom Search API key
- Google Custom Search Engine ID

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/azrabano23/ru_law-analysis-tool.git
   cd ru_law-analysis-tool
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google API credentials**:
   - Get Google API key from [Google Cloud Console](https://console.cloud.google.com/)
   - Create Custom Search Engine at [Google CSE](https://cse.google.com/)
   - Set environment variables:
     ```bash
     export GOOGLE_API_KEY='your_api_key_here'
     export GOOGLE_CSE_ID='your_cse_id_here'
     ```

## 🎯 Usage

### Quick Start
```bash
python enhanced_faculty_media_tracker.py
```

### Quick Test (5 faculty members)
```bash
python enhanced_faculty_media_tracker.py --quick-test
```

### API Setup Help
```bash
python enhanced_faculty_media_tracker.py --setup-api
```

## ⚙️ Configuration

Edit `config.yaml` to customize:

```yaml
search_period:
  start_date: '2025-06-01'
  end_date: '2025-08-19'

output:
  word_filename: 'CSRR_Faculty_Op-Eds_Jun2025_to_Aug2025.docx'
  excel_filename: 'CSRR_Faculty_Media_Report.xlsx'
  save_to_downloads: true
  max_results_per_faculty: 15

search:
  use_google_api: true
  use_basic_search: false
  delay_between_searches: 5
  max_results_per_query: 10
```

## 📊 Output

### Excel Report
- Comprehensive data with all article details
- Includes URLs, publication dates, and search methods
- Suitable for data analysis

### Word Document
- Clean, professional formatting
- Organized by faculty member
- Ready for presentation and sharing
- Saved to Downloads folder by default

## 🔍 Search Capabilities

### Content Types Found
- **Op-eds**: Opinion pieces and editorials
- **Print Interviews**: Newspaper and magazine interviews
- **Television Interviews**: TV news appearances
- **Commentary**: Analysis and commentary pieces

### Legitimate Sources
- Major newspapers (NYT, Guardian, Washington Post)
- News networks (CNN, MSNBC, Fox News, PBS)
- International media (Al Jazeera, BBC, Reuters)
- Legal publications (Law.com, Just Security)
- Academic and policy outlets

### Filtering
- **Date validation**: Only content within specified range
- **Source validation**: Only legitimate news outlets
- **Content validation**: Only actual media appearances
- **Excludes**: Social media, academic papers, generic pages

## 📈 Performance

### Recent Results (June 1 - August 19, 2025)
- **Total Faculty**: 167 faculty members
- **Faculty with Articles**: 29 faculty (17.4% success rate)
- **Total Articles**: 48 articles
- **Average per Faculty**: 1-3 articles (realistic for 2.5 months)

### Search Quality
- **High accuracy**: Only legitimate media appearances
- **Recent content**: All articles within date range
- **Relevant sources**: Major news outlets only
- **No false positives**: Strict filtering eliminates irrelevant content

## 🛡️ Error Handling

- **Rate limiting**: Automatic delays between API calls
- **Network errors**: Graceful handling of connection issues
- **Invalid dates**: Filtered out automatically
- **Missing data**: Handled with fallbacks

## 📁 File Structure

```
ru_law-analysis-tool/
├── enhanced_faculty_media_tracker.py  # Main application
├── config.yaml                        # Configuration file
├── requirements.txt                   # Python dependencies
├── README.md                         # This file
├── USAGE_GUIDE.md                    # Quick start guide
├── setup.py                          # Installation script
├── run_tracker.sh                    # Mac/Linux launcher
├── run_tracker.bat                   # Windows launcher
└── CSRR_Faculty_Op-Eds_Jun2025_to_Aug2025.docx  # Sample output
```

## 🔧 Troubleshooting

### Common Issues

1. **API Rate Limits**: 
   - The system automatically handles rate limiting
   - Consider upgrading to paid Google Cloud plan for higher quotas

2. **No Results Found**:
   - Check date range in config.yaml
   - Verify API credentials are set correctly
   - Ensure faculty members have recent media appearances

3. **Permission Errors**:
   - Ensure write permissions in output directory
   - Check Downloads folder access

## 💰 Cost Considerations

- **Google Custom Search API**: $5 per 1,000 queries
- **Estimated monthly cost**: $15-25 for comprehensive faculty tracking
- **Free tier**: 100 queries/day (insufficient for full faculty list)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is developed for CSRR (Center for Security, Race and Rights) at Rutgers University.

## 📞 Support

For questions or issues, please contact the CSRR team or create an issue in this repository.

---

**Last Updated**: August 2025  
**Version**: 2.0 (Enhanced with Google API)  
**Status**: Production Ready
