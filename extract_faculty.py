#!/usr/bin/env python3
"""
Extract complete faculty list from CSRR website
"""

import requests
from bs4 import BeautifulSoup
import re

def extract_faculty_names():
    url = 'https://csrr.rutgers.edu/about/faculty-affiliates/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Get all text content
    text = soup.get_text()
    lines = text.split('\n')
    
    faculty_names = []
    
    # Look for names that appear before "Professor" or other academic titles
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        # Check if next line contains academic title indicators
        next_line = lines[i+1].strip() if i+1 < len(lines) else ""
        
        # Look for names that precede academic titles
        if any(title in next_line.lower() for title in [
            'professor', 'associate professor', 'assistant professor', 
            'clinical professor', 'emeritus professor', 'visiting professor',
            'distinguished professor', 'lecturer', 'instructor'
        ]):
            # Clean up the name
            name = line.strip()
            # Remove common prefixes/suffixes
            name = re.sub(r'^(Dr\.|Prof\.|Professor)\s+', '', name)
            name = re.sub(r'\s+(Jr\.|Sr\.|II|III|IV)$', r' \1', name)
            
            # Check if it looks like a name (has at least 2 words, not too long)
            if len(name.split()) >= 2 and len(name) < 50 and not any(x in name.lower() for x in ['university', 'college', 'school', 'department']):
                faculty_names.append(name)
    
    # Also look for names in specific patterns from the HTML structure
    # Find all h3/h4 elements or similar that might contain names
    for element in soup.find_all(['h3', 'h4', 'h5', 'strong', 'b']):
        text = element.get_text().strip()
        if text and len(text.split()) >= 2 and len(text) < 50:
            # Check if it looks like a name
            words = text.split()
            if all(word[0].isupper() for word in words if word):  # All words start with capital
                faculty_names.append(text)
    
    # Remove duplicates and sort
    faculty_names = sorted(list(set(faculty_names)))
    
    # Filter out non-faculty entries that shouldn't be treated as names
    non_faculty_terms = [
        'LATEST NEWS', 'BREAKING NEWS', 'NEWS UPDATE', 'FEATURED', 'SPOTLIGHT',
        'ANNOUNCEMENT', 'ALERT', 'NOTICE', 'UPDATE', 'PRESS RELEASE',
        'MEDIA', 'CONTACT', 'INFORMATION', 'ABOUT', 'HOME', 'SEARCH',
        'MENU', 'NAVIGATION', 'FOOTER', 'HEADER', 'SIDEBAR', 'MORE INFO',
        'LEARN MORE', 'READ MORE', 'CLICK HERE', 'VIEW ALL', 'SEE ALL'
    ]
    
    filtered_faculty = []
    for name in faculty_names:
        # Skip if it's a non-faculty term
        if name.upper() in non_faculty_terms:
            print(f"  ⚠️  Filtered out non-faculty entry: {name}")
            continue
            
        # Skip if it contains obvious non-name patterns
        if any(term in name.upper() for term in ['NEWS', 'UPDATE', 'ALERT', 'CLICK', 'VIEW', 'READ']):
            print(f"  ⚠️  Filtered out non-name pattern: {name}")
            continue
            
        # Keep if it looks like a proper name (first/last name pattern)
        name_parts = name.split()
        if len(name_parts) >= 2 and all(part[0].isupper() and part[1:].islower() for part in name_parts if part.isalpha()):
            filtered_faculty.append(name)
    
    print(f"Filtered {len(faculty_names) - len(filtered_faculty)} non-faculty entries")
    return filtered_faculty

if __name__ == "__main__":
    faculty_list = extract_faculty_names()
    print(f"Found {len(faculty_list)} faculty members:")
    for i, name in enumerate(faculty_list, 1):
        print(f"{i:3d}. {name}")
