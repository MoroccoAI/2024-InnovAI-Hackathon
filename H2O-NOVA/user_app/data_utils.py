import calendar

import pandas as pd
from constants import DATA_PATH, THRESHOLD


def update_data(price, water_usage, city_threshold=THRESHOLD):
    df = pd.read_csv(DATA_PATH)
    # Extract the last row's month (assuming the 'Month' column is in YYYY-MM-DD format)
    last_row_date = pd.to_datetime(df['Month'].iloc[-1])

    # Calculate the next month and handle year change if necessary
    next_month = (last_row_date.month % 12) + 1
    next_year = last_row_date.year if next_month != 1 else last_row_date.year + 1

    _, last_day = calendar.monthrange(next_year, next_month)
    next_month_last_day = f"{next_year}-{next_month:02d}-{last_day:02d}"

    next_month_data = pd.DataFrame({
        'Month': [next_month_last_day],
        'User Water Usage (liters)': [water_usage],
        'City Threshold (liters)': [city_threshold],
        'Price': [price]
    })

    # Concatenate the new row to the existing DataFrame
    df = pd.concat([df, next_month_data], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)

    return df
