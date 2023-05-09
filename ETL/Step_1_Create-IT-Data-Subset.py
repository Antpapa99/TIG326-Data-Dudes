import json

# Open the JSON file and load the data
with open(r'C:\Users\Anthony\Desktop\JSON_data\2023.json', 'r') as f:
    data = json.load(f)

# Define the target concept_id
target_concept_id = 'apaJ_2ja_LuF'

# Create a new list to store the filtered data
filtered_data = []

# Loop through each data sample in the dataset
for sample in data:
    # Check if the occupation_group has the desired concept_id
    if sample.get('occupation_field', {}).get('concept_id') == target_concept_id:
        # Remove newline characters from relevant fields
        if "headline" in sample:
            sample["headline"] = sample["headline"].replace('\n', ' ')
        if "description" in sample and "text" in sample["description"]:
            sample["description"]["text"] = sample["description"]["text"].replace('\n', ' ')

        # Add the sample to the filtered data list
        filtered_data.append(sample)

# Save the filtered data to a new JSON file
with open(r'C:\Users\Anthony\Desktop\JSON_data\afiltered_data.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)  # Set ensure_ascii to False

print("done")
