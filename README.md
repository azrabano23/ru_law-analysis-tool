# CSRR Faculty Media Tracking System

**Center for Security, Race and Rights (CSRR) - Rutgers Law School**  
**Automated Media Mention Detection System**

## Overview

This system automatically tracks and analyzes media mentions, op-eds, interviews, and publications by CSRR faculty affiliates. It searches major news outlets and generates structured reports for review.

## Current Production System (July 2025)

The system has been refined to meet strict accuracy requirements:

- **Accuracy Validation**: Every result is verified for actual faculty mention
- **Trusted Sources**: Filters to legitimate news outlets (New York Times, Washington Post, CNN, etc.)
- **Proper Format**: Output matches required format (Author, Title, Source, Date, URL)
- **No Misattribution**: Prevents incorrect faculty associations
- **Quality Control**: Strict validation ensures only verified media mentions

## Latest Results (June - July 2025)

- 1 new faculty media mention identified
- Major outlets monitored: CNN, New York Times, Washington Post, Al Jazeera, BBC, NPR, Reuters, Politico, The Atlantic, The Guardian, and others
- Content types: Op-eds, interviews, articles, podcasts, TV appearances

## Files in Repository

**Current Reports:**
- `CSRR_Faculty_Media_June_July_2025_ONLY_20250727_1357.xlsx` - New findings for June-July 2025
- `CSRR_Faculty_Media_COMBINED_All_Periods_20250727_1357.xlsx` - Combined historical and new data

**Code:**
- `csrr_production_search.py` - Main automation script

**Documentation:**
- `README.md` - This file
- `requirements.txt` - Required software packages
- `LICENSE` - Usage terms

## How to Run the System

1. **Execute the search:**
   ```
   python3 csrr_production_search.py
   ```

2. **Review the output files:**
   - Excel files contain structured data for analysis
   - All results are pre-validated for accuracy
   - Processing time: approximately 60-90 minutes

## Support & Maintenance

**Primary Contact:** Azra Bano
**Repository:** [GitHub Link](https://github.com/azrabano23/ru_law-analysis-tool)

For issues, please ensure:
- Dependencies and network connectivity are correct
- Faculty names and search parameters are verified

Monthly reviews may include:
- Manual verification of entries
- Update of faculty list
- Archiving of previous results
- Summary generation

## License

MIT License - Open source for educational and research purposes.

## Mission Alignment

This system supports CSRR's mission by amplifying faculty voices in public discourse, tracking academic impact on policy, facilitating media engagement, and supporting transparency in academic-public interfaces.
