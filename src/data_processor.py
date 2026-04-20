"""
Data processor module for user retention and conversion analysis.
Handles data loading, cleaning, and metric calculations.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Tuple, List


class DataProcessor:
    """Process user data for retention and conversion analysis."""
    
    def __init__(self, users_file: str, logins_file: str, purchases_file: str):
        """
        Initialize the data processor.
        
        Args:
            users_file: Path to users CSV file
            logins_file: Path to logins CSV file
            purchases_file: Path to purchases CSV file
        """
        self.users_file = users_file
        self.logins_file = logins_file
        self.purchases_file = purchases_file
        
        self.users_df = None
        self.logins_df = None
        self.purchases_df = None
        
    def load_data(self) -> None:
        """Load all data from CSV files."""
        print("[INFO] Loading data from CSV files...")
        
        self.users_df = pd.read_csv(self.users_file)
        self.logins_df = pd.read_csv(self.logins_file)
        self.purchases_df = pd.read_csv(self.purchases_file)
        
        # Convert date columns to datetime
        self.users_df['register_date'] = pd.to_datetime(self.users_df['register_date'])
        self.logins_df['login_date'] = pd.to_datetime(self.logins_df['login_date'])
        self.purchases_df['purchase_date'] = pd.to_datetime(self.purchases_df['purchase_date'])
        
        # Extract date only (remove time)
        self.users_df['register_date_only'] = self.users_df['register_date'].dt.date
        self.logins_df['login_date_only'] = self.logins_df['login_date'].dt.date
        self.purchases_df['purchase_date_only'] = self.purchases_df['purchase_date'].dt.date
        
        print(f"[INFO] Loaded {len(self.users_df)} users, {len(self.logins_df)} logins, {len(self.purchases_df)} purchases")
    
    def get_daily_registration(self) -> pd.DataFrame:
        """
        Calculate daily user registration counts.
        
        Returns:
            DataFrame with register_date and count columns
        """
        daily_reg = self.users_df.groupby('register_date_only').size().reset_index(name='count')
        daily_reg = daily_reg.sort_values('register_date_only')
        return daily_reg
    
    def calculate_conversion_rate(self, days: int) -> pd.DataFrame:
        """
        Calculate conversion rate for users within specified days after registration.
        
        Args:
            days: Number of days to analyze (e.g., 7 or 15)
            
        Returns:
            DataFrame with day and conversion_rate columns
        """
        results = []
        
        for day in range(1, days + 1):
            converted_count = 0
            total_users = len(self.users_df)
            
            for _, user in self.users_df.iterrows():
                user_id = user['user_id']
                register_date = user['register_date']
                
                # Calculate the deadline for conversion
                deadline = register_date + timedelta(days=day)
                
                # Check if user made a purchase within the deadline
                user_purchases = self.purchases_df[
                    (self.purchases_df['user_id'] == user_id) &
                    (self.purchases_df['purchase_date'] <= deadline)
                ]
                
                if len(user_purchases) > 0:
                    converted_count += 1
            
            conversion_rate = converted_count / total_users if total_users > 0 else 0
            results.append({
                'day': day,
                'conversion_rate': conversion_rate,
                'converted_users': converted_count,
                'total_users': total_users
            })
        
        return pd.DataFrame(results)
    
    def calculate_retention_rate(self, days: int = 7) -> pd.DataFrame:
        """
        Calculate retention rate for users within specified days after registration.
        
        Args:
            days: Number of days to analyze (e.g., 7)
            
        Returns:
            DataFrame with day and retention_rate columns
        """
        results = []
        
        for day in range(1, days + 1):
            retained_count = 0
            total_users = len(self.users_df)
            
            for _, user in self.users_df.iterrows():
                user_id = user['user_id']
                register_date = user['register_date']
                
                # Calculate the deadline for retention check
                deadline = register_date + timedelta(days=day)
                
                # Check if user logged in within the deadline
                user_logins = self.logins_df[
                    (self.logins_df['user_id'] == user_id) &
                    (self.logins_df['login_date'] <= deadline)
                ]
                
                if len(user_logins) > 0:
                    retained_count += 1
            
            retention_rate = retained_count / total_users if total_users > 0 else 0
            results.append({
                'day': day,
                'retention_rate': retention_rate,
                'retained_users': retained_count,
                'total_users': total_users
            })
        
        return pd.DataFrame(results)
    
    def get_summary_stats(self) -> Dict:
        """
        Get summary statistics for the report.
        
        Returns:
            Dictionary with summary statistics
        """
        total_users = len(self.users_df)
        total_logins = len(self.logins_df)
        total_purchases = len(self.purchases_df)
        
        # Date range
        start_date = self.users_df['register_date'].min()
        end_date = self.users_df['register_date'].max()
        
        # Users with at least one purchase
        users_with_purchase = self.purchases_df['user_id'].nunique()
        purchase_rate = users_with_purchase / total_users if total_users > 0 else 0
        
        # Users with at least one login
        users_with_login = self.logins_df['user_id'].nunique()
        login_rate = users_with_login / total_users if total_users > 0 else 0
        
        return {
            'total_users': total_users,
            'total_logins': total_logins,
            'total_purchases': total_purchases,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'users_with_purchase': users_with_purchase,
            'purchase_rate': purchase_rate,
            'users_with_login': users_with_login,
            'login_rate': login_rate
        }
