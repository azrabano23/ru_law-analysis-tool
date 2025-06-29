import pandas as pd
import re
from datetime import datetime
from pathlib import Path

# Define a function for analysis
def analyze_csrr_publications(input_path, output_path):
    with open(input_path, 'r') as f:
        content = f.read()

    may_2024_data = []
    lines = content.split('\n')
      
    current_faculty = None
    for i, line in enumerate(lines):
        line = line.strip()
          
        if line and not line.startswith('•') and not 'http' in line and not line.startswith('Since') and not line.isdigit():
            if len(line) > 3 and not re.search(r'\d{4}', line) and not line.startswith('Op-Eds'):
                current_faculty = line
          
        elif line.startswith('•') and re.search(r'May.*2024|2024.*May|2024/05|05.*2024', line, re.IGNORECASE):
            entry_parts = line[1:].strip()  
            url_match = re.search(r'(https?://[^\s,]+)', entry_parts)
            url = url_match.group(1) if url_match else 'N/A'
            entry_no_url = re.sub(r'https?://[^\s,]+', '', entry_parts).strip()
            date_match = re.search(r'(May\s+\d{1,2},?\s+2024)', entry_no_url, re.IGNORECASE)
            date = date_match.group(1) if date_match else 'May 2024'
            title_match = re.search(r'^([^,]+)', entry_no_url)
            title = title_match.group(1).strip() if title_match else entry_no_url[:100]
            content_type = 'article'
            if any(term in entry_parts.lower() for term in ['op-ed', 'opinion', 'commentary']):
                content_type = 'op-ed'
            elif any(term in entry_parts.lower() for term in ['interview', 'talks with', 'speaks to']):
                content_type = 'interview'
            elif any(term in entry_parts.lower() for term in ['youtube', 'podcast', 'video']):
                content_type = 'video/podcast'
            elif any(term in entry_parts.lower() for term in ['tv', 'television', 'cnn', 'msnbc', 'bbc']):
                content_type = 'tv'
            source_match = re.search(r',\s*([^,]+),\s*' + re.escape(date), entry_no_url, re.IGNORECASE)
            if not source_match:
                source_match = re.search(r',\s*([^,]+)', entry_no_url)
            source = source_match.group(1).strip() if source_match else 'Unknown'
            
            may_2024_data.append({
                'Faculty Name': current_faculty or 'Unknown',
                'Content Type': content_type,
                'Title': title,
                'Source': source,
                'Date': date,
                'URL': url,
                'Date Found': datetime.now().strftime('%Y-%m-%d'),
                'Search Term': 'Manual extraction',
                'Description': entry_parts[:200] + '...' if len(entry_parts) > 200 else entry_parts
            })

    df = pd.DataFrame(may_2024_data)
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='May 2024 Results', index=False)
        faculty_summary = df.groupby('Faculty Name').agg({
            'Title': 'count',
            'Content Type': lambda x: ', '.join(x.unique())
        }).rename(columns={'Title': 'Number of Publications'})
        faculty_summary.to_excel(writer, sheet_name='Faculty Summary')
        content_summary = df.groupby('Content Type').agg({
            'Title': 'count',
            'Faculty Name': lambda x: ', '.join(x.unique()[:5])
        }).rename(columns={'Title': 'Count', 'Faculty Name': 'Sample Faculty'})
        content_summary.to_excel(writer, sheet_name='Content Type Summary')
    

if __name__ == "__main__":
    input_file = "data/5-31-25_Op-Ed_CSRR_Affiliates.txt"
    output_file = f"reports/CSRR_Faculty_Publications_May_2024_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    Path("reports").mkdir(parents=True, exist_ok=True)
    analyze_csrr_publications(input_file, output_file)

