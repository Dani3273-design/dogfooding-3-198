"""
Report generator module for user retention analysis.
Generates PDF reports with charts and analysis results.
"""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import os
import logging
from typing import Dict

logger = logging.getLogger(__name__)

import matplotlib.font_manager as fm

def get_chinese_font():
    """Get available Chinese font."""
    chinese_fonts = ['Arial Unicode MS', 'PingFang SC', 'Heiti TC', 'STHeiti', 'SimHei', 'Microsoft YaHei']
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    for font in chinese_fonts:
        if font in available_fonts:
            return font
    return 'DejaVu Sans'

plt.rcParams['font.sans-serif'] = [get_chinese_font(), 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class ReportGenerator:
    """Generate PDF reports for user retention analysis."""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize report generator.
        
        Args:
            output_dir: Directory to save the generated reports
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def _create_bar_chart(
        self, 
        ax, 
        data: pd.DataFrame, 
        x_col: str, 
        y_col: str, 
        title: str, 
        xlabel: str, 
        ylabel: str,
        color: str = "steelblue"
    ) -> None:
        """
        Create a bar chart on the given axis.
        
        Args:
            ax: Matplotlib axis
            data: DataFrame containing the data
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            color: Bar color
        """
        bars = ax.bar(data[x_col], data[y_col], color=color, edgecolor='black', linewidth=0.5)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_xlabel(xlabel, fontsize=10)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f'{height:.1f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom',
                fontsize=8
            )
    
    def _create_daily_registration_chart(self, ax, data: pd.DataFrame) -> None:
        """Create daily registration count bar chart."""
        data = data.copy()
        data["date_str"] = data["date"].dt.strftime("%m-%d")
        self._create_bar_chart(
            ax, data, "date_str", "count",
            "每日用户注册数", "日期", "注册人数", "steelblue"
        )
        ax.tick_params(axis='x', rotation=45)
        
    def _create_conversion_chart(self, ax, data: pd.DataFrame, days: int) -> None:
        """Create conversion rate bar chart."""
        self._create_bar_chart(
            ax, data, "day", "conversion_rate",
            f"{days}日内消费转换率", "注册后第N天", "转换率 (%)", "forestgreen"
        )
        
    def _create_retention_chart(self, ax, data: pd.DataFrame, days: int) -> None:
        """Create retention rate bar chart."""
        self._create_bar_chart(
            ax, data, "day", "retention_rate",
            f"{days}日内登录留存率", "注册后第N天", "留存率 (%)", "coral"
        )
        
    def generate_report(
        self,
        daily_registration: pd.DataFrame,
        conversion_7day: pd.DataFrame,
        conversion_15day: pd.DataFrame,
        retention_7day: pd.DataFrame,
        summary: Dict,
        filename: str = "user_retention_report.pdf"
    ) -> str:
        """
        Generate a comprehensive PDF report.
        
        Args:
            daily_registration: Daily registration count data
            conversion_7day: 7-day conversion rate data
            conversion_15day: 15-day conversion rate data
            retention_7day: 7-day retention rate data
            summary: Summary statistics dictionary
            filename: Output filename
            
        Returns:
            Path to the generated PDF file
        """
        output_path = os.path.join(self.output_dir, filename)
        
        logger.info(f"Generating PDF report: {output_path}")
        
        with PdfPages(output_path) as pdf:
            fig = plt.figure(figsize=(12, 16))
            fig.suptitle("用户留存转换分析报告", fontsize=16, fontweight='bold', y=0.98)
            
            ax1 = fig.add_axes([0.1, 0.78, 0.8, 0.16])
            self._create_daily_registration_chart(ax1, daily_registration)
            
            ax2 = fig.add_axes([0.1, 0.52, 0.8, 0.16])
            self._create_conversion_chart(ax2, conversion_7day, 7)
            
            ax3 = fig.add_axes([0.1, 0.30, 0.8, 0.16])
            self._create_conversion_chart(ax3, conversion_15day, 15)
            
            ax4 = fig.add_axes([0.1, 0.08, 0.8, 0.16])
            self._create_retention_chart(ax4, retention_7day, 7)
            
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)
            
            fig2 = plt.figure(figsize=(12, 10))
            fig2.suptitle("数据统计摘要", fontsize=16, fontweight='bold', y=0.95)
            
            summary_text = f"""
数据概览
═══════════════════════════════════════════════════════════════

基础数据统计
───────────────────────────────────────────────────────────────
• 总注册用户数: {summary['total_users']} 人
• 总登录记录数: {summary['total_logins']} 次
• 总消费记录数: {summary['total_consumptions']} 次
• 有登录行为的用户数: {summary['unique_login_users']} 人
• 有消费行为的用户数: {summary['unique_consume_users']} 人

用户行为统计
───────────────────────────────────────────────────────────────
• 人均登录次数: {summary['avg_logins_per_user']} 次
• 人均消费次数: {summary['avg_consumptions_per_user']} 次
• 平均消费金额: ¥{summary['avg_consumption_amount']}
• 总消费金额: ¥{summary['total_revenue']}

数据时间范围
───────────────────────────────────────────────────────────────
• 开始日期: {summary['date_range_start']}
• 结束日期: {summary['date_range_end']}

7日转换率统计
───────────────────────────────────────────────────────────────
"""
            for _, row in conversion_7day.iterrows():
                summary_text += f"• 第{int(row['day'])}日累计转换率: {row['conversion_rate']:.2f}%\n"
            
            summary_text += "\n15日转换率统计\n───────────────────────────────────────────────────────────────\n"
            for _, row in conversion_15day.iterrows():
                summary_text += f"• 第{int(row['day'])}日累计转换率: {row['conversion_rate']:.2f}%\n"
            
            summary_text += "\n7日留存率统计\n───────────────────────────────────────────────────────────────\n"
            for _, row in retention_7day.iterrows():
                summary_text += f"• 第{int(row['day'])}日留存率: {row['retention_rate']:.2f}%\n"
            
            ax = fig2.add_axes([0.05, 0.05, 0.9, 0.85])
            ax.axis('off')
            ax.text(0.05, 0.95, summary_text, transform=ax.transAxes, 
                   fontsize=11, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            pdf.savefig(fig2, bbox_inches='tight')
            plt.close(fig2)
        
        logger.info(f"PDF report generated successfully: {output_path}")
        return output_path
