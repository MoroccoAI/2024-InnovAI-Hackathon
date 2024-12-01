import os
import pandas as pd
import joblib
from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")  # Replace 'myproject' with your project name
application = get_wsgi_application()

# Import your model
from myapp.models import Medicine  # Replace 'myapp' and 'Medicine' with your app and model names

# Load the trained Random Forest model
model = joblib.load('shortagePredModel.pkl')

# Load data from the database
print("Fetching data from the database...")
medicines = Medicine.objects.all()
data = pd.DataFrame(list(medicines.values()))

# Check if data is empty
if data.empty:
    print("No data found in the database.")
    exit()

# Prepare the features for prediction
print("Preparing data for prediction...")
required_columns = [
    'SUBSTANCE ACTIVE', 'CLASSE THERAPEUTIQUE', 'Selling Speed', 'Reorder Point',
    'Start of Week 1 Stock', 'Week 1 Sales', 'End of Week 1 Stock',
    'Start of Week 2 Stock', 'Week 2 Sales', 'End of Week 2 Stock',
    'Start of Week 3 Stock', 'Week 3 Sales', 'End of Week 3 Stock'
]

# Ensure the required columns are present
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    print(f"Missing columns in the database: {missing_columns}")
    exit()

X_new = data[required_columns]

# Encode categorical variables
print("Encoding categorical variables...")
X_new = pd.get_dummies(X_new, drop_first=True)

# Ensure features match the training data
model_features = joblib.load('model_features.pkl')  # Save this during training
X_new = X_new.reindex(columns=model_features, fill_value=0)

# Run the model to make predictions
print("Running predictions...")
predictions = model.predict(X_new)

# Add predictions back to the database
print("Updating predictions in the database...")
for index, row in data.iterrows():
    medicine = Medicine.objects.get(id=row['id'])  # Replace 'id' with your primary key field
    medicine.shortage_prediction = predictions[index]  # Replace with the correct field name
    medicine.save()

print("Predictions updated successfully!")
