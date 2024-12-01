# dashboard/utils/stock_report.py
import matplotlib
matplotlib.use('Agg')  # Must be before importing pyplot
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime, timedelta
from django.db.models import Sum, Count, F, Q  # Add Q to imports
from django.utils import timezone
import os
class StockReportPDF(FPDF):
    def __init__(self, stock_data, orientation='P', unit='mm', format='A4'):
        super().__init__(orientation, unit, format)
        self.stock_data = stock_data
        self.filename = None
    def create_charts(self):
        temp_dir = os.path.dirname(self.filename) or os.getcwd()
        # 1. Stock Level Distribution Pie Chart
        plt.figure(figsize=(8, 6))
        stock_levels = self.stock_data.values(
            'drug__class_therapeutique'
        ).annotate(
            total_stock=Sum('level')
        ).order_by('-total_stock')
        plt.pie(
            [x['total_stock'] for x in stock_levels],
            labels=[x['drug__class_therapeutique'] for x in stock_levels],
            autopct='%1.1f%%',
            colors=['#90EE90', '#2E8B57', '#3CB371', '#98FB98', '#00FF7F']
        )
        plt.title('Stock Distribution by Medicine Group')
        dist_path = os.path.join(temp_dir, 'stock_dist.png')
        plt.savefig(dist_path, bbox_inches='tight', dpi=300)
        plt.close()
        # 2. Low Stock Items Bar Chart
        plt.figure(figsize=(10, 6))
        low_stock = self.stock_data.filter(
            level__lte=F('reorderPoint')
        ).values(
            'drug__name'
        ).annotate(
            current_level=Sum('level')
        ).order_by('current_level')[:10]
        plt.bar(
            [x['drug__name'] for x in low_stock],
            [x['current_level'] for x in low_stock],
            color='#FF6B6B'
        )
        plt.title('Low Stock Items')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        low_stock_path = os.path.join(temp_dir, 'low_stock.png')
        plt.savefig(low_stock_path, bbox_inches='tight', dpi=300)
        plt.close()
        # 3. Stock Health Overview
        plt.figure(figsize=(8, 6))
        stock_health = {
            'Healthy': self.stock_data.filter(level__gt=F('reorderPoint')).count(),
            'Low': self.stock_data.filter(level__lte=F('reorderPoint')).count(),
            'Out': self.stock_data.filter(level=0).count()
        }
        
        colors = ['#90EE90', '#FFD700', '#FF6B6B']
        plt.pie(
            stock_health.values(),
            labels=stock_health.keys(),
            autopct='%1.1f%%',
            colors=colors
        )
        plt.title('Stock Health Overview')
        health_path = os.path.join(temp_dir, 'stock_health.png')
        plt.savefig(health_path, bbox_inches='tight', dpi=300)
        plt.close()
        return dist_path, low_stock_path, health_path
    def generate(self, filename="stock_report.pdf"):
        self.filename = filename
        dist_path, low_stock_path, health_path = self.create_charts()
        self.add_page()
        
        # Title
        self.set_font('Arial', 'B', 24)
        self.set_text_color(0, 100, 0)
        self.cell(0, 15, 'Pharmacy Stock Report', ln=True, align='C')
        self.set_font('Arial', '', 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}', ln=True, align='C')
        
        # Overall Statistics
        self.ln(10)
        self.set_font('Arial', 'B', 16)
        self.set_fill_color(144, 238, 144)
        self.set_text_color(0, 100, 0)
        self.cell(0, 10, 'Stock Overview', ln=True, fill=True)
        
        total_stats = self.stock_data.aggregate(
            total_items=Count('id'),
            total_units=Sum('level'),
            low_stock=Count('id', filter=Q(level__lte=F('reorderPoint'))),  # Fix: Use Q directly
            out_of_stock=Count('id', filter=Q(level=0))  # Fix: Use Q directly
        )
        
        self.set_font('Arial', '', 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, f"Total Items: {total_stats['total_items']}", ln=True)
        self.cell(0, 10, f"Total Units: {total_stats['total_units']}", ln=True)
        self.cell(0, 10, f"Low Stock Items: {total_stats['low_stock']}", ln=True)
        self.cell(0, 10, f"Out of Stock: {total_stats['out_of_stock']}", ln=True)
        # Charts
        self.image(health_path, x=10, w=90)
        self.image(dist_path, x=110, w=90)
        
        # Low Stock Items Table
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 100, 0)
        self.cell(0, 10, 'Low Stock Items', ln=True, fill=True)
        
        # Table headers
        col_width = self.get_string_width('Medicine Name  ') + 20
        headers = ['Medicine', 'Current Stock', 'Reorder Point']
        
        self.set_font('Arial', 'B', 12)
        for header in headers:
            self.cell(col_width, 10, header, border=1)
        self.ln()
        
        # Table data
        self.set_font('Arial', '', 10)
        low_stock_items = self.stock_data.filter(
            level__lte=F('reorderPoint')
        ).select_related('drug')[:15]
        
        for item in low_stock_items:
            self.cell(col_width, 10, item.drug.name, border=1)
            self.cell(col_width, 10, str(item.level), border=1)
            self.cell(col_width, 10, str(item.reorderPoint), border=1)
            self.ln()
        self.output(filename)
        
        # Cleanup
        for path in [dist_path, low_stock_path, health_path]:
            try:
                os.remove(path)
            except OSError:
                pass