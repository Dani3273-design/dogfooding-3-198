"""
Test data generator script for user retention and conversion analysis.
This script generates simulated user registration, login, and purchase data.
Run this script separately before running the main analysis program.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from test_data_generator import generate_test_data


def main():
    """Main function to generate test data."""
    print("=" * 60)
    print("[INFO] Test Data Generator")
    print("=" * 60)
    
    # Generate test data
    users_file, logins_file, purchases_file = generate_test_data("data")
    
    print("\n" + "=" * 60)
    print("[INFO] Test data generation completed!")
    print(f"[INFO] Users data: {users_file}")
    print(f"[INFO] Logins data: {logins_file}")
    print(f"[INFO] Purchases data: {purchases_file}")
    print("\n[INFO] Now you can run the analysis program: python main.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
