from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from django.db.models import Sum, Count
from django.utils import timezone
import os

class SalesReportPDF:
    def __init__(self, sales_data):
        self.sales_data = sales_data
        self.pdf = FPDF()

    def create_charts(self):
        # Get temp directory path
        temp_dir = os.path.dirname(self.filename)
        if not temp_dir:
            temp_dir = os.getcwd()

        # Sales distribution chart
        plt.figure(figsize=(20, 10))
        group_sales = (
            self.sales_data
            .values('drug__class_therapeutique')
            .annotate(total=Sum('quantity'))
            .order_by('-total')
        )
        
        groups = [item['drug__class_therapeutique'] for item in group_sales]
        totals = [item['total'] for item in group_sales]
        
        plt.pie(
            totals,
            labels=groups,
            autopct='%1.1f%%',
            colors=['lightgreen', 'darkgreen', 'seagreen', 'mediumseagreen'],
            textprops={'fontsize': 24}  # Increase pie chart font size
        )
        plt.title('Sales by Medicine Group', fontsize=40)  # Increase title font size
        dist_path = os.path.join(temp_dir, 'sales_dist.png')
        plt.savefig(dist_path)
        plt.close()

        # Daily sales trend
        plt.figure(figsize=(10, 5))
        daily_sales = (
            self.sales_data
            .values('date')
            .annotate(total=Sum('quantity'))
            .order_by('date')
        )
        
        dates = [item['date'] for item in daily_sales]
        totals = [item['total'] for item in daily_sales]
        
        plt.plot(dates, totals, color='seagreen', marker='o')
        plt.title('Daily Sales Trend', fontsize=28)  # Increase title font size
        plt.xlabel('Date', fontsize=14)  # Increase x-axis label font size
        plt.ylabel('Sales Quantity', fontsize=14)  # Increase y-axis label font size
        plt.xticks(fontsize=12, rotation=45)  # Increase x-tick font size
        plt.yticks(fontsize=12)  # Increase y-tick font size
        plt.tight_layout()
        trend_path = os.path.join(temp_dir, 'daily_sales.png')
        plt.savefig(trend_path)
        plt.close()
        
        return dist_path, trend_path


    def generate(self, filename="sales_report.pdf"):
        self.filename = filename
        dist_path, trend_path = self.create_charts()

        self.pdf.add_page()
        
        # Title
        self.pdf.set_font('Arial', 'B', 24)
        self.pdf.set_text_color(0, 100, 0)  # Green
        self.pdf.cell(0, 15, 'Pharmacy Sales Report', ln=True, align='C')
        self.pdf.set_font('Arial', '', 12)
        self.pdf.set_text_color(64, 64, 64)  # Dark gray
        self.pdf.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}', ln=True, align='C')
        
        # Section 1: This Week's Sales
        self.pdf.ln(10)
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.set_text_color(0, 100, 0)  # Light green
        self.pdf.set_fill_color(200, 255, 200)
        self.pdf.cell(0, 10, 'This Week\'s Sales Statistics', ln=True, fill=True)
        
        # Sales statistics text
        self.pdf.set_font('Arial', '', 12)
        self.pdf.set_text_color(64, 64, 64)  # Dark gray
        week_start = timezone.now().date() - timedelta(days=timezone.now().weekday())
        week_sales = self.sales_data.filter(date__gte=week_start)
        weekly_stats = week_sales.aggregate(
            total_quantity=Sum('quantity'),
            unique_medicines=Count('drug', distinct=True),
            total_revenue=Sum('drug__PPV')
        )
        
        self.pdf.cell(0, 10, f"Total Sales: {weekly_stats['total_quantity'] or 0}", ln=True)
        self.pdf.cell(0, 10, f"Unique Medicines: {weekly_stats['unique_medicines'] or 0}", ln=True)
        self.pdf.cell(0, 10, f"Total Revenue: {weekly_stats['total_revenue'] or 0:.2f} DH", ln=True)
        
        # Section 2: Most In-Demand Drugs
        self.pdf.ln(10)
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.set_text_color(0, 100, 0)  # Light green
        self.pdf.set_fill_color(200, 255, 200)
        self.pdf.cell(0, 10, 'Most In-Demand Drugs', ln=True, fill=True)
        
        top_drugs = self.sales_data.values(
            'drug__name', 'drug__class_therapeutique'
        ).annotate(
            total_sold=Sum('quantity')
        ).order_by('-total_sold')[:5]
        
        page_width = self.pdf.w - 20
        col_widths = [page_width * 0.4, page_width * 0.3, page_width * 0.3]

        # Render table headers
        self.pdf.set_font('Arial', 'B', 10)
        self.pdf.set_text_color(144, 238, 144)  # Light green
        headers = ['Medicine', 'Category', 'Units Sold']
        for i, header in enumerate(headers):
            self.pdf.cell(col_widths[i], 10, header, border=1, fill=True)
        self.pdf.ln()
        
        # Render table rows
        self.pdf.set_font('Arial', '', 10)
        self.pdf.set_text_color(64, 64, 64)  # Dark gray
        for drug in top_drugs:
            self.pdf.cell(col_widths[0], 10, str(drug['drug__name']), border=1)
            self.pdf.cell(col_widths[1], 10, str(drug['drug__class_therapeutique']), border=1)
            self.pdf.cell(col_widths[2], 10, str(drug['total_sold']), border=1)
            self.pdf.ln()
        
        # Section 3: Next Week Forecast
        self.pdf.ln(10)
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.set_text_color(0, 100, 0)  # Light green
        self.pdf.set_fill_color(200, 255, 200)
        self.pdf.cell(0, 10, 'Next Week Demand Forecast', ln=True, fill=True)
        
        # Forecast data
        self.pdf.set_font('Arial', '', 10)
        self.pdf.set_text_color(64, 64, 64)  # Dark gray
        four_weeks_ago = timezone.now().date() - timedelta(weeks=4)
        monthly_avg = self.sales_data.filter(
            date__gte=four_weeks_ago
        ).values(
            'drug__name', 'drug__class_therapeutique'
        ).annotate(
            avg_weekly=Sum('quantity') / 4
        ).order_by('-avg_weekly')[:5]
        
        for drug in monthly_avg:
            self.pdf.cell(col_widths[0], 10, str(drug['drug__name']), border=1)
            self.pdf.cell(col_widths[1], 10, str(drug['drug__class_therapeutique']), border=1)
            self.pdf.cell(col_widths[2], 10, f"{drug['avg_weekly']:.0f} units", border=1)
            self.pdf.ln()
        
        # Add charts
        self.pdf.add_page()
        self.pdf.image(dist_path, x=10, y=None, w=self.pdf.w - 20)
        self.pdf.image(trend_path, x=10, y=None, w=self.pdf.w - 20)
        
        self.pdf.output(filename)
        
        # Cleanup
        try:
            os.remove(dist_path)
            os.remove(trend_path)
        except OSError:
            pass 