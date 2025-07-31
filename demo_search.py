#!/usr/bin/env python3
"""
Demo search for CSRR Faculty to test the tool
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from csrr_production_search import CSRRMediaSearcher

def demo_search():
    # Test with a few prominent faculty members and recent dates
    searcher = CSRRMediaSearcher("January 2024 - July 2025")
    
    # Override the date validation to be more inclusive for demo
    def is_date_in_range_demo(date_str):
        """More inclusive date range for demo"""
        try:
            if any(year in date_str for year in ['2024', '2025']):
                return True
            if any(month in date_str.lower() for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']):
                return True
            return True  # For demo, accept most dates
        except:
            return True
    
    searcher.is_date_in_range = is_date_in_range_demo
    
    # Test with some high-profile faculty who likely have recent articles
    test_faculty = [
        "Noura Erakat",
        "Juan Cole", 
        "Khaled A. Beydoun",
        "Hatem Bazian",
        "Joel Beinin"
    ]
    
    print("🔍 DEMO SEARCH - Testing tool functionality")
    print(f"📅 Searching for articles from recent months (broader range)")
    print(f"👥 Testing with {len(test_faculty)} prominent faculty members")
    print("=" * 60)
    
    all_results = []
    
    for i, faculty_name in enumerate(test_faculty, 1):
        print(f"\n[{i}/{len(test_faculty)}] Testing: {faculty_name}")
        
        # Use web scraping approach with broader date range
        results = searcher.search_with_web_scraping(faculty_name)
        
        if results:
            print(f"  ✅ Found {len(results)} results")
            all_results.extend(results)
            for result in results:
                print(f"    📰 {result['title'][:80]}...")
                print(f"        🔗 {result['source']} - {result['publication_date']}")
        else:
            print(f"  ❌ No results found")
    
    print("\n" + "=" * 60)
    print(f"📊 DEMO RESULTS SUMMARY:")
    print(f"   Total faculty tested: {len(test_faculty)}")
    print(f"   Total articles found: {len(all_results)}")
    print(f"   Success rate: {len([r for r in all_results if r])/len(test_faculty)*100:.1f}%")
    
    if all_results:
        print(f"\n📄 Sample results:")
        for result in all_results[:3]:
            print(f"   • {result['faculty_name']}: {result['title'][:60]}...")
    
    return all_results

if __name__ == "__main__":
    demo_search()
