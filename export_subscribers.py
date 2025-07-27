#!/usr/bin/env python3

"""
CSRR Mailing List Subscriber Export Tool

This script connects to the Supabase database and exports all mailing list
subscribers to an Excel file for use with the monthly report distribution.

Usage:
    python3 export_subscribers.py

Requirements:
    - SUPABASE_URL environment variable
    - SUPABASE_SERVICE_KEY environment variable
    - pip install supabase pandas openpyxl python-dotenv
"""

import os
import pandas as pd
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def connect_to_supabase():
    """Initialize Supabase client"""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    
    if not url or not key:
        raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_KEY environment variables")
    
    return create_client(url, key)

def fetch_subscribers(supabase: Client):
    """Fetch all subscribers from the mailing_list table"""
    try:
        response = supabase.table('mailing_list').select('*').order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Error fetching subscribers: {e}")
        return []

def export_to_excel(subscribers, filename=None):
    """Export subscribers to Excel file"""
    if not subscribers:
        print("No subscribers found to export.")
        return
    
    # Create DataFrame
    df = pd.DataFrame(subscribers)
    
    # Rename columns for better readability
    column_mapping = {
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'email': 'Email Address',
        'organization': 'Organization',
        'title': 'Title',
        'created_at': 'Subscription Date'
    }
    
    df = df.rename(columns=column_mapping)
    
    # Format date column
    if 'Subscription Date' in df.columns:
        df['Subscription Date'] = pd.to_datetime(df['Subscription Date']).dt.strftime('%Y-%m-%d')
    
    # Reorder columns
    column_order = ['First Name', 'Last Name', 'Email Address', 'Organization', 'Title', 'Subscription Date']
    df = df[column_order]
    
    # Generate filename if not provided
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        filename = f'CSRR_Mailing_List_Subscribers_{timestamp}.xlsx'
    
    # Export to Excel
    df.to_excel(filename, index=False, engine='openpyxl')
    
    print(f"Successfully exported {len(subscribers)} subscribers to {filename}")
    return filename

def main():
    """Main function"""
    try:
        # Connect to Supabase
        supabase = connect_to_supabase()
        
        # Fetch subscribers
        print("Fetching subscribers from database...")
        subscribers = fetch_subscribers(supabase)
        
        # Export to Excel
        filename = export_to_excel(subscribers)
        
        # Print summary
        print(f"\\nExport Summary:")
        print(f"- Total subscribers: {len(subscribers)}")
        print(f"- Export file: {filename}")
        print(f"- File ready for email distribution")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
