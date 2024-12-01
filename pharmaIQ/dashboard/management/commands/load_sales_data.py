import csv
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from dashboard.models import Drug, Sale
from datetime import date, datetime, timedelta

class Command(BaseCommand):
    help = 'Load sales data from CSV file and save into Sale model'

    def calculate_sales_dates(self, week_start_date):
        return [week_start_date + timedelta(days=i) for i in range(7)]

    def random_time(self):
        """Generate a random time within a day."""
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        return datetime.time(datetime(1, 1, 1, hour, minute, second))

    def handle(self, *args, **kwargs):
        file_path = './assets/data/data.csv'  # Path to your CSV file
        start_date = date(2024, 9, 1)  # Start date for week 1

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                code = row['CODE']  # This corresponds to the Drug model's ID
                drug = Drug.objects.filter(id=code).first()  # Get the Drug instance

                if not drug:
                    self.stdout.write(self.style.WARNING(f'Drug with ID {code} not found.'))
                    continue

                # Sales data for each week
                week_sales = [
                    int(row.get(f'Week {i} Sales', 0) or 0) for i in range(1, 5)
                ]

                # Calculate sales dates
                week_dates = self.calculate_sales_dates(start_date)

                # Process sales for each week
                for week_index, total_sales in enumerate(week_sales):
                    if total_sales > 0:
                        # Randomly distribute total_sales across the week
                        daily_sales = []
                        remaining_sales = total_sales
                        for day in range(7):
                            if day < 6:  # Allow some sales to roll into the last day
                                sales_today = random.randint(0, remaining_sales // (7 - day))
                                daily_sales.append(sales_today)
                                remaining_sales -= sales_today
                            else:
                                daily_sales.append(remaining_sales)  # Assign the remaining sales to the last day

                        # Create sales for each day
                        for day_index, sales in enumerate(daily_sales):
                            if sales > 0:
                                # Directly create sale entries for the specific drug from the CSV
                                Sale.objects.create(
                                    drug=drug,  # Use the specific drug ID from CSV
                                    quantity=sales,
                                    date=week_dates[day_index] + timedelta(weeks=week_index),
                                    time=self.random_time(),  # Random time within the day
                                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded sales data'))
