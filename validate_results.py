#!/usr/bin/env python3
"""
CSRR Faculty Media Search - Validation Script
Helps manually review results for accuracy before sending to boss
"""

import pandas as pd
from docx import Document
import random
import requests
from bs4 import BeautifulSoup

def validate_excel_output(excel_file):
    """Load and validate Excel output"""
    try:
        df = pd.read_excel(excel_file)
        print(f"Loaded Excel file: {excel_file}")
        print(f"Total entries: {len(df)}")
        print(f"Faculty with results: {df['Faculty Name'].nunique()}")
        print(f"Columns: {list(df.columns)}")
        
        return df
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None

def check_url_validity(url, max_checks=20):
    """Check if URLs are actually accessible and valid"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        return response.status_code == 200
    except:
        return False

def sample_validation_check(df, sample_size=10):
    """Perform validation checks on a sample of results"""
    print(f"\n=== SAMPLE VALIDATION CHECK ({sample_size} entries) ===")
    
    if len(df) == 0:
        print("No data to validate!")
        return
    
    # Sample random entries
    sample_size = min(sample_size, len(df))
    sample_df = df.sample(n=sample_size)
    
    issues_found = []
    
    for idx, row in sample_df.iterrows():
        faculty_name = row['Faculty Name']
        title = row['Title']
        url = row.get('Link', row.get('URL', 'N/A'))
        source = row.get('Publication', row.get('Source', 'Unknown'))
        author = row.get('Author', faculty_name)  # Default to faculty name
        
        print(f"\nChecking entry {idx + 1}:")
        print(f"Faculty: {faculty_name}")
        print(f"Author: {author}")
        print(f"Title: {title[:80]}...")
        print(f"Source: {source}")
        print(f"URL: {url}")
        
        # Check 1: Author should match faculty name
        if author != faculty_name:
            issue = f"Author mismatch: {author} != {faculty_name}"
            issues_found.append(issue)
            print(f"⚠️  {issue}")
        
        # Check 2: Faculty name should appear in title (basic relevance)
        name_parts = faculty_name.lower().split()
        title_lower = title.lower()
        name_in_title = any(part in title_lower for part in name_parts if len(part) > 2)
        
        if not name_in_title:
            issue = f"Faculty name not found in title: {faculty_name} -> {title[:50]}..."
            issues_found.append(issue)
            print(f"⚠️  {issue}")
        
        # Check 3: URL validity (check a few)
        if len(issues_found) < 3:  # Only check URLs for first few to avoid being blocked
            url_valid = check_url_validity(url)
            if not url_valid:
                issue = f"URL may be invalid or inaccessible: {url}"
                issues_found.append(issue)
                print(f"⚠️  {issue}")
        
        # Check 4: Source should match URL domain
        expected_domains = {
            'New York Times': 'nytimes.com',
            'Washington Post': 'washingtonpost.com',
            'CNN': 'cnn.com',
            'Al Jazeera': 'aljazeera.com',
            'BBC': 'bbc.com',
            'NPR': 'npr.org',
            'Reuters': 'reuters.com',
            'The Guardian': 'theguardian.com'
        }
        
        if source in expected_domains:
            expected_domain = expected_domains[source]
            if expected_domain not in url.lower():
                issue = f"Source/URL mismatch: {source} should contain {expected_domain} but URL is {url}"
                issues_found.append(issue)
                print(f"⚠️  {issue}")
        
        if len(issues_found) == 0:
            print("✅ Entry looks good!")
    
    print(f"\n=== VALIDATION SUMMARY ===")
    print(f"Entries checked: {sample_size}")
    print(f"Issues found: {len(issues_found)}")
    
    if issues_found:
        print("\n🚨 ISSUES DETECTED:")
        for i, issue in enumerate(issues_found, 1):
            print(f"{i}. {issue}")
        print(f"\nRecommendation: Review these issues before sending to boss.")
    else:
        print("✅ No obvious issues detected in sample!")
    
    return issues_found

def check_for_nausheen_husain_issue(df):
    """Specifically check for the Nausheen Husain issue mentioned by boss"""
    print(f"\n=== CHECKING FOR NAUSHEEN HUSAIN ISSUE ===")
    
    # Find entries where Nausheen Husain appears
    nausheen_entries = df[df['Faculty Name'].str.contains('Nausheen Husain', case=False, na=False)]
    
    if len(nausheen_entries) > 0:
        print(f"Found {len(nausheen_entries)} entries for Nausheen Husain:")
        for idx, row in nausheen_entries.iterrows():
            source = row.get('Publication', row.get('Source', 'Unknown'))
            print(f"- {row['Title'][:60]}... ({source})")
    else:
        print("No entries found for Nausheen Husain")
    
    # Check if Nausheen Husain appears in other faculty's entries (the boss's concern)
    other_entries = df[~df['Faculty Name'].str.contains('Nausheen Husain', case=False, na=False)]
    problematic = other_entries[
        other_entries['Title'].str.contains('Nausheen Husain', case=False, na=False) |
        other_entries['Snippet'].str.contains('Nausheen Husain', case=False, na=False)
    ]
    
    if len(problematic) > 0:
        print(f"\n🚨 FOUND THE ISSUE! Nausheen Husain appears in {len(problematic)} entries attributed to other faculty:")
        for idx, row in problematic.iterrows():
            source = row.get('Publication', row.get('Source', 'Unknown'))
            print(f"❌ Listed under: {row['Faculty Name']}")
            print(f"   Title: {row['Title'][:80]}...")
            print(f"   Source: {source}")
            print()
    else:
        print("✅ No misattribution of Nausheen Husain found")

def generate_accuracy_report(excel_file):
    """Generate a comprehensive accuracy report"""
    print("=== CSRR FACULTY MEDIA SEARCH - ACCURACY VALIDATION ===\n")
    
    df = validate_excel_output(excel_file)
    if df is None:
        return
    
    # Basic statistics
    print(f"📊 BASIC STATISTICS:")
    print(f"Total entries: {len(df)}")
    print(f"Unique faculty with results: {df['Faculty Name'].nunique()}")
    print(f"Total faculty in list: 151")
    print(f"Coverage: {df['Faculty Name'].nunique()}/151 ({df['Faculty Name'].nunique()/151*100:.1f}%)")
    
    # Source distribution
    print(f"\n📰 SOURCE DISTRIBUTION:")
    if 'Source' in df.columns:
        source_counts = df['Source'].value_counts()
        for source, count in source_counts.head(10).items():
            print(f"{source}: {count} articles")
    elif 'Publication' in df.columns:
        source_counts = df['Publication'].value_counts()
        for source, count in source_counts.head(10).items():
            print(f"{source}: {count} articles")
    else:
        print("No source/publication column found")
    
    # Check for specific issue mentioned by boss
    check_for_nausheen_husain_issue(df)
    
    # Sample validation
    sample_validation_check(df, sample_size=15)
    
    # Format compliance check
    print(f"\n📋 FORMAT COMPLIANCE CHECK:")
    required_columns = ['Faculty Name', 'Author', 'Title', 'Source', 'URL']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"❌ Missing required columns: {missing_columns}")
    else:
        print("✅ All required columns present")
    
    # Check for empty entries
    empty_titles = df['Title'].isna().sum()
    empty_urls = df.get('Link', df.get('URL', pd.Series([]))).isna().sum() if 'Link' in df.columns or 'URL' in df.columns else 0
    empty_sources = df.get('Publication', df.get('Source', pd.Series([]))).isna().sum() if 'Publication' in df.columns or 'Source' in df.columns else 0
    
    print(f"Empty titles: {empty_titles}")
    print(f"Empty URLs: {empty_urls}")
    print(f"Empty sources: {empty_sources}")
    
    print(f"\n=== RECOMMENDATIONS ===")
    print("1. Manually review the sample entries flagged above")
    print("2. Check that faculty attribution is correct")
    print("3. Verify that URLs are accessible and relevant")
    print("4. Confirm that the format matches: Author, Title, Source, Date, URL")
    print("5. Test a few articles to ensure they actually mention the faculty member")

if __name__ == "__main__":
    import sys
    
    # Default to the fixed version if no file specified
    excel_file = "CSRR_Faculty_Media_June_July_2025_FIXED_VALIDATED.xlsx"
    
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
    
    try:
        generate_accuracy_report(excel_file)
    except Exception as e:
        print(f"Error during validation: {e}")
        import traceback
        traceback.print_exc()
