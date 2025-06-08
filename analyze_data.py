import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import os

# Set the style for the plots
plt.style.use('ggplot')
sns.set(font_scale=1.2)
sns.set_style("whitegrid")

# Create custom colormap
colors = ["#4e79a7", "#f28e2c", "#e15759", "#76b7b2", "#59a14f", "#edc949", "#af7aa1", "#ff9da7", "#9c755f", "#bab0ab"]

# Set output directory
output_dir = '/home/ubuntu/trip_data_visualization'
os.makedirs(output_dir, exist_ok=True)

# Load the JSON data
with open('/home/ubuntu/trip_data_visualization/public_cases.json', 'r') as f:
    data = json.load(f)

# Convert to pandas DataFrame
records = []
for item in data:
    record = {
        'trip_duration_days': item['input']['trip_duration_days'],
        'miles_traveled': item['input']['miles_traveled'],
        'total_receipts_amount': item['input']['total_receipts_amount'],
        'expected_output': item['expected_output']
    }
    records.append(record)

df = pd.DataFrame(records)

# Save the basic statistics
stats = df.describe()
stats.to_csv(f'{output_dir}/data_statistics.csv')

# Print basic information about the dataset
print("Data Shape:", df.shape)
print("\nData Types:")
print(df.dtypes)
print("\nBasic Statistics:")
print(stats)

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Calculate additional metrics
df['cost_per_mile'] = df['expected_output'] / df['miles_traveled']
df['cost_per_day'] = df['expected_output'] / df['trip_duration_days']
df['receipts_percentage'] = (df['total_receipts_amount'] / df['expected_output']) * 100

# Group data by trip duration
duration_groups = df.groupby('trip_duration_days').agg({
    'miles_traveled': 'mean',
    'total_receipts_amount': 'mean',
    'expected_output': 'mean',
    'cost_per_mile': 'mean',
    'cost_per_day': 'mean',
    'receipts_percentage': 'mean'
}).reset_index()

print("\nAverage values by trip duration:")
print(duration_groups)

# Save the processed data
df.to_csv(f'{output_dir}/processed_data.csv', index=False)
duration_groups.to_csv(f'{output_dir}/duration_groups.csv', index=False)

print("\nData analysis complete. Results saved to CSV files.")

