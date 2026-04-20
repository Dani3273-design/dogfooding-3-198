"""
Data processor module for user retention analysis.
Handles data loading, cleaning, and analysis calculations.
"""
import pandas as pd
from datetime import timedelta
import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)


class DataProcessor:
    """Process user data for retention and conversion analysis."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize data processor.
        
        Args:
            data_dir: Directory containing the data files
        """
        self.data_dir = data_dir
        self.df_registration = None
        self.df_login = None
        self.df_consumption = None
        
    def load_data(self) -> None:
        """Load all data files from the data directory."""
        logger.info("Loading data files...")
        
        self.df_registration = pd.read_csv(
            f"{self.data_dir}/user_registration.csv",
            parse_dates=["registration_date"]
        )
        self.df_login = pd.read_csv(
            f"{self.data_dir}/user_login.csv",
            parse_dates=["login_time"]
        )
        self.df_consumption = pd.read_csv(
            f"{self.data_dir}/user_consumption.csv",
            parse_dates=["consumption_time"]
        )
        
        logger.info(f"Loaded {len(self.df_registration)} registrations")
        logger.info(f"Loaded {len(self.df_login)} login records")
        logger.info(f"Loaded {len(self.df_consumption)} consumption records")
        
    def get_daily_registration_count(self) -> pd.DataFrame:
        """
        Calculate daily registration count.
        
        Returns:
            DataFrame with date and registration count
        """
        df = self.df_registration.copy()
        df["date"] = df["registration_date"].dt.date
        daily_count = df.groupby("date").size().reset_index(name="count")
        daily_count["date"] = pd.to_datetime(daily_count["date"])
        daily_count = daily_count.sort_values("date").reset_index(drop=True)
        logger.info("Calculated daily registration count")
        return daily_count
    
    def calculate_conversion_rate(self, days: int) -> pd.DataFrame:
        """
        Calculate conversion rate within specified days after registration.
        
        Args:
            days: Number of days to analyze (e.g., 7 or 15)
            
        Returns:
            DataFrame with day number and conversion rate
        """
        df_reg = self.df_registration.copy()
        df_cons = self.df_consumption.copy()
        
        first_consumption = df_cons.groupby("user_id")["consumption_time"].min().reset_index()
        first_consumption.columns = ["user_id", "first_consumption"]
        
        merged = pd.merge(df_reg, first_consumption, on="user_id", how="left")
        
        merged["days_to_consume"] = (
            merged["first_consumption"] - merged["registration_date"]
        ).dt.days
        
        results = []
        for day in range(1, days + 1):
            users_registered = len(merged)
            users_converted_in_day = len(
                merged[merged["days_to_consume"].notna() & (merged["days_to_consume"] <= day - 1)]
            )
            rate = users_converted_in_day / users_registered * 100 if users_registered > 0 else 0
            results.append({
                "day": day,
                "conversion_rate": rate,
                "users_converted": users_converted_in_day,
                "total_users": users_registered
            })
        
        logger.info(f"Calculated {days}-day conversion rate")
        return pd.DataFrame(results)
    
    def calculate_retention_rate(self, days: int) -> pd.DataFrame:
        """
        Calculate retention rate (login within specified days after registration).
        
        Args:
            days: Number of days to analyze (e.g., 7 or 15)
            
        Returns:
            DataFrame with day number and retention rate
        """
        df_reg = self.df_registration.copy()
        df_login = self.df_login.copy()
        
        results = []
        for day in range(1, days + 1):
            retained_users = set()
            
            for _, row in df_reg.iterrows():
                user_id = row["user_id"]
                reg_date = row["registration_date"]
                target_date = reg_date + timedelta(days=day - 1)
                
                user_logins = df_login[df_login["user_id"] == user_id]
                logins_on_day = user_logins[
                    user_logins["login_time"].dt.date == target_date.date()
                ]
                
                if len(logins_on_day) > 0:
                    retained_users.add(user_id)
            
            total_users = len(df_reg)
            rate = len(retained_users) / total_users * 100 if total_users > 0 else 0
            results.append({
                "day": day,
                "retention_rate": rate,
                "users_retained": len(retained_users),
                "total_users": total_users
            })
        
        logger.info(f"Calculated {days}-day retention rate")
        return pd.DataFrame(results)
    
    def get_analysis_summary(self) -> Dict:
        """
        Get summary statistics for the analysis.
        
        Returns:
            Dictionary containing summary statistics
        """
        total_users = len(self.df_registration)
        total_logins = len(self.df_login)
        total_consumptions = len(self.df_consumption)
        
        unique_login_users = self.df_login["user_id"].nunique()
        unique_consume_users = self.df_consumption["user_id"].nunique()
        
        avg_logins_per_user = total_logins / unique_login_users if unique_login_users > 0 else 0
        avg_consumptions_per_user = total_consumptions / unique_consume_users if unique_consume_users > 0 else 0
        
        total_revenue = self.df_consumption["amount"].sum()
        avg_consumption_amount = self.df_consumption["amount"].mean()
        
        date_range_start = self.df_registration["registration_date"].min()
        date_range_end = self.df_registration["registration_date"].max()
        
        summary = {
            "total_users": total_users,
            "total_logins": total_logins,
            "total_consumptions": total_consumptions,
            "unique_login_users": unique_login_users,
            "unique_consume_users": unique_consume_users,
            "avg_logins_per_user": round(avg_logins_per_user, 2),
            "avg_consumptions_per_user": round(avg_consumptions_per_user, 2),
            "total_revenue": round(total_revenue, 2),
            "avg_consumption_amount": round(avg_consumption_amount, 2),
            "date_range_start": date_range_start.strftime("%Y-%m-%d"),
            "date_range_end": date_range_end.strftime("%Y-%m-%d")
        }
        
        logger.info("Generated analysis summary")
        return summary
