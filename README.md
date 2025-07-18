# CSRR Faculty Media Tracking System

**Center for Security, Race and Rights (CSRR) - Rutgers Law School**  
**Automated Op-Ed and Media Mention Detection System**

## 📋 Overview

This repository contains a comprehensive automated system for tracking and analyzing media mentions, op-eds, interviews, and publications by CSRR faculty affiliates. The system processes web searches across major news outlets and generates structured reports for monthly review.

## 🚀 Latest Update (July 18, 2025)

**Complete System Overhaul:** Upgraded from manual May 2024 processing to fully automated web scraping system covering all 151 CSRR faculty affiliates.

### Key Improvements:
- **Comprehensive Coverage:** All 151 faculty members from official CSRR website
- **Multi-Source Search:** CNN, NYT, Washington Post, Al Jazeera, BBC, NPR, Reuters, and 20+ more outlets
- **Automated Processing:** 14 different search strategies per faculty member
- **Smart Filtering:** AI-powered relevance detection and duplicate removal
- **Monthly Automation:** Ready-to-use scripts for ongoing monthly reports

## 📊 Current Results (June 18 - July 18, 2025)

- **68 faculty members** with media mentions
- **120 total media mentions** catalogued
- **Major outlets covered:** CNN, New York Times, Washington Post, Al Jazeera, BBC, NPR, Reuters, Politico, The Atlantic, The Guardian, HuffPost, Slate, Vox, and more
- **Content types:** Op-eds, interviews, articles, podcasts, TV appearances

## 📁 Repository Structure

```
📁 ru_law-analysis-tool/
├── 📊 CSRR_Faculty_Media_June_July_2025_ALL_151_FACULTY.xlsx    # Primary Excel Report
├── 📄 CSRR_Faculty_Media_June_July_2025_ALL_151_FACULTY.docx    # Primary Word Report
├── 📋 CSRR_Merged_Opeds_June_July_2025.docx                    # Comprehensive Historical Record
├── 📄 5-31-25 Op-Ed CSRR Affiliates (5).docx                   # Original Reference Document
├── 🐍 csrr_working_search.py                                   # Main Automation Script
├── 📖 README.md                                                # This Documentation
├── 📊 data/                                                    # Legacy Data Directory
└── 🧪 reports/                                                 # Output Reports Directory
```

## 🛠️ System Components

### Primary Files

**📊 Excel Report** (`CSRR_Faculty_Media_June_July_2025_ALL_151_FACULTY.xlsx`)
- **120 rows** of structured data
- **Columns:** Faculty Name, Title, Publication, Link, Snippet, Date Found, Search Order
- **Usage:** Data analysis, filtering, sorting, and statistics

**📄 Word Report** (`CSRR_Faculty_Media_June_July_2025_ALL_151_FACULTY.docx`)
- **Formatted document** matching traditional CSRR style
- **Faculty sections** with publication listings
- **Usage:** Direct publication, newsletter inclusion, website updates

**📋 Comprehensive Document** (`CSRR_Merged_Opeds_June_July_2025.docx`)
- **Complete historical record** from October 2023 to July 2025
- **Combined data** from multiple search periods
- **Usage:** Long-term tracking, historical analysis

### Automation Script

**🐍 Main Script** (`csrr_working_search.py`)
- **151 faculty members** processed automatically
- **14 search strategies** per faculty member
- **Rate limiting** to avoid blocking (2-4 second delays)
- **Smart filtering** for academic/media content
- **Output:** Both Excel and Word formats

## 🚀 Usage Instructions

### For Monthly Reports

1. **Update Date Range:**
   ```python
   # In csrr_working_search.py, modify search queries for new date range
   ```

2. **Run the Script:**
   ```bash
   cd ru_law-analysis-tool
   python3 csrr_working_search.py
   ```

3. **Review Results:**
   - Excel file for data analysis
   - Word document for publication
   - Approximately 35-40 minutes processing time

### For Custom Searches

1. **Modify Faculty List:**
   ```python
   # Edit faculty_list array in csrr_working_search.py
   faculty_list = ["Faculty Name 1", "Faculty Name 2", ...]
   ```

2. **Adjust Search Parameters:**
   ```python
   # Modify search_queries array for different content types
   search_queries = [
       f'"{name}" op-ed',
       f'"{name}" interview',
       # Add custom queries...
   ]
   ```

## 🔧 Technical Requirements

```bash
# Install required packages
pip3 install pandas python-docx requests beautifulsoup4 openpyxl

# Optional: For enhanced analysis
pip3 install openai  # If using AI features
```

### Dependencies
- **Python 3.7+**
- **pandas** - Data manipulation and Excel export
- **python-docx** - Word document generation
- **requests** - Web scraping
- **beautifulsoup4** - HTML parsing
- **openpyxl** - Excel file handling

## 📈 Search Methodology

### Multi-Strategy Approach
For each faculty member, the system performs:

1. **Direct Searches:**
   - `"Faculty Name" op-ed`
   - `"Faculty Name" interview`
   - `"Faculty Name" commentary`

2. **Outlet-Specific Searches:**
   - `Faculty Name CNN`
   - `Faculty Name "New York Times"`
   - `Faculty Name "Washington Post"`

3. **Content-Type Searches:**
   - `Faculty Name podcast`
   - `Faculty Name television`
   - `Faculty Name opinion`

### Filtering & Quality Control
- **Relevance filtering** for academic/media content
- **Duplicate removal** based on titles and links
- **Source verification** against major news outlets
- **Content type classification** (op-ed, interview, article, etc.)

## 📅 Automation Schedule

**Recommended Monthly Process:**
1. **1st of each month:** Run automated search for previous month
2. **2nd-3rd:** Review and verify results
3. **5th:** Publish final reports
4. **Integration:** Add to CSRR website "In the News" section

## 🎯 Future Enhancements

- **AI-Powered Summarization:** Automated content analysis
- **Sentiment Analysis:** Track positive/negative coverage
- **Impact Metrics:** Social media engagement tracking
- **Real-time Alerts:** Immediate notification of high-impact mentions
- **Dashboard Interface:** Web-based monitoring system

## 📊 Historical Data

### Previous Versions:
- **May 2024:** Manual processing system (legacy)
- **June 2025:** Automated system implementation
- **July 2025:** Full faculty coverage (151 members)

### Growth Metrics:
- **Faculty Coverage:** 151 members (100% of CSRR affiliates)
- **Search Efficiency:** 35-40 minutes for complete scan
- **Detection Rate:** ~45% of faculty have monthly media mentions
- **Source Diversity:** 20+ major news outlets monitored

## 🔗 Integration

### CSRR Website
- **"In the News" section:** Direct publication of results
- **Faculty profiles:** Individual mention tracking
- **Monthly newsletters:** Automated content generation

### External Systems
- **Email alerts:** Stakeholder notifications
- **Social media:** Automated sharing of highlights
- **Academic databases:** Cross-reference with publications

## 📞 Support & Maintenance

**Primary Contact:** Azra Bano  
**Repository:** https://github.com/azrabano23/ru_law-analysis-tool  
**Last Updated:** July 18, 2025

### For Issues:
1. **Technical Problems:** Check dependencies and network connectivity
2. **Missing Results:** Verify faculty names and search parameters
3. **Performance Issues:** Adjust rate limiting in script

### Monthly Review Process:
1. **Validate Results:** Manual spot-checking of 10-15 entries
2. **Update Faculty List:** Add/remove affiliates as needed
3. **Archive Data:** Store previous month's results
4. **Generate Summary:** Create monthly impact report

## 📋 License

MIT License - Open source for educational and research purposes.

## 🎯 Mission Alignment

This system directly supports CSRR's mission of promoting security, race, and rights scholarship by:
- **Amplifying faculty voices** in public discourse
- **Tracking impact** of academic expertise on policy debates
- **Facilitating media engagement** through organized outreach
- **Supporting transparency** in academic-public interfaces

---

*This system represents a significant advancement in academic media tracking, providing CSRR with comprehensive, automated monitoring of faculty public engagement and scholarly impact.*
