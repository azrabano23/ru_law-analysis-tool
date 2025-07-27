#!/usr/bin/env python3
"""
Extract Faculty Names and Run Media Search
Extracts faculty names from the reference document and runs search for June-July 2025
"""

import pandas as pd
import docx
import re
from datetime import datetime
import time
import random
import requests
from bs4 import BeautifulSoup
import urllib.parse

def extract_faculty_names_from_document(doc_path):
    """Extract clean faculty names from the Word document"""
    try:
        doc = docx.Document(doc_path)
        faculty_names = []
        
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            
            # Skip empty lines, headers, and URLs
            if not text or text.startswith('Op-Eds') or text.startswith('Since') or 'http' in text or 'www.' in text:
                continue
            
            # Check if this looks like a faculty name (not a citation)
            # Faculty names are typically 2-4 words, no commas, no periods except middle initials
            words = text.split()
            if (2 <= len(words) <= 4 and 
                not text.startswith('*') and
                not any(char in text for char in ['©', '®', '™']) and
                not text.isupper() and
                not text.endswith('.') and
                ',' not in text):
                
                # Additional filters to exclude non-names
                if not any(word.lower() in text.lower() for word in ['university', 'college', 'institute', 'center', 'department', 'school']):
                    faculty_names.append(text)
        
        # Remove duplicates while preserving order
        unique_faculty = []
        seen = set()
        for name in faculty_names:
            if name not in seen:
                seen.add(name)
                unique_faculty.append(name)
        
        return unique_faculty
        
    except Exception as e:
        print(f"Error reading document: {e}")
        return []

def search_faculty_member(faculty_name, session):
    """Search for media mentions of a specific faculty member"""
    print(f"🔍 Searching: {faculty_name}")
    
    results = []
    
    # Search queries for June-July 2025
    search_queries = [
        f'"{faculty_name}" op-ed opinion commentary after:2025-06-01',
        f'"{faculty_name}" interview quoted after:2025-06-01',
        f'"{faculty_name}" author byline news after:2025-06-01'
    ]
    
    for query in search_queries:
        try:
            # Use DuckDuckGo search (more reliable than Google for automated searches)
            search_url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            
            response = session.get(search_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Parse DuckDuckGo results
                for result in soup.find_all('div', class_='result')[:3]:
                    title_elem = result.find('a', class_='result__a')
                    snippet_elem = result.find('a', class_='result__snippet')
                    
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        url = title_elem.get('href', '')
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                        
                        # Basic validation - faculty name should appear in title or snippet
                        content = f"{title} {snippet}".lower()
                        if faculty_name.lower() in content or any(part.lower() in content for part in faculty_name.split()):
                            
                            # Extract source from URL
                            try:
                                domain = urllib.parse.urlparse(url).netloc
                                source = domain.replace('www.', '').split('.')[0].title()
                            except:
                                source = 'Unknown'
                            
                            results.append({
                                'faculty_name': faculty_name,
                                'author': faculty_name,
                                'title': title,
                                'source': source,
                                'url': url,
                                'publication_date': 'June-July 2025',
                                'snippet': snippet[:200] + '...' if len(snippet) > 200 else snippet,
                                'date_found': datetime.now().strftime('%Y-%m-%d')
                            })
            
            time.sleep(random.uniform(1, 3))  # Rate limiting
            
        except Exception as e:
            print(f"  Search error for {faculty_name}: {e}")
            continue
    
    if results:
        print(f"  ✅ Found {len(results)} results")
    else:
        print(f"  ❌ No results found")
    
    return results

def main():
    """Main function to extract names and run search"""
    print("=" * 60)
    print("🎯 CSRR FACULTY EXTRACTION AND MEDIA SEARCH")
    print("=" * 60)
    
    # Extract faculty names from document
    doc_path = '/Users/azrabano/Downloads/5-31-25 Op-Ed CSRR Affiliates (6).docx'
    print(f"📄 Extracting faculty names from: {doc_path}")
    
    faculty_names = extract_faculty_names_from_document(doc_path)
    print(f"✅ Extracted {len(faculty_names)} faculty names")
    
    # Show first 10 names for verification
    print("\n📋 First 10 faculty names:")
    for i, name in enumerate(faculty_names[:10], 1):
        print(f"  {i:2d}. {name}")
    print("  ...")
    
    # Ask for confirmation before proceeding with search
    print(f"\n🔍 Ready to search for media mentions from June 1 - July 27, 2025")
    print(f"⏱️  Estimated time: {len(faculty_names) * 2} minutes")
    
    proceed = input("\nProceed with search? (y/n): ").lower()
    if proceed != 'y':
        print("Search cancelled.")
        return
    
    # Initialize session for searches
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    
    # Run searches for ALL faculty members
    all_results = []
    for i, faculty_name in enumerate(faculty_names, 1):  # ALL FACULTY - NO LIMIT
        print(f"\n[{i:3d}/{len(faculty_names)}] Processing: {faculty_name}")
        
        results = search_faculty_member(faculty_name, session)
        all_results.extend(results)
        
        # Progress update every 10 faculty
        if i % 10 == 0:
            print(f"\n📊 Progress: {i}/{len(faculty_names)} complete, {len(all_results)} total results")
        
        time.sleep(random.uniform(2, 5))  # Rate limiting between faculty
    
    # Create Excel report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"CSRR_Faculty_Media_June_July_2025_{timestamp}.xlsx"
    
    if all_results:
        # Add search order
        for i, result in enumerate(all_results, 1):
            result['search_order'] = i
            
        df = pd.DataFrame(all_results)
        df = df[["faculty_name", "author", "title", "source", "url", 
                "publication_date", "date_found", "search_order", "snippet"]]
        df.columns = ["Faculty Name", "Author", "Title", "Source", "URL", 
                     "Publication Date", "Date Found", "Search Order", "Snippet"]
    else:
        # Create empty structure if no results
        df = pd.DataFrame(columns=[
            "Faculty Name", "Author", "Title", "Source", "URL", 
            "Publication Date", "Date Found", "Search Order", "Snippet"
        ])
    
    df.to_excel(filename, index=False)
    
    print("\n" + "=" * 60)
    print("📋 FINAL RESULTS")
    print("=" * 60)
    print(f"Total faculty processed: {len(faculty_names)}")
    print(f"Total results found: {len(all_results)}")
    print(f"Faculty with results: {len(set(r['faculty_name'] for r in all_results)) if all_results else 0}")
    print(f"Excel file: {filename}")
    print("=" * 60)
    
    return filename

if __name__ == "__main__":
    main()
