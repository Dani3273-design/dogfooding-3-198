#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Data Generator Script.
This script is ONLY for generating test data.
It is NOT part of the analysis program.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os


def generate_test_data(output_dir='data'):
    """
    Generate test data for user retention and conversion analysis.
    This function is for testing purposes only and is separate from the analysis program.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    random_month = random.randint(1, 12)
    year = 2024
    num_days_in_month = (datetime(year, random_month % 12 + 1, 1) - timedelta(days=1)).day
    start_date = datetime(year, random_month, 1)
    
    print(f"Generating test data for {year}-{random_month:02d}")
    
    user_ids = [f'USER_{i:04d}' for i in range(1, 201)]
    
    registrations = []
    for user_id in user_ids:
        random_day = random.randint(0, num_days_in_month - 1)
        base_date = start_date + timedelta(days=random_day)
        
        weekday = base_date.weekday()
        if weekday < 5:
            hour = random.choice([12, 13, 18, 19, 20, 21, 22])
        else:
            hour = random.randint(9, 23)
        
        minute = random.randint(0, 59)
        register_time = base_date + timedelta(hours=hour, minutes=minute)
        registrations.append({
            'user_id': user_id,
            'register_date': register_time
        })
    
    df_registrations = pd.DataFrame(registrations)
    df_registrations.to_csv(os.path.join(output_dir, 'registrations.csv'), index=False)
    print(f"Generated {len(df_registrations)} user registration records")
    
    logins = []
    for _ in range(500):
        user_id = random.choice(user_ids)
        user_register_time = df_registrations[df_registrations['user_id'] == user_id]['register_date'].iloc[0]
        
        days_after_register = random.randint(0, 60)
        base_date = user_register_time + timedelta(days=days_after_register)
        
        weekday = base_date.weekday()
        if weekday < 5:
            hour = random.choice([8, 9, 12, 13, 18, 19, 20, 21, 22])
        else:
            hour = random.randint(10, 23)
        
        minute = random.randint(0, 59)
        login_time = base_date + timedelta(hours=hour, minutes=minute)
        logins.append({
            'user_id': user_id,
            'login_time': login_time
        })
    
    df_logins = pd.DataFrame(logins)
    df_logins = df_logins.sort_values('login_time')
    df_logins.to_csv(os.path.join(output_dir, 'logins.csv'), index=False)
    print(f"Generated {len(df_logins)} user login records")
    
    purchases = []
    for _ in range(400):
        user_id = random.choice(user_ids)
        user_register_time = df_registrations[df_registrations['user_id'] == user_id]['register_date'].iloc[0]
        
        days_after_register = random.randint(0, 60)
        base_date = user_register_time + timedelta(days=days_after_register)
        
        weekday = base_date.weekday()
        if weekday < 5:
            hour = random.choice([12, 13, 19, 20, 21, 22])
        else:
            hour = random.randint(11, 22)
        
        minute = random.randint(0, 59)
        purchase_time = base_date + timedelta(hours=hour, minutes=minute)
        amount = round(random.uniform(9.9, 999.9), 2)
        purchases.append({
            'user_id': user_id,
            'purchase_time': purchase_time,
            'amount': amount
        })
    
    df_purchases = pd.DataFrame(purchases)
    df_purchases = df_purchases.sort_values('purchase_time')
    df_purchases.to_csv(os.path.join(output_dir, 'purchases.csv'), index=False)
    print(f"Generated {len(df_purchases)} user purchase records")
    
    print("Test data generation completed successfully")
    print(f"Data files saved in: {output_dir}/")
    return True


if __name__ == '__main__':
    print("=" * 60)
    print("TEST DATA GENERATOR - NOT PART OF ANALYSIS PROGRAM")
    print("=" * 60)
    generate_test_data()
