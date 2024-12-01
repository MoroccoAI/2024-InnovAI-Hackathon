import csv
from django.core.management.base import BaseCommand
from django.utils import timezone
from dashboard.models import Drug, Stock
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Load stock data from CSV file and save into Stock model'

    def handle_selling_speed(self , selling_speed):
        if(selling_speed=='Very Fast'):
            return 'VF'
        elif(selling_speed=='Fast'):
            return 'F'
        elif(selling_speed=='Medium'):
            return 'M'
        elif(selling_speed=='Slow'):
            return 'S'
        elif(selling_speed == 'Very Slow'):
            return 'VS'
    def calculate_week_dates(self, start_date):
        weeks = []
        for i in range(4):
            week_start = start_date + timedelta(weeks=i)
            week_end = week_start + timedelta(days=6)
            weeks.append((week_start, week_end))
        return weeks

    def findLastReorderDate(self, start_week_1, end_week_1, start_week_2, end_week_2, start_week_3, end_week_3, start_week_4, end_week_4):
        start_date = date(2024, 9, 1)
        weeks = self.calculate_week_dates(start_date)
        if start_week_4 > end_week_3:
            return weeks[3][0]  # Return start date of week 4
        elif start_week_3 > end_week_2:
            return weeks[2][0]  # Return start date of week 3
        elif start_week_2 > end_week_1:
            return weeks[1][0]  # Return start date of week 2
        else:
            return weeks[0][0]  # Return start date of week 1
        
    def handle(self, *args, **kwargs):
        file_path = './assets/data/data.csv'  # Path to your CSV file
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                code = row['CODE']  # This corresponds to the Drug model's ID
                drug = Drug.objects.filter(id=code).first()  # Get the Drug instance

                if not drug:
                    self.stdout.write(self.style.WARNING(f'Drug with ID {code} not found.'))
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
                selling_speed = row['Selling Speed']
                reorder_point = int(row['Reorder Point']) if row['Reorder Point'] else 10  # Default if not specified

                # Create or update the stock instance for the drug
                stock = Stock(
                    drug=drug,
                    level=end_week_4,
                    lastReorderDate = self.findLastReorderDate(start_week_1, end_week_1, start_week_2, end_week_2, start_week_3, end_week_3, start_week_4, end_week_4),
                    reorderPoint=reorder_point,
                    sellingSpeed=self.handle_selling_speed(selling_speed)
                )
                stock.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded stock data'))
