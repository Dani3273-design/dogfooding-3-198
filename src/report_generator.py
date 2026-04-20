"""
Report generator module for user retention and conversion analysis.
Generates PDF reports with charts and statistics.
"""

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
from datetime import datetime
import os

# Set font for Chinese characters
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


class ReportGenerator:
    """Generate PDF reports with user retention and conversion analysis."""
    
    def __init__(self, output_path: str = "output/report.pdf"):
        """
        Initialize the report generator.
        
        Args:
            output_path: Path to save the PDF report
        """
        self.output_path = output_path
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
    
    def generate_report(self, data_processor) -> str:
        """
        Generate the complete PDF report.
        
        Args:
            data_processor: DataProcessor instance with loaded data
            
        Returns:
            Path to the generated PDF file
        """
        print("[INFO] Generating PDF report...")
        
        # Calculate all metrics
        daily_reg = data_processor.get_daily_registration()
        conversion_7d = data_processor.calculate_conversion_rate(7)
        conversion_15d = data_processor.calculate_conversion_rate(15)
        retention_7d = data_processor.calculate_retention_rate(7)
        summary = data_processor.get_summary_stats()
        
        # Create PDF
        with PdfPages(self.output_path) as pdf:
            # Page 1: Title and Summary
            self._create_title_page(pdf, summary)
            
            # Page 2: Daily Registration
            self._create_daily_registration_page(pdf, daily_reg, summary)
            
            # Page 3: 7-Day Conversion
            self._create_conversion_page(pdf, conversion_7d, 7)
            
            # Page 4: 15-Day Conversion
            self._create_conversion_page(pdf, conversion_15d, 15)
            
            # Page 5: 7-Day Retention
            self._create_retention_page(pdf, retention_7d)
        
        print(f"[INFO] PDF report saved to: {self.output_path}")
        return self.output_path
    
    def _create_title_page(self, pdf, summary: dict):
        """Create the title page with summary statistics."""
        fig, ax = plt.subplots(figsize=(8, 11))
        ax.axis('off')
        
        # Title
        title_text = '用户留存与转化分析报告'
        ax.text(0.5, 0.9, title_text, fontsize=24, ha='center', va='top', weight='bold')
        
        # Generation time
        gen_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ax.text(0.5, 0.85, f'生成时间: {gen_time}', fontsize=12, ha='center', va='top')
        
        # Summary section
        summary_y = 0.75
        ax.text(0.1, summary_y, '数据概览', fontsize=16, ha='left', va='top', weight='bold')
        
        summary_items = [
            f"数据时间范围: {summary['start_date']} 至 {summary['end_date']}",
            f"总注册用户数: {summary['total_users']}",
            f"总登录次数: {summary['total_logins']}",
            f"总消费次数: {summary['total_purchases']}",
            f"有消费的用户数: {summary['users_with_purchase']}",
            f"整体消费转化率: {summary['purchase_rate']:.2%}",
            f"有登录的用户数: {summary['users_with_login']}",
            f"整体登录率: {summary['login_rate']:.2%}"
        ]
        
        for i, item in enumerate(summary_items):
            ax.text(0.15, summary_y - 0.05 - (i * 0.04), item, fontsize=12, ha='left', va='top')
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _create_daily_registration_page(self, pdf, daily_reg: pd.DataFrame, summary: dict):
        """Create the daily registration chart page."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Convert dates to string for better display
        dates = [str(d) for d in daily_reg['register_date_only']]
        counts = daily_reg['count'].values
        
        # Create bar chart
        bars = ax.bar(dates, counts, color='steelblue', alpha=0.8)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=9)
        
        ax.set_xlabel('注册日期', fontsize=12)
        ax.set_ylabel('注册用户数', fontsize=12)
        ax.set_title('每日用户注册数统计', fontsize=16, weight='bold')
        
        # Rotate x-axis labels
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _create_conversion_page(self, pdf, conversion_df: pd.DataFrame, days: int):
        """Create the conversion rate chart page."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        days_list = conversion_df['day'].values
        rates = conversion_df['conversion_rate'].values
        
        # Create bar chart
        bars = ax.bar(days_list, rates * 100, color='coral', alpha=0.8)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom', fontsize=9)
        
        ax.set_xlabel('注册后天数', fontsize=12)
        ax.set_ylabel('转化率 (%)', fontsize=12)
        ax.set_title(f'{days}日内用户消费转化率', fontsize=16, weight='bold')
        ax.set_xticks(days_list)
        
        # Set y-axis limit
        ax.set_ylim(0, max(rates) * 100 * 1.2)
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _create_retention_page(self, pdf, retention_df: pd.DataFrame):
        """Create the retention rate chart page."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        days_list = retention_df['day'].values
        rates = retention_df['retention_rate'].values
        
        # Create bar chart
        bars = ax.bar(days_list, rates * 100, color='mediumseagreen', alpha=0.8)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom', fontsize=9)
        
        ax.set_xlabel('注册后天数', fontsize=12)
        ax.set_ylabel('留存率 (%)', fontsize=12)
        ax.set_title('7日内用户登录留存率', fontsize=16, weight='bold')
        ax.set_xticks(days_list)
        
        # Set y-axis limit
        ax.set_ylim(0, max(rates) * 100 * 1.2)
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
