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

# Load the processed data
df = pd.read_csv(f'{output_dir}/processed_data.csv')

# Create a figure with multiple subplots
fig = plt.figure(figsize=(20, 24))

# 1. Distribution of Expected Output
plt.subplot(4, 3, 1)
plt.hist(df['expected_output'], bins=30, color=colors[0], alpha=0.7, edgecolor='black')
plt.title('Distribution of Expected Output (Trip Costs)', fontsize=14, fontweight='bold')
plt.xlabel('Expected Output ($)')
plt.ylabel('Frequency')
plt.grid(True, alpha=0.3)

# 2. Trip Duration vs Expected Output
plt.subplot(4, 3, 2)
plt.scatter(df['trip_duration_days'], df['expected_output'], alpha=0.6, color=colors[1], s=50)
plt.title('Trip Duration vs Expected Output', fontsize=14, fontweight='bold')
plt.xlabel('Trip Duration (Days)')
plt.ylabel('Expected Output ($)')
plt.grid(True, alpha=0.3)

# 3. Miles Traveled vs Expected Output
plt.subplot(4, 3, 3)
plt.scatter(df['miles_traveled'], df['expected_output'], alpha=0.6, color=colors[2], s=50)
plt.title('Miles Traveled vs Expected Output', fontsize=14, fontweight='bold')
plt.xlabel('Miles Traveled')
plt.ylabel('Expected Output ($)')
plt.grid(True, alpha=0.3)

# 4. Receipts Amount vs Expected Output
plt.subplot(4, 3, 4)
plt.scatter(df['total_receipts_amount'], df['expected_output'], alpha=0.6, color=colors[3], s=50)
plt.title('Receipts Amount vs Expected Output', fontsize=14, fontweight='bold')
plt.xlabel('Total Receipts Amount ($)')
plt.ylabel('Expected Output ($)')
plt.grid(True, alpha=0.3)

# 5. Box plot of Expected Output by Trip Duration
plt.subplot(4, 3, 5)
df.boxplot(column='expected_output', by='trip_duration_days', ax=plt.gca())
plt.title('Expected Output by Trip Duration', fontsize=14, fontweight='bold')
plt.xlabel('Trip Duration (Days)')
plt.ylabel('Expected Output ($)')
plt.suptitle('')  # Remove the automatic title

# 6. Cost per Mile Distribution
plt.subplot(4, 3, 6)
plt.hist(df['cost_per_mile'], bins=30, color=colors[4], alpha=0.7, edgecolor='black')
plt.title('Distribution of Cost per Mile', fontsize=14, fontweight='bold')
plt.xlabel('Cost per Mile ($)')
plt.ylabel('Frequency')
plt.grid(True, alpha=0.3)

# 7. Cost per Day Distribution
plt.subplot(4, 3, 7)
plt.hist(df['cost_per_day'], bins=30, color=colors[5], alpha=0.7, edgecolor='black')
plt.title('Distribution of Cost per Day', fontsize=14, fontweight='bold')
plt.xlabel('Cost per Day ($)')
plt.ylabel('Frequency')
plt.grid(True, alpha=0.3)

# 8. Receipts Percentage Distribution
plt.subplot(4, 3, 8)
plt.hist(df['receipts_percentage'], bins=30, color=colors[6], alpha=0.7, edgecolor='black')
plt.title('Distribution of Receipts as % of Total Cost', fontsize=14, fontweight='bold')
plt.xlabel('Receipts Percentage (%)')
plt.ylabel('Frequency')
plt.grid(True, alpha=0.3)

# 9. Average Cost per Day by Trip Duration
duration_groups = df.groupby('trip_duration_days')['cost_per_day'].mean()
plt.subplot(4, 3, 9)
plt.bar(duration_groups.index, duration_groups.values, color=colors[7], alpha=0.8)
plt.title('Average Cost per Day by Trip Duration', fontsize=14, fontweight='bold')
plt.xlabel('Trip Duration (Days)')
plt.ylabel('Average Cost per Day ($)')
plt.grid(True, alpha=0.3)

# 10. Average Miles Traveled by Trip Duration
miles_by_duration = df.groupby('trip_duration_days')['miles_traveled'].mean()
plt.subplot(4, 3, 10)
plt.plot(miles_by_duration.index, miles_by_duration.values, marker='o', linewidth=3, markersize=8, color=colors[8])
plt.title('Average Miles Traveled by Trip Duration', fontsize=14, fontweight='bold')
plt.xlabel('Trip Duration (Days)')
plt.ylabel('Average Miles Traveled')
plt.grid(True, alpha=0.3)

# 11. Correlation Heatmap
plt.subplot(4, 3, 11)
correlation_matrix = df[['trip_duration_days', 'miles_traveled', 'total_receipts_amount', 'expected_output']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, square=True, 
            cbar_kws={'shrink': 0.8}, fmt='.2f')
plt.title('Correlation Matrix', fontsize=14, fontweight='bold')

# 12. Trip Duration Distribution
plt.subplot(4, 3, 12)
duration_counts = df['trip_duration_days'].value_counts().sort_index()
plt.bar(duration_counts.index, duration_counts.values, color=colors[9], alpha=0.8)
plt.title('Distribution of Trip Durations', fontsize=14, fontweight='bold')
plt.xlabel('Trip Duration (Days)')
plt.ylabel('Number of Trips')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/comprehensive_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("Comprehensive analysis chart saved!")

# Create a detailed scatter plot matrix
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Scatter plot 1: Duration vs Output with color by miles
scatter1 = axes[0, 0].scatter(df['trip_duration_days'], df['expected_output'], 
                             c=df['miles_traveled'], cmap='viridis', alpha=0.7, s=60)
axes[0, 0].set_title('Trip Duration vs Expected Output\n(Color: Miles Traveled)', fontweight='bold')
axes[0, 0].set_xlabel('Trip Duration (Days)')
axes[0, 0].set_ylabel('Expected Output ($)')
plt.colorbar(scatter1, ax=axes[0, 0], label='Miles Traveled')

# Scatter plot 2: Miles vs Output with color by duration
scatter2 = axes[0, 1].scatter(df['miles_traveled'], df['expected_output'], 
                             c=df['trip_duration_days'], cmap='plasma', alpha=0.7, s=60)
axes[0, 1].set_title('Miles Traveled vs Expected Output\n(Color: Trip Duration)', fontweight='bold')
axes[0, 1].set_xlabel('Miles Traveled')
axes[0, 1].set_ylabel('Expected Output ($)')
plt.colorbar(scatter2, ax=axes[0, 1], label='Trip Duration (Days)')

# Scatter plot 3: Receipts vs Output with color by duration
scatter3 = axes[1, 0].scatter(df['total_receipts_amount'], df['expected_output'], 
                             c=df['trip_duration_days'], cmap='coolwarm', alpha=0.7, s=60)
axes[1, 0].set_title('Receipts Amount vs Expected Output\n(Color: Trip Duration)', fontweight='bold')
axes[1, 0].set_xlabel('Total Receipts Amount ($)')
axes[1, 0].set_ylabel('Expected Output ($)')
plt.colorbar(scatter3, ax=axes[1, 0], label='Trip Duration (Days)')

# Scatter plot 4: Cost per mile vs Cost per day
scatter4 = axes[1, 1].scatter(df['cost_per_mile'], df['cost_per_day'], 
                             c=df['trip_duration_days'], cmap='spring', alpha=0.7, s=60)
axes[1, 1].set_title('Cost per Mile vs Cost per Day\n(Color: Trip Duration)', fontweight='bold')
axes[1, 1].set_xlabel('Cost per Mile ($)')
axes[1, 1].set_ylabel('Cost per Day ($)')
plt.colorbar(scatter4, ax=axes[1, 1], label='Trip Duration (Days)')

plt.tight_layout()
plt.savefig(f'{output_dir}/detailed_scatter_plots.png', dpi=300, bbox_inches='tight')
plt.close()

print("Detailed scatter plots saved!")

# Create trend analysis charts
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Average values by trip duration
duration_stats = df.groupby('trip_duration_days').agg({
    'expected_output': 'mean',
    'miles_traveled': 'mean',
    'total_receipts_amount': 'mean',
    'cost_per_mile': 'mean',
    'cost_per_day': 'mean',
    'receipts_percentage': 'mean'
}).reset_index()

# Plot 1: Expected Output Trend
axes[0, 0].plot(duration_stats['trip_duration_days'], duration_stats['expected_output'], 
                marker='o', linewidth=3, markersize=8, color=colors[0])
axes[0, 0].set_title('Average Expected Output by Trip Duration', fontweight='bold')
axes[0, 0].set_xlabel('Trip Duration (Days)')
axes[0, 0].set_ylabel('Average Expected Output ($)')
axes[0, 0].grid(True, alpha=0.3)

# Plot 2: Cost per Day Trend
axes[0, 1].plot(duration_stats['trip_duration_days'], duration_stats['cost_per_day'], 
                marker='s', linewidth=3, markersize=8, color=colors[1])
axes[0, 1].set_title('Average Cost per Day by Trip Duration', fontweight='bold')
axes[0, 1].set_xlabel('Trip Duration (Days)')
axes[0, 1].set_ylabel('Average Cost per Day ($)')
axes[0, 1].grid(True, alpha=0.3)

# Plot 3: Cost per Mile Trend
axes[1, 0].plot(duration_stats['trip_duration_days'], duration_stats['cost_per_mile'], 
                marker='^', linewidth=3, markersize=8, color=colors[2])
axes[1, 0].set_title('Average Cost per Mile by Trip Duration', fontweight='bold')
axes[1, 0].set_xlabel('Trip Duration (Days)')
axes[1, 0].set_ylabel('Average Cost per Mile ($)')
axes[1, 0].grid(True, alpha=0.3)

# Plot 4: Receipts Percentage Trend
axes[1, 1].plot(duration_stats['trip_duration_days'], duration_stats['receipts_percentage'], 
                marker='d', linewidth=3, markersize=8, color=colors[3])
axes[1, 1].set_title('Average Receipts Percentage by Trip Duration', fontweight='bold')
axes[1, 1].set_xlabel('Trip Duration (Days)')
axes[1, 1].set_ylabel('Average Receipts Percentage (%)')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/trend_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("Trend analysis charts saved!")

print("All visualizations have been created successfully!")

