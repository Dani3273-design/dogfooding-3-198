"""
Test data generator for user retention and conversion analysis.
Generates simulated user registration, login, and purchase data.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os


def generate_test_data(output_dir: str = "data"):
    """
    Generate test data for user retention and conversion analysis.
    
    Args:
        output_dir: Directory to save generated data files
    """
    print("[INFO] Starting test data generation...")
    
    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Randomly select a month
    year = 2024
    month = random.randint(1, 12)
    print(f"[INFO] Generating data for {year}-{month:02d}")
    
    # Calculate days in month
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    days_in_month = (next_month - datetime(year, month, 1)).days
    
    # Generate user registration data (200 users)
    print("[INFO] Generating user registration data...")
    users_df = generate_users(year, month, days_in_month)
    users_file = os.path.join(output_dir, "users.csv")
    users_df.to_csv(users_file, index=False, encoding='utf-8')
    print(f"[INFO] Generated {len(users_df)} users, saved to {users_file}")
    
    # Generate login records (500 logins)
    print("[INFO] Generating login records...")
    logins_df = generate_logins(users_df, year, month, days_in_month, 500)
    logins_file = os.path.join(output_dir, "logins.csv")
    logins_df.to_csv(logins_file, index=False, encoding='utf-8')
    print(f"[INFO] Generated {len(logins_df)} login records, saved to {logins_file}")
    
    # Generate purchase records (400 purchases)
    print("[INFO] Generating purchase records...")
    purchases_df = generate_purchases(users_df, year, month, days_in_month, 400)
    purchases_file = os.path.join(output_dir, "purchases.csv")
    purchases_df.to_csv(purchases_file, index=False, encoding='utf-8')
    print(f"[INFO] Generated {len(purchases_df)} purchase records, saved to {purchases_file}")
    
    print("[INFO] Test data generation completed successfully!")
    return users_file, logins_file, purchases_file


def generate_users(year: int, month: int, days_in_month: int) -> pd.DataFrame:
    """
    Generate user registration data.
    
    Args:
        year: Year for registration
        month: Month for registration
        days_in_month: Number of days in the month
        
    Returns:
        DataFrame with user_id and register_date columns
    """
    users = []
    user_id_start = 10001
    
    for i in range(200):
        user_id = user_id_start + i
        # Generate registration date with bias towards weekends and evening hours
        register_date = generate_biased_datetime(year, month, days_in_month)
        users.append({
            'user_id': user_id,
            'register_date': register_date.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return pd.DataFrame(users)


def generate_logins(users_df: pd.DataFrame, year: int, month: int, 
                    days_in_month: int, count: int) -> pd.DataFrame:
    """
    Generate user login records.
    
    Args:
        users_df: DataFrame with user registration data
        year: Year for login dates
        month: Month for login dates
        days_in_month: Number of days in the month
        count: Number of login records to generate
        
    Returns:
        DataFrame with user_id and login_date columns
    """
    logins = []
    user_ids = users_df['user_id'].tolist()
    
    # Parse user registration dates
    user_register_dates = {}
    for _, row in users_df.iterrows():
        user_register_dates[row['user_id']] = datetime.strptime(
            row['register_date'], '%Y-%m-%d %H:%M:%S'
        )
    
    for _ in range(count):
        user_id = random.choice(user_ids)
        register_date = user_register_dates[user_id]
        
        # Login date should be on or after registration date
        max_day = min(days_in_month, register_date.day + 30)  # Within 30 days after registration
        if max_day <= register_date.day:
            max_day = days_in_month
        
        # Generate login date with bias
        login_date = generate_biased_datetime(year, month, days_in_month, 
                                              min_day=register_date.day)
        
        logins.append({
            'user_id': user_id,
            'login_date': login_date.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return pd.DataFrame(logins)


def generate_purchases(users_df: pd.DataFrame, year: int, month: int,
                       days_in_month: int, count: int) -> pd.DataFrame:
    """
    Generate user purchase records.
    
    Args:
        users_df: DataFrame with user registration data
        year: Year for purchase dates
        month: Month for purchase dates
        days_in_month: Number of days in the month
        count: Number of purchase records to generate
        
    Returns:
        DataFrame with user_id and purchase_date columns
    """
    purchases = []
    user_ids = users_df['user_id'].tolist()
    
    # Parse user registration dates
    user_register_dates = {}
    for _, row in users_df.iterrows():
        user_register_dates[row['user_id']] = datetime.strptime(
            row['register_date'], '%Y-%m-%d %H:%M:%S'
        )
    
    for _ in range(count):
        user_id = random.choice(user_ids)
        register_date = user_register_dates[user_id]
        
        # Purchase date should be on or after registration date
        max_day = min(days_in_month, register_date.day + 30)
        if max_day <= register_date.day:
            max_day = days_in_month
        
        # Generate purchase date with bias
        purchase_date = generate_biased_datetime(year, month, days_in_month,
                                                 min_day=register_date.day)
        
        purchases.append({
            'user_id': user_id,
            'purchase_date': purchase_date.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return pd.DataFrame(purchases)


def generate_biased_datetime(year: int, month: int, days_in_month: int,
                             min_day: int = 1) -> datetime:
    """
    Generate a datetime with bias towards weekends and evening hours.
    
    Args:
        year: Year
        month: Month
        days_in_month: Number of days in the month
        min_day: Minimum day of month
        
    Returns:
        Biased datetime object
    """
    # Generate day with bias towards weekends
    days = list(range(min_day, days_in_month + 1))
    weights = []
    
    for day in days:
        date = datetime(year, month, day)
        weekday = date.weekday()
        # Weekend (5=Saturday, 6=Sunday) has higher weight
        if weekday >= 5:
            weights.append(3.0)
        # Friday evening effect
        elif weekday == 4:
            weights.append(2.0)
        else:
            weights.append(1.0)
    
    day = random.choices(days, weights=weights, k=1)[0]
    
    # Generate hour with bias towards evening and lunch time
    hours = list(range(0, 24))
    hour_weights = []
    
    for hour in hours:
        if 12 <= hour <= 14:  # Lunch time
            hour_weights.append(2.5)
        elif 18 <= hour <= 22:  # Evening leisure time
            hour_weights.append(3.0)
        elif 9 <= hour <= 11:  # Morning work time
            hour_weights.append(1.5)
        elif 0 <= hour <= 6:  # Late night / early morning
            hour_weights.append(0.3)
        else:
            hour_weights.append(1.0)
    
    hour = random.choices(hours, weights=hour_weights, k=1)[0]
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    
    return datetime(year, month, day, hour, minute, second)


if __name__ == "__main__":
    generate_test_data()
