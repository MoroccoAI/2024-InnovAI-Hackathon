from dashboard.models import *
from django.db.models import Sum, F, FloatField
from datetime import datetime, timedelta , date
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncDay , TruncDate
from django.http import JsonResponse
from collections import defaultdict
import pandas as pd
import numpy as np
import joblib

def fetch_sales_data():
    sales = Sale.objects.all() # Fetch all sales data
    return sales
    
# Dashboard functions : 
#---------------------------------------------------

def getDashboardData():
    # Get today's date
    today = datetime.now().date()

    # Get the latest 30 sales ordered by the most recent sale date
    recent_sales = Sale.objects.all().order_by('-date', '-time')[:30]

    # Get the sales data grouped by month
    monthly_sales = (
        Sale.objects.annotate(month=TruncMonth('date'))  # Truncate date to month
        .values('month')  # Group by month
        .annotate(total_sales=Sum('quantity'))  # Calculate total quantity sold
        .order_by('month')  # Sort by month
    )

    # Calculate the stock progress based on sales for each month
    progress = []
    previous_stock = 1000  # You can replace this with your actual starting stock, or calculate it dynamically

    for month_data in monthly_sales:
        month = month_data['month']
        total_sales = month_data['total_sales'] or 0  # Handle null values for sales
        
        # Calculate the remaining stock after sales in the month
        remaining_stock = previous_stock - total_sales
        
        # Append the current month progress
        progress.append({
            "month": month.strftime('%b'),  # Format month as 'Jan', 'Feb', etc.
            "total_sales": total_sales,
            "remaining_stock": remaining_stock,
        })
        
        # Update previous_stock for the next month
        previous_stock = remaining_stock

    # Get today's earnings (using the PPV field from the Drug model)
    total_earnings = Sale.objects.filter(date=today).aggregate(
        total=Sum(F('quantity') * F('drug__PPV'), output_field=FloatField())
    )['total'] or 0

    # Get lifetime sales and total sales
    total_sales = Sale.objects.aggregate(total_sales=Sum('quantity'))['total_sales'] or 0
    total_sales_total = Sale.objects.aggregate(
        total=Sum(F('quantity') * F('drug__PPV'), output_field=FloatField())
    )['total'] or 0

    # Get category sales
    category_sales = Sale.objects.values('drug__class_therapeutique').annotate(total_sales=Sum('quantity')).order_by('-total_sales')

    # Sort categories by sales count in descending order and get the top 4
    top_categories = category_sales[:4]
    
    # Calculate total sales for the top 4 categories
    top_categories_total = sum([category['total_sales'] for category in top_categories])
    
    # Calculate percentages for the top 4 categories
    top_categories_percentages = {category['drug__class_therapeutique']: (category['total_sales'] / top_categories_total) * 100 for category in top_categories}

    result = {
        "recentSales": recent_sales,
        "monthlyProgress": progress,
        "totalEarnings": total_earnings,
        "totalSales": total_sales,
        "totalSalesTotal": total_sales_total,
        "topCategoriesPercentages": top_categories_percentages
    }
    
    return result
#---------------------------------------------------

# Sales Report functions : 
#---------------------------------------------------
 
def getLastThirtyDaysSales():
    today = datetime.now().date()
    start_date = today - timedelta(days=29)
    
    # Fetch raw sales data (adjust to fetch data from your database or an API)
    sales_data = Sale.objects.filter(date__range=(start_date, today))
    
    # Prepare the structure for daily and weekly sales
    all_sales = defaultdict(list)  # Holds daily sales
    total_week = {f"week_{i+1}": {"date": None, "total_sales": 0} for i in range(4)}
    
    # Helper to group days into weeks
    def get_week_number(sale_date):
        delta_days = (sale_date - start_date).days
        return delta_days // 7 + 1  # Week 1, 2, 3, or 4
    
    # Process each sale
    for sale in sales_data:
        sale_date = sale.date
        if start_date <= sale_date <= today:
            all_sales[str(sale_date)].append(sale)
            week_number = get_week_number(sale_date)
            total_week[f"week_{week_number}"]["total_sales"] += sale.quantity  # Use 'quantity' field
    
    # Add week date ranges
    for i in range(4):
        week_start = start_date + timedelta(days=i * 7)
        week_end = min(week_start + timedelta(days=6), today)
        total_week[f"week_{i+1}"]["date"] = f"{week_start} - {week_end}"
    
    # Final output structure
    return {
        "total_week": total_week,
        "all": dict(all_sales)  # Convert defaultdict to a normal dict
    }
    
#---------------------------------------------------


# Stock Report functions : 
#---------------------------------------------------
 
def getLastMonthStock():
    """
    Gets the last 4 weeks of stock data dynamically based on the available archive data.
    Returns:
        {
            'week1': {
                'weekDate': 'Oct 1 - Oct 7',
                'totalStock': 1000,
                'all': {'group 1': 340, 'group 2': 560, ...}
            },
            'week2': {
                'weekDate': 'Oct 8 - Oct 15',
                'totalStock': 1000,
                'all': {'group 1': 340, 'group 2': 560, ...}
            },
            ...
        }
    """
    # Fetch the earliest and latest lastReorderDate from the database to define the range of available data
    first_date = Stock.objects.order_by('lastReorderDate').first().lastReorderDate
    last_date = Stock.objects.order_by('-lastReorderDate').first().lastReorderDate
    
    # Initialize end_date as the latest available date (usually Sunday or the last day of the week)
    # Calculate the last Sunday date from the `last_date`
    end_date = last_date - timedelta(days=last_date.weekday()) + timedelta(days=6)
    
    # Result dictionary to store stock data for the last 4 weeks
    result = {}

    # Loop to go through the last 4 weeks dynamically
    for week_index in range(4):
        # The start of the week is 6 days before the end date
        start_date = end_date - timedelta(days=6)

        # Fetch stock data for the week, grouped by therapeutic class
        weekly_stock = Stock.objects.filter(
            lastReorderDate__range=[start_date, end_date]
        ).select_related('drug')

        # Initialize data for the current week
        week_data = {
            'weekDate': f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d')}",
            'totalStock': 0,
            'all': defaultdict(int),
        }

        # Aggregate the stock data by class_therapeutique
        for stock in weekly_stock:
            group = stock.drug.class_therapeutique
            week_data['totalStock'] += stock.level
            week_data['all'][group] += stock.level

        # Convert defaultdict to regular dict
        week_data['all'] = dict(week_data['all'])

        # Save the week's data into the result dictionary
        result[f'week{4 - week_index}'] = week_data

        # Move the end_date to the previous week (Saturday of the previous week)
        end_date = start_date - timedelta(days=1)
        
        # Make sure the end_date does not go past the first available date
        if end_date < first_date:
            break
    
    # Print the result for debugging purposes
    print(result)
    
    return result

#---------------------------------------------------

# Shortage Prediction functions :
#---------------------------------------------------
def predictShortages():
    # Step 1: Fetch drug data with archives
    drug_data = fetch_all_drugs_with_archives()

    # Step 2: Prepare data for prediction
    data_to_predict = prepare_data_for_prediction(drug_data)

    # Step 3: Load the pre-trained AI model and encoder
    model = joblib.load("C:\\Users\\moustaid\\Desktop\\DSPP\\Drug-Availabilty-Tracker\\dashboard\\API\\shortagePredModel.pkl")
    encoder = joblib.load("C:\\Users\\moustaid\\Desktop\\DSPP\\Drug-Availabilty-Tracker\\dashboard\\API\\onehot_encoder.pkl")

    # Load feature names from training
    with open("C:\\Users\\moustaid\\Desktop\\DSPP\\Drug-Availabilty-Tracker\\dashboard\\API\\feature_names.pkl", "rb") as f:
        trained_feature_names = joblib.load(f)

    # Step 4: Encode categorical columns
    categorical_columns = ['SPECIALITE', 'SUBSTANCE ACTIVE', 'CLASSE THERAPEUTIQUE', 'Selling Speed']
    categorical_data = encoder.transform(data_to_predict[categorical_columns])

    # Combine numerical and encoded categorical data
    numerical_columns = [
        'Reorder Point',
        'Start of Week 1 Stock', 'Week 1 Sales', 'End of Week 1 Stock',
        'Start of Week 2 Stock', 'Week 2 Sales', 'End of Week 2 Stock',
        'Start of Week 3 Stock', 'Week 3 Sales', 'End of Week 3 Stock'
    ]
    numerical_data = data_to_predict[numerical_columns].to_numpy()

    # Concatenate numerical and categorical data
    combined_data = np.hstack([numerical_data, categorical_data])

    # Align with the trained feature names
    final_data = pd.DataFrame(combined_data, columns=numerical_columns + list(encoder.get_feature_names_out()))
    for col in trained_feature_names:
        if col not in final_data:
            final_data[col] = 0
    final_data = final_data[trained_feature_names]

    # Step 5: Predict shortages
    predictions = model.predict(final_data)

    # Validate categorical columns  tbeforeransformation
    missing_categorical_columns = [col for col in categorical_columns if col not in data_to_predict.columns]
    if missing_categorical_columns:
        raise ValueError(f"Missing categorical columns: {missing_categorical_columns}")


    # Step 6: Add predictions to the drug data
    for index, drug in enumerate(drug_data):
        drug['shortage_prediction'] = bool(predictions[index])

    return drug_data


def prepare_data_for_prediction(drug_data):
    """Prepare drug data for model prediction matching training preprocessing"""
    import pandas as pd

    # Convert to DataFrame
    df = pd.DataFrame(drug_data)

    # Define all columns
    all_columns = [
        'SPECIALITE', 'SUBSTANCE ACTIVE', 'CLASSE THERAPEUTIQUE', 'Selling Speed',
        'Reorder Point',
        'Start of Week 1 Stock', 'Week 1 Sales', 'End of Week 1 Stock',
        'Start of Week 2 Stock', 'Week 2 Sales', 'End of Week 2 Stock',
        'Start of Week 3 Stock', 'Week 3 Sales', 'End of Week 3 Stock'
    ]

    # Ensure all required columns are present, default missing to a placeholder
    for col in all_columns:
        if col not in df:
            df[col] = "Unknown" if col in ['SPECIALITE', 'SUBSTANCE ACTIVE', 'CLASSE THERAPEUTIQUE', 'Selling Speed'] else 0

    return df

def fetch_all_drugs_with_archives():
    # Step 1: Fetch all drugs
    drugs = Drug.objects.all()
    
    # Step 2: Prepare the result list
    result = []

    # Step 3: Loop through each drug and fetch its archives
    for drug in drugs:
        # Fetch archives for the drug, sorted by the start of the week
        archives = Archive.objects.filter(stock__drug=drug).order_by('sowd')
        
        # Initialize drug data with exact column names matching X
        drug_data = {
            'SPECIALITE': drug.name or "Unknown",
            'SUBSTANCE ACTIVE': drug.substances or "Unknown",
            'CLASSE THERAPEUTIQUE': drug.class_therapeutique or "Unknown",
            'Selling Speed': "Unknown",
            'Reorder Point': 0,
            'Start of Week 1 Stock': 0,
            'Week 1 Sales': 0,
            'End of Week 1 Stock': 0,
            'Start of Week 2 Stock': 0,
            'Week 2 Sales': 0,
            'End of Week 2 Stock': 0,
            'Start of Week 3 Stock': 0,
            'Week 3 Sales': 0,
            'End of Week 3 Stock': 0
        }

        
        totaleSales = 0
        # Populate weekly data for exactly 3 weeks
        for week_num, archive in enumerate(archives[:3], start=1):
            drug_data[f'Start of Week {week_num} Stock'] = archive.sows
            drug_data[f'Week {week_num} Sales'] = archive.sales
            drug_data[f'End of Week {week_num} Stock'] = archive.eows
            totaleSales += archive.sales
        
        sellingSpeed, sellingSpeedValue = calculate_selling_speed(totaleSales)            
        drug_data['Selling Speed'] = sellingSpeed
        drug_data['Reorder Point'] = getReorderPoint(sellingSpeedValue)
        
        # Add the drug data to the result list
        result.append(drug_data)
    
    return result
# Define function to calculate selling speed
def calculate_selling_speed(totalSales):
    avg_sales = totalSales / 4
    
    if avg_sales <= 10:
        return 'Very Slow', 1
    elif avg_sales <= 20:
        return 'Slow', 2
    elif avg_sales <= 30:
        return 'Medium', 3
    elif avg_sales <= 50:
        return 'Fast', 4
    else:
        return 'Very Fast', 5

# Define function to calculate selling speed
def getReorderPoint(sellingSpeed):
    return sellingSpeed * 10



