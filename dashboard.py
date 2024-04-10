import matplotlib.pyplot as plt
import pandas as pd

# Sample time series data
time_series_data = pd.DataFrame({
    'Date': pd.date_range('2023-01-01', periods=10, freq='D'),
    'Value': [10, 15, 20, 18, 25, 30, 28, 35, 40, 45]
})

# Sample categorical data
categorical_data = pd.DataFrame({
    'Date': ['2023-01-03', '2023-01-06', '2023-01-09'],
    'Category': ['A', 'B', 'C']
})

# Convert the 'Date' columns to datetime objects
time_series_data['Date'] = pd.to_datetime(time_series_data['Date'])
categorical_data['Date'] = pd.to_datetime(categorical_data['Date'])

# Create a figure and axis
fig, ax = plt.subplots()

# Plot the time series data as a line chart
ax.plot(time_series_data['Date'], time_series_data['Value'], label='Time Series Data', marker='o')

# Scatter the categorical data points on top of the line chart
ax.scatter(categorical_data['Date'], time_series_data['Value'][categorical_data['Date']],
            marker='o', color='red', label='Categorical Data')

# Set labels and legend
ax.set_xlabel('Date')
ax.set_ylabel('Value')
ax.legend()

# Show the plot
plt.show()
