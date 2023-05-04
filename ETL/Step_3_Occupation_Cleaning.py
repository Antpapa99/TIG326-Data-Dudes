import json

with open('Job_Dictionary.json', 'r') as file:
    data = [json.loads(line) for line in file]

# Merge dictionaries with the same occupation-type
merged_data = {}
for item in data:
    occupation_type = item['Occupation-type']
    if occupation_type not in merged_data:
        merged_data[occupation_type] = {
            'Occupation-type': occupation_type,
            'Skills': item['Skills']
        }
    else:
        merged_data[occupation_type]['Skills'].extend(item['Skills'])

# Remove duplicates in skills list
for occupation_type, item in merged_data.items():
    item['Skills'] = list(set(item['Skills']))

# Convert merged_data into a list of dictionaries
merged_data_list = list(merged_data.values())

# Save the merged data to a new JSON file
with open('merged_jobdictionary.json', 'w') as file:
    json.dump(merged_data_list, file, ensure_ascii=False, indent=4)
