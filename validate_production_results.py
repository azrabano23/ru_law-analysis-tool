#!/usr/bin/env python3
"""
CSRR Faculty Media Search - PRODUCTION VALIDATION SCRIPT
Comprehensive validation for production results to ensure boss requirements are met
Author: Azra Bano
Date: July 26, 2025
"""

import pandas as pd
from docx import Document
import requests
import re
from typing import Dict, List, Tuple
import random

class ProductionValidator:
    """Validates production results against boss requirements"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        # Boss requirements checklist
        self.required_columns = ['Faculty Name', 'Author', 'Title', 'Source', 'URL']
        self.trusted_sources = {
            'New York Times', 'Washington Post', 'CNN', 'Al Jazeera', 'BBC', 
            'NPR', 'Reuters', 'Politico', 'The Atlantic', 'The Guardian', 
            'HuffPost', 'Slate', 'Vox', 'Axios', 'Associated Press'
        }
    
    def load_and_analyze_excel(self, filename: str) -> Dict:
        """Load Excel file and perform comprehensive analysis"""
        try:
            df = pd.read_excel(filename)
            
            analysis = {
                'filename': filename,
                'total_entries': len(df),
                'columns': list(df.columns),
                'faculty_count': df['Faculty Name'].nunique() if 'Faculty Name' in df.columns else 0,
                'dataframe': df
            }
            
            print(f"📊 LOADED: {filename}")
            print(f"   Entries: {analysis['total_entries']}")
            print(f"   Faculty: {analysis['faculty_count']}")
            print(f"   Columns: {analysis['columns']}")
            
            return analysis
            
        except Exception as e:
            print(f"❌ Error loading {filename}: {e}")
            return None
    
    def check_format_compliance(self, analysis: Dict) -> List[str]:
        """Check if format meets boss requirements"""
        issues = []
        df = analysis['dataframe']
        
        # Check required columns
        missing_cols = [col for col in self.required_columns if col not in analysis['columns']]
        if missing_cols:
            issues.append(f"Missing required columns: {missing_cols}")
        
        # Check Author = Faculty Name requirement
        if 'Author' in df.columns and 'Faculty Name' in df.columns:
            author_mismatch = df[df['Author'] != df['Faculty Name']]
            if len(author_mismatch) > 0:
                issues.append(f"Author ≠ Faculty Name in {len(author_mismatch)} entries")
        
        # Check for empty critical fields
        if 'Title' in df.columns:
            empty_titles = df['Title'].isna().sum()
            if empty_titles > 0:
                issues.append(f"{empty_titles} entries have empty titles")
        
        if 'URL' in df.columns:
            empty_urls = df['URL'].isna().sum()
            if empty_urls > 0:
                issues.append(f"{empty_urls} entries have empty URLs")
        
        return issues
    
    def validate_source_quality(self, analysis: Dict) -> Dict:
        """Validate source quality and distribution"""
        df = analysis['dataframe']
        
        if 'Source' not in df.columns:
            return {'error': 'No Source column found'}
        
        source_stats = df['Source'].value_counts()
        
        # Calculate trusted vs unknown sources
        trusted_count = sum(count for source, count in source_stats.items() 
                          if source in self.trusted_sources)
        unknown_count = source_stats.get('Unknown', 0)
        
        quality_score = trusted_count / len(df) * 100 if len(df) > 0 else 0
        
        return {
            'source_distribution': dict(source_stats),
            'trusted_sources': trusted_count,
            'unknown_sources': unknown_count,
            'quality_score': quality_score,
            'total_entries': len(df)
        }
    
    def validate_faculty_attribution(self, analysis: Dict, sample_size: int = 20) -> Dict:
        """Validate that faculty are actually mentioned in their attributed articles"""
        df = analysis['dataframe']
        
        if len(df) == 0:
            return {'error': 'No data to validate'}
        
        # Sample entries for validation
        sample_size = min(sample_size, len(df))
        sample_df = df.sample(n=sample_size, random_state=42)
        
        validation_results = []
        
        for idx, row in sample_df.iterrows():
            faculty_name = row['Faculty Name']
            title = row['Title']
            url = row.get('URL', 'N/A')
            source = row.get('Source', 'Unknown')
            
            # Check if faculty name appears in title
            faculty_in_title = self._check_name_in_text(faculty_name, title)
            
            validation_results.append({
                'faculty_name': faculty_name,
                'title': title[:100] + "..." if len(title) > 100 else title,
                'source': source,
                'url': url,
                'faculty_in_title': faculty_in_title,
                'row_index': idx
            })
        
        # Calculate accuracy statistics
        accurate_count = sum(1 for r in validation_results if r['faculty_in_title'])
        accuracy_rate = accurate_count / len(validation_results) * 100
        
        return {
            'sample_size': len(validation_results),
            'accurate_attributions': accurate_count,
            'accuracy_rate': accuracy_rate,
            'validation_details': validation_results
        }
    
    def _check_name_in_text(self, faculty_name: str, text: str) -> bool:
        """Check if faculty name appears in text"""
        if not text or pd.isna(text):
            return False
            
        text_lower = str(text).lower()
        faculty_lower = faculty_name.lower()
        
        # Check for full name
        if faculty_lower in text_lower:
            return True
        
        # Check for name parts
        name_parts = faculty_lower.split()
        if len(name_parts) >= 2:
            last_name = name_parts[-1]
            first_name = name_parts[0]
            
            # Both first and last names should appear
            return last_name in text_lower and first_name in text_lower
        
        return False
    
    def check_nausheen_husain_issue(self, analysis: Dict) -> Dict:
        """Specifically check for the Nausheen Husain misattribution issue"""
        df = analysis['dataframe']
        
        # Find entries for Nausheen Husain
        nausheen_entries = df[df['Faculty Name'].str.contains('Nausheen Husain', case=False, na=False)]
        
        # Check for misattribution (Nausheen Husain mentioned under other faculty)
        other_entries = df[~df['Faculty Name'].str.contains('Nausheen Husain', case=False, na=False)]
        
        misattributed = []
        for idx, row in other_entries.iterrows():
            title = str(row.get('Title', ''))
            snippet = str(row.get('Snippet', ''))
            
            if ('nausheen husain' in title.lower() or 'nausheen husain' in snippet.lower()):
                misattributed.append({
                    'attributed_to': row['Faculty Name'],
                    'title': title[:100] + "..." if len(title) > 100 else title,
                    'row_index': idx
                })
        
        return {
            'nausheen_entries_count': len(nausheen_entries),
            'misattributed_entries': misattributed,
            'issue_detected': len(misattributed) > 0
        }
    
    def generate_comprehensive_report(self, filename: str) -> None:
        """Generate comprehensive validation report"""
        print("=" * 70)
        print("🔍 CSRR PRODUCTION RESULTS VALIDATION")
        print("=" * 70)
        
        # Load and analyze
        analysis = self.load_and_analyze_excel(filename)
        if not analysis:
            return
        
        print("\n📋 FORMAT COMPLIANCE CHECK")
        print("-" * 40)
        format_issues = self.check_format_compliance(analysis)
        
        if format_issues:
            print("❌ FORMAT ISSUES DETECTED:")
            for issue in format_issues:
                print(f"   • {issue}")
        else:
            print("✅ All format requirements met")
        
        print("\n📰 SOURCE QUALITY ANALYSIS")
        print("-" * 40)
        source_quality = self.validate_source_quality(analysis)
        
        if 'error' in source_quality:
            print(f"❌ {source_quality['error']}")
        else:
            print(f"Quality Score: {source_quality['quality_score']:.1f}%")
            print(f"Trusted Sources: {source_quality['trusted_sources']}")
            print(f"Unknown Sources: {source_quality['unknown_sources']}")
            
            print(f"\nTop Sources:")
            for source, count in list(source_quality['source_distribution'].items())[:10]:
                status = "✅" if source in self.trusted_sources else "❓"
                print(f"   {status} {source}: {count}")
        
        print("\n🎯 FACULTY ATTRIBUTION VALIDATION")
        print("-" * 40)
        attribution_check = self.validate_faculty_attribution(analysis)
        
        if 'error' in attribution_check:
            print(f"❌ {attribution_check['error']}")
        else:
            print(f"Sample Size: {attribution_check['sample_size']}")
            print(f"Accurate Attributions: {attribution_check['accurate_attributions']}")
            print(f"Accuracy Rate: {attribution_check['accuracy_rate']:.1f}%")
            
            # Show problematic entries
            problematic = [r for r in attribution_check['validation_details'] 
                          if not r['faculty_in_title']]
            
            if problematic:
                print(f"\n⚠️  ATTRIBUTION ISSUES ({len(problematic)} found):")
                for item in problematic[:5]:  # Show first 5
                    print(f"   • {item['faculty_name']} → '{item['title']}'")
                    print(f"     Source: {item['source']}")
                if len(problematic) > 5:
                    print(f"   ... and {len(problematic) - 5} more")
        
        print("\n🔍 NAUSHEEN HUSAIN ISSUE CHECK")
        print("-" * 40)
        nausheen_check = self.check_nausheen_husain_issue(analysis)
        
        print(f"Nausheen Husain entries: {nausheen_check['nausheen_entries_count']}")
        
        if nausheen_check['issue_detected']:
            print(f"❌ MISATTRIBUTION DETECTED:")
            for item in nausheen_check['misattributed_entries']:
                print(f"   • Listed under: {item['attributed_to']}")
                print(f"     Title: {item['title']}")
        else:
            print("✅ No Nausheen Husain misattribution found")
        
        print("\n" + "=" * 70)
        print("📊 OVERALL ASSESSMENT")
        print("=" * 70)
        
        # Calculate overall score
        total_issues = len(format_issues)
        attribution_score = attribution_check.get('accuracy_rate', 0)
        source_score = source_quality.get('quality_score', 0)
        nausheen_issue = nausheen_check.get('issue_detected', False)
        
        overall_score = (attribution_score + source_score) / 2
        
        if nausheen_issue:
            overall_score -= 20
        if total_issues > 0:
            overall_score -= (total_issues * 10)
        
        overall_score = max(0, overall_score)
        
        print(f"Overall Quality Score: {overall_score:.1f}/100")
        
        if overall_score >= 90:
            print("🎉 EXCELLENT - Ready for boss submission")
        elif overall_score >= 75:
            print("✅ GOOD - Minor issues to address")
        elif overall_score >= 60:
            print("⚠️  NEEDS IMPROVEMENT - Several issues found")
        else:
            print("❌ POOR - Major issues require fixing")
        
        print("\n💡 RECOMMENDATIONS:")
        
        if format_issues:
            print("• Fix format compliance issues")
        if attribution_score < 80:
            print("• Improve faculty attribution accuracy")
        if source_score < 70:
            print("• Include more trusted news sources")
        if nausheen_issue:
            print("• Fix Nausheen Husain misattribution")
        if overall_score >= 90:
            print("• Results meet boss requirements - ready to submit!")

def main():
    """Main execution function"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 validate_production_results.py <excel_file>")
        return
    
    filename = sys.argv[1]
    validator = ProductionValidator()
    validator.generate_comprehensive_report(filename)

if __name__ == "__main__":
    main()
