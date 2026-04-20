"""
Main program for user retention and conversion analysis.
"""
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_processor import DataProcessor
from src.report_generator import ReportGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main function to run the user retention analysis."""
    logger.info("=" * 60)
    logger.info("Starting User Retention Analysis")
    logger.info("=" * 60)
    
    data_dir = "data"
    output_dir = "output"
    
    processor = DataProcessor(data_dir)
    processor.load_data()
    
    logger.info("Calculating daily registration count...")
    daily_registration = processor.get_daily_registration_count()
    
    logger.info("Calculating 7-day conversion rate...")
    conversion_7day = processor.calculate_conversion_rate(7)
    
    logger.info("Calculating 15-day conversion rate...")
    conversion_15day = processor.calculate_conversion_rate(15)
    
    logger.info("Calculating 7-day retention rate...")
    retention_7day = processor.calculate_retention_rate(7)
    
    logger.info("Generating analysis summary...")
    summary = processor.get_analysis_summary()
    
    logger.info("Generating PDF report...")
    generator = ReportGenerator(output_dir)
    report_path = generator.generate_report(
        daily_registration=daily_registration,
        conversion_7day=conversion_7day,
        conversion_15day=conversion_15day,
        retention_7day=retention_7day,
        summary=summary
    )
    
    logger.info("=" * 60)
    logger.info("Analysis completed successfully!")
    logger.info(f"Report saved to: {report_path}")
    logger.info("=" * 60)
    
    print("\n" + "=" * 60)
    print("Analysis Summary")
    print("=" * 60)
    print(f"Total Users: {summary['total_users']}")
    print(f"Total Logins: {summary['total_logins']}")
    print(f"Total Consumptions: {summary['total_consumptions']}")
    print(f"Total Revenue: ¥{summary['total_revenue']}")
    print(f"Date Range: {summary['date_range_start']} to {summary['date_range_end']}")
    print(f"\nReport saved to: {report_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
