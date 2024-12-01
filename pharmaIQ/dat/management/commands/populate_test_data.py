from django.core.management.base import BaseCommand
from dashboard.models import Customer, Sale, Product, Order
from django.utils import timezone
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database...')

        # Create Customers
        customers = [
            Customer.objects.create(name=f"Customer {i}") for i in range(1, 6)
        ]

        # Create Products
        products = [
            Product.objects.create(
                name=f"Product {i}",
                price=Decimal(random.uniform(10, 100)).quantize(Decimal('0.01')),
                stock=random.randint(10, 100)
            ) for i in range(1, 11)
        ]

        # Create Sales
        for _ in range(20):
            Sale.objects.create(
                customer=random.choice(customers),
                amount=Decimal(random.uniform(50, 500)).quantize(Decimal('0.01')),
                date=timezone.now() - timezone.timedelta(days=random.randint(0, 30))
            )

        # Create Orders
        statuses = ['Pending', 'Shipped', 'Delivered']
        for _ in range(15):
            Order.objects.create(
                medicine_name=f"Medicine {random.randint(1, 10)}",
                expire_date=timezone.now().date() + timezone.timedelta(days=random.randint(30, 365)),
                quantity=random.randint(1, 50),
                batch_no=f"BATCH-{random.randint(1000, 9999)}",
                status=random.choice(statuses),
                price=Decimal(random.uniform(5, 200)).quantize(Decimal('0.01'))
            )

        self.stdout.write(self.style.SUCCESS('Database successfully populated with test data!'))