import pandas as pd
import json
import os

# Create an empty list to store DataFrames
data_frames = []

# List of JSON files
 # Replace with your actual file names

# Loop over each JSON file
for i in range(1,156) :
    file_name='map ('+str(i)+')'
    with open(file_name, 'r') as file:
        json_data = json.load(file)

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(json_data)

    # Append the DataFrame to the list
    data_frames.append(df)

# Concatenate all DataFrames into a single DataFrame
final_df = pd.concat(data_frames, ignore_index=True)

# Print the final DataFrame
print(final_df)
final_df.to_csv('intel_data.csv')
