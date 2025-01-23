import pandas as pd

# Generate synthetic manufacturing data
data = {
    'Machine_ID': ['M001', 'M002', 'M003'] * 33,  # Repeat for consistent data
    'Temperature': [72.5, 85.3, 68.9] * 33,      # Repeat the values
    'Run_Time': list(range(120, 120 + 3 * 99, 3)),  # Generate runtime values
    'Downtime_Flag': [0, 0, 1] * 33               # Repeated flags
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('machine_data.csv', index=False)

# Print DataFrame info
print("Sample Data:")
print(df.head())

