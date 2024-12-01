import csv
from django.core.management.base import BaseCommand
from django.utils import timezone
from dashboard.models import Drug, Stock, Archive
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Load stock data from CSV file and save into Stock model'

    
    def calculate_week_dates(self, start_date):
        weeks = []
        for i in range(4):
            week_start = start_date + timedelta(weeks=i)
            week_end = week_start + timedelta(days=6)
            weeks.append((week_start, week_end))
        return weeks

    def handle(self, *args, **kwargs):
        file_path = './assets/data/data.csv'  # Path to your CSV file
        
        start_date = date(2024, 9, 1)
        weeks = self.calculate_week_dates(start_date)
    
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                code = row['CODE']  # This corresponds to the Drug model's ID
                drug = Drug.objects.filter(id=code).first()  # Get the Drug instance

                if not drug:
                    self.stdout.write(self.style.WARNING(f'Drug with ID {code} not found.'))
                    continue

                # Get the Stock instance for this drug
                stock = Stock.objects.filter(drug=drug).first()
                if not stock:
                    self.stdout.write(self.style.WARNING(f'Stock for Drug with ID {code} not found.'))
                    continue

                # Extract stock data for each week
                start_week_1 = int(row['Start of Week 1 Stock']) if row['Start of Week 1 Stock'] else 0
                week_1_sales = int(row['Week 1 Sales']) if row['Week 1 Sales'] else 0
                end_week_1 = int(row['End of Week 1 Stock']) if row['End of Week 1 Stock'] else 0

                start_week_2 = int(row['Start of Week 2 Stock']) if row['Start of Week 2 Stock'] else 0
                week_2_sales = int(row['Week 2 Sales']) if row['Week 2 Sales'] else 0
                end_week_2 = int(row['End of Week 2 Stock']) if row['End of Week 2 Stock'] else 0

                start_week_3 = int(row['Start of Week 3 Stock']) if row['Start of Week 3 Stock'] else 0
                week_3_sales = int(row['Week 3 Sales']) if row['Week 3 Sales'] else 0
                end_week_3 = int(row['End of Week 3 Stock']) if row['End of Week 3 Stock'] else 0

                start_week_4 = int(row['Start of Week 4 Stock']) if row['Start of Week 4 Stock'] else 0
                week_4_sales = int(row['Week 4 Sales']) if row['Week 4 Sales'] else 0
                end_week_4 = int(row['End of Week 4 Stock']) if row['End of Week 4 Stock'] else 0

                # Calculate selling speed and reorder point from CSV
                reorder_point = int(row['Reorder Point']) if row['Reorder Point'] else 10  # Default if not specified

                # Create or update the archive instances for the stock
                archive1 = Archive(
                    stock=stock,
                    sows=start_week_1,
                    eows=end_week_1,
                    sales=week_1_sales,
                    sowd=weeks[0][0],
                    eowd=weeks[0][1],
                    shortage=end_week_1 <= reorder_point
                )
                archive1.save()
                
                archive2 = Archive(
                    stock=stock,
                    sows=start_week_2,
                    eows=end_week_2,
                    sales=week_2_sales,
                    sowd=weeks[1][0],
                    eowd=weeks[1][1],
                    shortage=end_week_2 <= reorder_point
                )
                archive2.save()
                
                archive3 = Archive(
                    stock=stock,
                    sows=start_week_3,
                    eows=end_week_3,
                    sales=week_3_sales,
                    sowd=weeks[2][0],
                    eowd=weeks[2][1],
                    shortage=end_week_3 <= reorder_point
                )
                archive3.save()
                
                archive4 = Archive(
                    stock=stock,
                    sows=start_week_4,
                    eows=end_week_4,
                    sales=week_4_sales,
                    sowd=weeks[3][0],
                    eowd=weeks[3][1],
                    shortage=end_week_4 <= reorder_point
                )
                archive4.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded archive data'))
