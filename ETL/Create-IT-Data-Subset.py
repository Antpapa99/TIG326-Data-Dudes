import json

# Open the JSON file and load the data
with open('2023.json', 'r') as f:
    data = json.load(f)

# Define the target concept_id
target_concept_id = 'apaJ_2ja_LuF'

# Create a new list to store the filtered data
filtered_data = []

# Loop through each data sample in the dataset
for sample in data:
    # Check if the occupation_group has the desired concept_id
    if sample.get('occupation_field', {}).get('concept_id') == target_concept_id:
        # Add the sample to the filtered data list
        filtered_data.append(sample)

# Save the filtered data to a new JSON file
with open('filtered_data.json', 'w') as f:
    json.dump(filtered_data, f, indent=4)  # Set the indent parameter to 4

print("done")
