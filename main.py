#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
User Retention and Conversion Analysis Program.
This program analyzes user behavior data including:
- Daily registrations
- 7-day and 15-day conversion rates
- 7-day retention rates
Outputs analysis results as a PDF report.

Note: Test data generation is NOT part of this analysis program.
Please use generate_test_data.py separately to generate test data.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_processor import DataProcessor
from report_generator import ReportGenerator


def run_analysis():
    """
    Main function to run the complete analysis workflow.
    """
    print("=" * 60)
    print("Starting User Retention and Conversion Analysis")
    print("=" * 60)
    
    processor = DataProcessor(data_dir='data')
    processor.load_data()
    processor.prepare_combined_data()
    
    summary = processor.get_summary_statistics()
    print("\n" + "=" * 60)
    print("Analysis Summary:")
    print("=" * 60)
    print(f"Total users: {summary['total_users']}")
    print(f"Users with login: {summary['users_with_login']}")
    print(f"Users with purchase: {summary['users_with_purchase']}")
    print(f"Overall retention rate: {summary['overall_retention_rate']*100:.1f}%")
    print(f"Overall conversion rate: {summary['overall_conversion_rate']*100:.1f}%")
    print(f"Average days to first login: {summary['avg_days_to_login']:.1f} days")
    print(f"Average days to first purchase: {summary['avg_days_to_purchase']:.1f} days")
    print("=" * 60)
    
    report_generator = ReportGenerator(output_dir='output')
    report_path = report_generator.generate_report(processor)
    
    print("\nAnalysis completed successfully!")
    print(f"Report saved to: {report_path}")
    
    return True


if __name__ == '__main__':
    run_analysis()
