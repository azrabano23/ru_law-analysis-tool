#!/usr/bin/env python3
"""
CSRR Faculty Media Search - PRODUCTION VERSION
Addresses all accuracy issues and meets boss requirements exactly
Author: Azra Bano
Date: July 26, 2025
"""

import pandas as pd
from docx import Document
import time
import random
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import json
import os
from typing import List, Dict, Optional

# Complete faculty list - all 151 members
FACULTY_LIST = [
    "Adil Haque", "Adnan Zulfiqar", "Alexander A. Reinert", "Alexander Hinton",
    "Alexis Karteron", "Ali A. Olomi", "Ali R. Chaudhary", "Ameena Ghaffar-Kucher",
    "Amir Hussain", "Anju Gupta", "Atalia Omer", "Atiya Aftab", "Audrey Truschke",
    "Aziz Rana", "Aziza Ahmed", "Behrooz Ghamari-Tabrizi", "Beth Baron", "Beth Stephens",
    "Bidisha Biswas", "Brittany Friedman", "Catherine M. Grosso", "Chaumtoli Huq",
    "Clark B. Lombardi", "Cyra A. Choudhury", "D. Asher Ghertner", "Dalia Fahmy",
    "Deepa Kumar", "Eid Mohamed", "Elise Boddie", "Ellen C. Yaroshefsky",
    "Emily Berman", "Emmaia Gelman", "Eric McDaniel", "Esaa Mohammad Samarah Samarsky",
    "Esther Canty-Barnes", "Faisal Kutty", "Faiza Sayed", "Falguni A. Sheth",
    "Farid Hafez", "Fatemeh Shams", "Gaiutra Devi Bahadur", "Ghada Ageel",
    "Hadi Khoshneviss", "Haider Ala Hamoudi", "Hajar Yazdiha", "Hatem Bazian",
    "Heba M. Khalil", "Huda J. Fakhreddine", "Irus Braverman", "Ivan Kalmar",
    "James R. Jones", "Jasbir K. Puar", "Jasmin Zine", "Jason Brownlee",
    "Jesse Norris", "Joel Beinin", "John Tehranian", "Jon Dubin", "Jonathan Feingold",
    "Jonathan Hafetz", "Jorge Contesse", "Juan Cole", "Karam Dana", "Karim Malak",
    "Karishma Desai", "Khaled A. Beydoun", "Khyati Joshi", "LaToya Baldwin Clark",
    "Lara Sheehi", "Leila Kawar", "Leyla Amzi-Erdogdular", "Lorenzo Veracini",
    "Mahruq Khan", "Marc O. Jones", "Margaret Hu", "Mark Bray", "Marta Esquilin",
    "Maryam Jamshidi", "Matthew Abraham", "Maura Finkelstein", "Mayte Green-Mercado",
    "Meera E. Deo", "Mitra Rastegar", "Mohammad Fadel", "Mojtaba Mahdavi",
    "Muhannad Ayyash", "Nader Hashemi", "Nadia Ahmad", "Nahed Samour",
    "Nancy A. Khalil", "Natsu Taylor Saito", "Nausheen Husain", "Naved Bakali",
    "Nazia Kazi", "Nermin Allam", "Norrinda Brown Hayat", "Noura Erakat",
    "Omar Al-Dewachi", "Omar Dajani", "Omar S. Dahi", "Omid Safi", "Ousseina Alidou",
    "Rabea Benhalim", "Rachel Godsil", "Raquel E Aldana", "Raz Segal",
    "Rebecca Hankins", "Riaz Tejani", "Robert S. Chang", "Sabreena Ghaffar-Siddiqui",
    "Sabrina Alimahomed", "Saeed Khan", "Sahar Mohamed Khamis", "Salman Sayyid",
    "Santiago Slabodsky", "Sarah Eltantawi", "Seema Saifee", "Sherene Razack",
    "Shirin Saeidi", "Shirin Sinnar", "Shoba Sivaprasad Wadhia", "Siham Elkassem",
    "Stacy Hawkins", "Stephen Dycus", "Stephen Sheehi", "Susan M. Akram",
    "Sylvia Chan-Malik", "Tahseen Shah", "Taleed El-Sabawi", "Tazeen M. Ali",
    "Timothy Eatman", "Timothy P. Daniels", "Timothy Raphael", "Toby Jones",
    "Udi Ofer", "Umayyah Cable", "Veena Dubal", "Victoria Ramenzoni",
    "Wadie Said", "Wendell Marsh", "Wendy Greene", "Whitney Strub",
    "William C. Banks", "William I. Robinson", "Yasmiyn Irizarry", "Zahra Ali",
    "Zain Abdullah", "Zakia Salime", "M. Shahid Alam", "Khalil Al-Anani",
    "Joseph Massad", "John L. Esposito", "Katherine M. Franke", "Tanya K. Hernandez"
]

# Trusted news sources mapping (URL domain -> Publication name)
TRUSTED_SOURCES = {
    'nytimes.com': 'New York Times',
    'washingtonpost.com': 'Washington Post', 
    'cnn.com': 'CNN',
    'aljazeera.com': 'Al Jazeera',
    'bbc.com': 'BBC',
    'npr.org': 'NPR',
    'reuters.com': 'Reuters',
    'politico.com': 'Politico',
    'theatlantic.com': 'The Atlantic',
    'theguardian.com': 'The Guardian',
    'huffpost.com': 'HuffPost',
    'slate.com': 'Slate',
    'vox.com': 'Vox',
    'axios.com': 'Axios',
    'apnews.com': 'Associated Press',
    'abcnews.go.com': 'ABC News',
    'cbsnews.com': 'CBS News',
    'nbcnews.com': 'NBC News',
    'foxnews.com': 'Fox News',
    'usatoday.com': 'USA Today',
    'wsj.com': 'Wall Street Journal',
    'newyorker.com': 'The New Yorker',
    'time.com': 'Time',
    'newsweek.com': 'Newsweek',
    'thehill.com': 'The Hill',
    'pbs.org': 'PBS',
    'economist.com': 'The Economist',
    'ft.com': 'Financial Times',
    'nypost.com': 'New York Post'
}

class CSRRMediaSearcher:
    """Main class for CSRR Faculty Media Search with accuracy validation"""
    
    def __init__(self, date_range: str = "June 2025 - July 2025"):
        self.date_range = date_range
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.results_cache = {}
        self.validation_errors = []
        
    def is_trusted_source(self, url: str) -> tuple[bool, str]:
        """Check if URL is from a trusted news source"""
        url_lower = url.lower()
        for domain, name in TRUSTED_SOURCES.items():
            if domain in url_lower:
                return True, name
        return False, "Unknown"
    
    def extract_publication_date(self, content: str, url: str) -> str:
        """Extract actual publication date from content"""
        # Common date patterns
        date_patterns = [
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+202[45]',
            r'\d{1,2}[/-]\d{1,2}[/-]202[45]',
            r'202[45]-\d{2}-\d{2}',
            r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+202[45]'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(0)
        
        # Default based on date range
        return "2025"
    
    def validate_faculty_mention(self, faculty_name: str, title: str, snippet: str, url: str) -> bool:
        """STRICT validation that result actually mentions the faculty member - BOSS REQUIREMENT"""
        content_text = f"{title} {snippet}".lower()
        faculty_lower = faculty_name.lower()
        
        # BOSS REQUIREMENT: Faculty name MUST appear in the content
        # Check for exact name match first (most reliable)
        if faculty_lower in content_text:
            print(f"    ✓ Exact name match found: {faculty_name}")
            return True
        
        # Check for name components (STRICT: both first and last name required)
        name_parts = faculty_lower.split()
        if len(name_parts) >= 2:
            last_name = name_parts[-1]
            first_name = name_parts[0]
            
            # CRITICAL: Both names must appear
            if last_name in content_text and first_name in content_text:
                # Extra validation: ensure names are contextually related
                title_words = title.lower().split()
                snippet_words = snippet.lower().split()
                all_words = title_words + snippet_words
                
                try:
                    first_pos = all_words.index(first_name)
                    last_pos = all_words.index(last_name)
                    # Names must be within 5 words of each other (stricter than before)
                    if abs(first_pos - last_pos) <= 5:
                        print(f"    ✓ Name components validated: {first_name} {last_name}")
                        return True
                    else:
                        print(f"    ✗ Names too far apart: {first_name} and {last_name}")
                except ValueError:
                    print(f"    ✗ Name indexing failed for: {first_name} {last_name}")
        
        # BOSS REQUIREMENT: If we can't validate, reject the result
        print(f"    ✗ REJECTED: '{faculty_name}' not properly mentioned in '{title[:50]}...'")
        return False
    
    def search_with_validation(self, query: str, faculty_name: str, max_results: int = 3) -> List[Dict]:
        """Search with strict validation"""
        try:
            # Add time filter for recent results
            search_query = f"{query} after:2024-06-01"
            url = f"https://www.bing.com/search?q={urllib.parse.quote(search_query)}&count={max_results}"
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            validated_results = []
            
            for result in soup.find_all('li', class_='b_algo')[:max_results]:
                title_elem = result.find('h2')
                if not title_elem:
                    continue
                    
                title_link = title_elem.find('a')
                if not title_link:
                    continue
                
                title = title_link.get_text(strip=True)
                link = title_link.get('href', '')
                
                # Get snippet
                snippet_elem = result.find('p')
                snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                
                # Only process trusted sources
                is_trusted, source_name = self.is_trusted_source(link)
                if not is_trusted:
                    continue
                
                # Strict validation: faculty member must actually be mentioned
                if not self.validate_faculty_mention(faculty_name, title, snippet, link):
                    self.validation_errors.append(f"Failed validation: {faculty_name} not found in '{title[:50]}...'")
                    continue
                
                # Extract publication date
                pub_date = self.extract_publication_date(f"{title} {snippet}", link)
                
                validated_results.append({
                    'title': title,
                    'url': link,
                    'snippet': snippet,
                    'source': source_name,
                    'publication_date': pub_date,
                    'faculty_name': faculty_name
                })
            
            return validated_results
            
        except Exception as e:
            print(f"  Search error for {faculty_name}: {e}")
            return []
    
    def search_faculty_comprehensive(self, faculty_name: str) -> List[Dict]:
        """Comprehensive search for a faculty member with multiple strategies"""
        print(f"🔍 Searching: {faculty_name}")
        
        # High-precision search queries
        search_strategies = [
            f'"{faculty_name}" (op-ed OR opinion OR commentary) 2025',
            f'"{faculty_name}" interview 2025',
            f'"{faculty_name}" Gaza Palestine 2024 2025',
            f'"{faculty_name}" author byline news',
            f'"{faculty_name}" professor quoted'
        ]
        
        all_results = []
        
        for strategy in search_strategies:
            try:
                results = self.search_with_validation(strategy, faculty_name, max_results=2)
                all_results.extend(results)
                
                # Rate limiting
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                print(f"  Error with strategy '{strategy}': {e}")
                continue
        
        # Remove duplicates based on URL
        unique_results = []
        seen_urls = set()
        
        for result in all_results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
                
                # Limit to top 3 per faculty for quality
                if len(unique_results) >= 3:
                    break
        
        if unique_results:
            print(f"  ✅ Found {len(unique_results)} validated results")
        else:
            print(f"  ❌ No validated results found")
            
        return unique_results
    
    def create_excel_report(self, all_results: List[Dict], filename: str) -> None:
        """Create Excel report with boss's required format"""
        if not all_results:
            # Create empty file with proper structure
            df = pd.DataFrame(columns=[
                "Faculty Name", "Author", "Title", "Source", "URL", 
                "Publication Date", "Date Found", "Search Order", "Snippet"
            ])
            df.to_excel(filename, index=False)
            return
        
        # Convert results to DataFrame
        excel_data = []
        for i, result in enumerate(all_results, 1):
            excel_data.append({
                "Faculty Name": result['faculty_name'],
                "Author": result['faculty_name'],  # Boss requirement: Author = Faculty Name
                "Title": result['title'],
                "Source": result['source'],
                "URL": result['url'],
                "Publication Date": result['publication_date'],
                "Date Found": datetime.now().strftime('%Y-%m-%d'),
                "Search Order": i,
                "Snippet": result['snippet'][:500] + "..." if len(result['snippet']) > 500 else result['snippet']
            })
        
        df = pd.DataFrame(excel_data)
        df.to_excel(filename, index=False)
        print(f"📊 Excel report saved: {filename}")
    
    def create_word_report(self, all_results: List[Dict], filename: str) -> None:
        """Create Word report matching boss's exact format requirements"""
        doc = Document()
        
        # Header matching boss's requirement
        doc.add_heading("Op-Eds by CSRR Faculty Affiliates", 0)
        doc.add_heading(self.date_range, 1)
        doc.add_paragraph("")
        
        # Group results by faculty
        faculty_results = {}
        for result in all_results:
            faculty = result['faculty_name']
            if faculty not in faculty_results:
                faculty_results[faculty] = []
            faculty_results[faculty].append(result)
        
        # Sort faculty alphabetically
        for faculty_name in sorted(faculty_results.keys()):
            doc.add_heading(faculty_name, level=2)
            
            results = faculty_results[faculty_name]
            for result in results:
                # Boss's exact format: Author, Title, Source, Date, URL.
                formatted_entry = (
                    f"{result['faculty_name']}, "
                    f"{result['title']}, "
                    f"{result['source']}, "
                    f"{result['publication_date']}, "
                    f"{result['url']}."
                )
                doc.add_paragraph(formatted_entry)
        
        # Add faculty with no results for completeness
        all_faculty_with_results = set(faculty_results.keys())
        faculty_without_results = set(FACULTY_LIST) - all_faculty_with_results
        
        for faculty_name in sorted(faculty_without_results):
            doc.add_heading(faculty_name, level=2)
            doc.add_paragraph("No media mentions found for this period.")
        
        doc.save(filename)
        print(f"📄 Word report saved: {filename}")
    
    def run_complete_search(self) -> tuple[str, str]:
        """Run the complete search for all faculty members"""
        print("=" * 60)
        print("🎯 CSRR FACULTY MEDIA SEARCH - PRODUCTION VERSION")
        print("=" * 60)
        print(f"📅 Period: {self.date_range}")
        print(f"👥 Faculty to process: {len(FACULTY_LIST)}")
        print(f"🔍 Validation: STRICT (only verified mentions)")
        print(f"📰 Sources: TRUSTED OUTLETS ONLY")
        print(f"⏱️  Estimated time: 60-90 minutes")
        print("=" * 60)
        print()
        
        all_results = []
        faculty_with_results = 0
        total_validation_errors = 0
        
        # Process each faculty member
        for i, faculty_name in enumerate(FACULTY_LIST, 1):
            print(f"[{i:3d}/{len(FACULTY_LIST)}] Processing: {faculty_name}")
            
            try:
                results = self.search_faculty_comprehensive(faculty_name)
                
                if results:
                    faculty_with_results += 1
                    all_results.extend(results)
                
                # Progress update every 25 faculty
                if i % 25 == 0:
                    print()
                    print("📊 PROGRESS UPDATE")
                    print(f"   Processed: {i}/{len(FACULTY_LIST)} faculty")
                    print(f"   With results: {faculty_with_results}")
                    print(f"   Total validated results: {len(all_results)}")
                    print(f"   Validation errors caught: {len(self.validation_errors)}")
                    print(f"   Success rate: {faculty_with_results/i*100:.1f}%")
                    print()
                
                # Rate limiting between faculty
                time.sleep(random.uniform(4, 7))
                
            except Exception as e:
                print(f"  ❌ Error processing {faculty_name}: {e}")
                continue
        
        # Final statistics
        print("\n" + "=" * 60)
        print("📋 FINAL RESULTS SUMMARY")
        print("=" * 60)
        print(f"Total faculty processed: {len(FACULTY_LIST)}")
        print(f"Faculty with validated results: {faculty_with_results}")
        print(f"Total validated media mentions: {len(all_results)}")
        print(f"Validation errors prevented: {len(self.validation_errors)}")
        print(f"Success rate: {faculty_with_results/len(FACULTY_LIST)*100:.1f}%")
        print(f"Average results per faculty: {len(all_results)/len(FACULTY_LIST):.2f}")
        
        # Source distribution
        if all_results:
            sources = {}
            for result in all_results:
                source = result['source']
                sources[source] = sources.get(source, 0) + 1
            
            print(f"\n📰 SOURCE DISTRIBUTION:")
            for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
                print(f"   {source}: {count} articles")
        
        # Generate reports
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        excel_filename = f"CSRR_Faculty_Media_{self.date_range.replace(' ', '_').replace('-', 'to')}_{timestamp}_VALIDATED.xlsx"
        word_filename = f"CSRR_Faculty_Media_{self.date_range.replace(' ', '_').replace('-', 'to')}_{timestamp}_VALIDATED.docx"
        
        self.create_excel_report(all_results, excel_filename)
        self.create_word_report(all_results, word_filename)
        
        print(f"\n✅ REPORTS COMPLETED")
        print(f"📊 Excel: {excel_filename}")
        print(f"📄 Word: {word_filename}")
        print("\n🔍 QUALITY ASSURANCE:")
        print("- All results validated for faculty mention")
        print("- Only trusted news sources included")
        print("- Format matches boss requirements exactly")
        print("- Ready for manual review and submission")
        
        return excel_filename, word_filename

def main():
    """Main execution function"""
    try:
        searcher = CSRRMediaSearcher("June 2025 - July 2025")
        excel_file, word_file = searcher.run_complete_search()
        
        print(f"\n🎉 SUCCESS! Files ready for boss review:")
        print(f"📊 {excel_file}")
        print(f"📄 {word_file}")
        
    except KeyboardInterrupt:
        print("\n⚠️  Search interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during search: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
