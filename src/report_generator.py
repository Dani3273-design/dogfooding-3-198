import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
from datetime import datetime

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class ReportGenerator:
    """
    Report generator class for creating PDF analysis reports.
    Handles visualization and PDF generation.
    """
    
    def __init__(self, output_dir='output'):
        """
        Initialize ReportGenerator with output directory.
        
        Args:
            output_dir: Directory to save the PDF report
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def plot_daily_registrations(self, daily_counts, ax):
        """
        Plot daily registration bar chart.
        
        Args:
            daily_counts: DataFrame with date and count columns
            ax: Matplotlib axes object
        """
        dates = [str(d) for d in daily_counts['date']]
        counts = daily_counts['count'].values
        
        bars = ax.bar(dates, counts, color='#4CAF50', alpha=0.7)
        ax.set_title('每日用户注册数', fontsize=14, pad=20)
        ax.set_xlabel('日期', fontsize=12)
        ax.set_ylabel('注册用户数', fontsize=12)
        ax.tick_params(axis='x', rotation=45, labelsize=8)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=8
            )
        
    def plot_7day_conversion(self, conversion_rates, ax):
        """
        Plot 7-day conversion rate bar chart.
        
        Args:
            conversion_rates: Dict with day as key and rate as value
            ax: Matplotlib axes object
        """
        days = list(conversion_rates.keys())
        rates = [v * 100 for v in conversion_rates.values()]
        
        bars = ax.bar([f'第{d}天' for d in days], rates, color='#2196F3', alpha=0.7)
        ax.set_title('7日用户转换率（注册后N日内首次消费）', fontsize=14, pad=20)
        ax.set_xlabel('注册后天数', fontsize=12)
        ax.set_ylabel('转换率 (%)', fontsize=12)
        ax.set_ylim(0, max(rates) * 1.2 if max(rates) > 0 else 1)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=9
            )
        
    def plot_15day_conversion(self, conversion_rates, ax):
        """
        Plot 15-day conversion rate bar chart.
        
        Args:
            conversion_rates: Dict with day as key and rate as value
            ax: Matplotlib axes object
        """
        days = list(conversion_rates.keys())
        rates = [v * 100 for v in conversion_rates.values()]
        
        bars = ax.bar([f'第{d}天' for d in days], rates, color='#9C27B0', alpha=0.7)
        ax.set_title('15日用户累积转换率', fontsize=14, pad=20)
        ax.set_xlabel('注册后天数', fontsize=12)
        ax.set_ylabel('累积转换率 (%)', fontsize=12)
        ax.set_ylim(0, max(rates) * 1.2 if max(rates) > 0 else 1)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=9
            )
        
    def plot_7day_retention(self, retention_rates, ax):
        """
        Plot 7-day retention rate bar chart.
        
        Args:
            retention_rates: Dict with day as key and rate as value
            ax: Matplotlib axes object
        """
        days = list(retention_rates.keys())
        rates = [v * 100 for v in retention_rates.values()]
        
        bars = ax.bar([f'第{d}天' for d in days], rates, color='#FF9800', alpha=0.7)
        ax.set_title('7日用户留存率（注册后N日内首次登陆）', fontsize=14, pad=20)
        ax.set_xlabel('注册后天数', fontsize=12)
        ax.set_ylabel('留存率 (%)', fontsize=12)
        ax.set_ylim(0, max(rates) * 1.2 if max(rates) > 0 else 1)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=9
            )
        
    def add_summary_table(self, summary_stats, ax):
        """
        Add summary statistics table to the report.
        
        Args:
            summary_stats: Dictionary containing summary statistics
            ax: Matplotlib axes object
        """
        ax.axis('tight')
        ax.axis('off')
        
        table_data = [
            ['总用户数', f"{summary_stats['total_users']}"],
            ['有登陆记录用户数', f"{summary_stats['users_with_login']}"],
            ['有消费记录用户数', f"{summary_stats['users_with_purchase']}"],
            ['总体留存率', f"{summary_stats['overall_retention_rate']*100:.1f}%"],
            ['总体转换率', f"{summary_stats['overall_conversion_rate']*100:.1f}%"],
            ['平均首次登陆天数', f"{summary_stats['avg_days_to_login']:.1f} 天"],
            ['平均首次消费天数', f"{summary_stats['avg_days_to_purchase']:.1f} 天"]
        ]
        
        table = ax.table(
            cellText=table_data,
            colLabels=['指标', '数值'],
            loc='center',
            cellLoc='center',
            colWidths=[0.5, 0.5]
        )
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 2)
        ax.set_title('用户留存转换分析概览', fontsize=16, pad=30)
        
    def generate_report(self, data_processor, filename='user_retention_conversion_analysis.pdf'):
        """
        Generate complete PDF analysis report.
        
        Args:
            data_processor: DataProcessor instance with processed data
            filename: Output PDF filename
        """
        print("Generating PDF report...")
        
        filepath = os.path.join(self.output_dir, filename)
        
        with PdfPages(filepath) as pdf:
            fig = plt.figure(figsize=(12, 16))
            
            ax1 = plt.subplot(5, 1, 1)
            self.add_summary_table(data_processor.get_summary_statistics(), ax1)
            
            ax2 = plt.subplot(5, 1, 2)
            self.plot_daily_registrations(data_processor.get_daily_registrations(), ax2)
            
            ax3 = plt.subplot(5, 1, 3)
            self.plot_7day_conversion(data_processor.get_7day_conversion_rates(), ax3)
            
            ax4 = plt.subplot(5, 1, 4)
            self.plot_15day_conversion(data_processor.get_15day_conversion_rates(), ax4)
            
            ax5 = plt.subplot(5, 1, 5)
            self.plot_7day_retention(data_processor.get_7day_retention_rates(), ax5)
            
            plt.figtext(
                0.5, 0.01,
                f'报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                ha='center', fontsize=10, color='gray'
            )
            
            plt.tight_layout(rect=[0, 0.03, 1, 0.97])
            pdf.savefig(fig)
            plt.close()
            
            d = pdf.infodict()
            d['Title'] = '用户留存转换分析报告'
            d['Author'] = 'Analysis System'
            d['Subject'] = 'User Retention and Conversion Analysis'
            d['CreationDate'] = datetime.now()
            
        print(f"Report generated successfully: {filepath}")
        return filepath
