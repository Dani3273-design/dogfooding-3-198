"""
Main entry point for user retention and conversion analysis.
This script analyzes existing data and generates a PDF report.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_processor import DataProcessor
from report_generator import ReportGenerator


def main():
    """Main function to run the analysis."""
    print("=" * 60)
    print("[INFO] User Retention and Conversion Analysis Tool")
    print("=" * 60)
    
    # Data file paths
    users_file = "data/users.csv"
    logins_file = "data/logins.csv"
    purchases_file = "data/purchases.csv"
    
    # Check if data files exist
    for file_path in [users_file, logins_file, purchases_file]:
        if not os.path.exists(file_path):
            print(f"[ERROR] Data file not found: {file_path}")
            print("[INFO] Please generate test data first by running: python generate_test_data.py")
            return
    
    # Step 1: Process data
    print("\n[INFO] Step 1: Loading and processing data...")
    processor = DataProcessor(users_file, logins_file, purchases_file)
    processor.load_data()
    
    # Step 2: Generate report
    print("\n[INFO] Step 2: Generating report...")
    report_gen = ReportGenerator("output/report.pdf")
    report_path = report_gen.generate_report(processor)
    
    print("\n" + "=" * 60)
    print("[INFO] Analysis completed successfully!")
    print(f"[INFO] Report saved to: {report_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
