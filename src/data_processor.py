import pandas as pd
import os
from datetime import datetime, timedelta


class DataProcessor:
    """
    Data processing class for user retention and conversion analysis.
    Handles loading, cleaning, and transforming user behavior data.
    """
    
    def __init__(self, data_dir='data'):
        """
        Initialize DataProcessor with data directory.
        
        Args:
            data_dir: Directory containing the data files
        """
        self.data_dir = data_dir
        self.df_registrations = None
        self.df_logins = None
        self.df_purchases = None
        self.df_combined = None
        
    def load_data(self):
        """
        Load all data files from the data directory.
        """
        print("Loading data files...")
        
        registrations_path = os.path.join(self.data_dir, 'registrations.csv')
        logins_path = os.path.join(self.data_dir, 'logins.csv')
        purchases_path = os.path.join(self.data_dir, 'purchases.csv')
        
        self.df_registrations = pd.read_csv(registrations_path, parse_dates=['register_date'])
        self.df_logins = pd.read_csv(logins_path, parse_dates=['login_time'])
        self.df_purchases = pd.read_csv(purchases_path, parse_dates=['purchase_time'])
        
        print(f"Loaded {len(self.df_registrations)} registration records")
        print(f"Loaded {len(self.df_logins)} login records")
        print(f"Loaded {len(self.df_purchases)} purchase records")
        
    def prepare_combined_data(self):
        """
        Combine all user data into a single DataFrame for analysis.
        Calculate days to first login and days to first purchase for each user.
        """
        print("Preparing combined dataset...")
        
        first_logins = self.df_logins.groupby('user_id')['login_time'].min().reset_index()
        first_logins.columns = ['user_id', 'first_login_time']
        
        first_purchases = self.df_purchases.groupby('user_id')['purchase_time'].min().reset_index()
        first_purchases.columns = ['user_id', 'first_purchase_time']
        
        self.df_combined = self.df_registrations.merge(
            first_logins, on='user_id', how='left'
        ).merge(
            first_purchases, on='user_id', how='left'
        )
        
        self.df_combined['days_to_first_login'] = (
            self.df_combined['first_login_time'] - self.df_combined['register_date']
        ).dt.total_seconds() / 86400
        
        self.df_combined['days_to_first_purchase'] = (
            self.df_combined['first_purchase_time'] - self.df_combined['register_date']
        ).dt.total_seconds() / 86400
        
        print(f"Prepared combined data for {len(self.df_combined)} users")
        
    def get_daily_registrations(self):
        """
        Get daily registration counts.
        
        Returns:
            DataFrame with date and count of registrations
        """
        daily_reg = self.df_registrations.copy()
        daily_reg['date'] = daily_reg['register_date'].dt.date
        daily_counts = daily_reg.groupby('date').size().reset_index(name='count')
        daily_counts = daily_counts.sort_values('date')
        return daily_counts
    
    def get_7day_conversion_rates(self):
        """
        Calculate conversion rates for each day within 7 days after registration.
        
        Returns:
            Dictionary with day as key and conversion rate as value
        """
        total_users = len(self.df_combined)
        conversion_rates = {}
        
        for day in range(1, 8):
            converted_users = len(self.df_combined[
                (self.df_combined['days_to_first_purchase'] <= day) &
                (self.df_combined['days_to_first_purchase'] >= 0)
            ])
            conversion_rates[day] = converted_users / total_users if total_users > 0 else 0
            
        return conversion_rates
    
    def get_15day_conversion_rates(self):
        """
        Calculate cumulative conversion rates within 15 days after registration.
        
        Returns:
            Dictionary with day as key and cumulative conversion rate as value
        """
        total_users = len(self.df_combined)
        conversion_rates = {}
        
        days_to_analyze = [1, 3, 5, 7, 10, 15]
        for day in days_to_analyze:
            converted_users = len(self.df_combined[
                (self.df_combined['days_to_first_purchase'] <= day) &
                (self.df_combined['days_to_first_purchase'] >= 0)
            ])
            conversion_rates[day] = converted_users / total_users if total_users > 0 else 0
            
        return conversion_rates
    
    def get_7day_retention_rates(self):
        """
        Calculate retention rates for each day within 7 days after registration.
        Retention = user logged in at least once on or before that day.
        
        Returns:
            Dictionary with day as key and retention rate as value
        """
        total_users = len(self.df_combined)
        retention_rates = {}
        
        for day in range(1, 8):
            retained_users = len(self.df_combined[
                (self.df_combined['days_to_first_login'] <= day) &
                (self.df_combined['days_to_first_login'] >= 0)
            ])
            retention_rates[day] = retained_users / total_users if total_users > 0 else 0
            
        return retention_rates
    
    def get_summary_statistics(self):
        """
        Get summary statistics of the analysis.
        
        Returns:
            Dictionary containing key metrics
        """
        total_users = len(self.df_combined)
        users_with_purchase = len(self.df_combined[self.df_combined['days_to_first_purchase'] >= 0])
        users_with_login = len(self.df_combined[self.df_combined['days_to_first_login'] >= 0])
        
        avg_days_to_purchase = self.df_combined[self.df_combined['days_to_first_purchase'] >= 0]['days_to_first_purchase'].mean()
        avg_days_to_login = self.df_combined[self.df_combined['days_to_first_login'] >= 0]['days_to_first_login'].mean()
        
        return {
            'total_users': total_users,
            'users_with_purchase': users_with_purchase,
            'users_with_login': users_with_login,
            'overall_conversion_rate': users_with_purchase / total_users if total_users > 0 else 0,
            'overall_retention_rate': users_with_login / total_users if total_users > 0 else 0,
            'avg_days_to_purchase': avg_days_to_purchase,
            'avg_days_to_login': avg_days_to_login
        }
