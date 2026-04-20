"""
Test data generator for user retention analysis.
This script generates mock user registration, login, and consumption data.
"""
import random
import pandas as pd
from datetime import datetime, timedelta
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_activity_weight(hour: int, is_weekend: bool) -> float:
    """
    Calculate activity weight based on hour and day type.
    Higher activity during non-working hours and weekends.
    """
    if is_weekend:
        if 10 <= hour <= 22:
            return 2.0
        elif 8 <= hour <= 23:
            return 1.5
        else:
            return 0.5
    else:
        if 12 <= hour <= 14:
            return 1.8
        elif 18 <= hour <= 23:
            return 2.0
        elif 7 <= hour <= 9:
            return 1.2
        else:
            return 0.3


def generate_random_datetime(start_date: datetime, end_date: datetime) -> datetime:
    """
    Generate a random datetime with weighted probability based on activity patterns.
    """
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_date = start_date + timedelta(days=random_days)
    
    is_weekend = random_date.weekday() >= 5
    
    hour_weights = [get_activity_weight(h, is_weekend) for h in range(24)]
    total_weight = sum(hour_weights)
    hour_weights = [w / total_weight for w in hour_weights]
    
    hour = random.choices(range(24), weights=hour_weights)[0]
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    
    return random_date.replace(hour=hour, minute=minute, second=second)


def generate_test_data(
    num_users: int = 200,
    num_logins: int = 500,
    num_consumptions: int = 400,
    output_dir: str = "data"
) -> None:
    """
    Generate test data for user retention analysis.
    
    Args:
        num_users: Number of users to generate
        num_logins: Number of login records to generate
        num_consumptions: Number of consumption records to generate
        output_dir: Directory to save the generated data
    """
    os.makedirs(output_dir, exist_ok=True)
    
    year = 2024
    month = random.randint(1, 12)
    start_date = datetime(year, month, 1)
    
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(seconds=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)
    
    logger.info(f"Generating data for {year}-{month:02d}")
    
    user_ids = [f"U{str(i).zfill(6)}" for i in range(1, num_users + 1)]
    
    registration_data = []
    for user_id in user_ids:
        reg_date = generate_random_datetime(start_date, end_date)
        registration_data.append({
            "user_id": user_id,
            "registration_date": reg_date
        })
    
    df_registration = pd.DataFrame(registration_data)
    df_registration = df_registration.sort_values("registration_date").reset_index(drop=True)
    logger.info(f"Generated {len(df_registration)} user registrations")
    
    login_data = []
    for _ in range(num_logins):
        user_id = random.choice(user_ids)
        login_time = generate_random_datetime(start_date, end_date)
        login_data.append({
            "user_id": user_id,
            "login_time": login_time
        })
    
    df_login = pd.DataFrame(login_data)
    df_login = df_login.sort_values("login_time").reset_index(drop=True)
    logger.info(f"Generated {len(df_login)} login records")
    
    consumption_data = []
    for _ in range(num_consumptions):
        user_id = random.choice(user_ids)
        consumption_time = generate_random_datetime(start_date, end_date)
        amount = round(random.uniform(10, 500), 2)
        consumption_data.append({
            "user_id": user_id,
            "consumption_time": consumption_time,
            "amount": amount
        })
    
    df_consumption = pd.DataFrame(consumption_data)
    df_consumption = df_consumption.sort_values("consumption_time").reset_index(drop=True)
    logger.info(f"Generated {len(df_consumption)} consumption records")
    
    df_registration.to_csv(os.path.join(output_dir, "user_registration.csv"), index=False, encoding="utf-8")
    df_login.to_csv(os.path.join(output_dir, "user_login.csv"), index=False, encoding="utf-8")
    df_consumption.to_csv(os.path.join(output_dir, "user_consumption.csv"), index=False, encoding="utf-8")
    
    logger.info(f"Data saved to {output_dir}/")
    logger.info("Test data generation completed!")


if __name__ == "__main__":
    generate_test_data()
