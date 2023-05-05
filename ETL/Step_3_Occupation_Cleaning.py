import json

with open('Job_Dictionary.json', 'r') as file:
    data = [json.loads(line) for line in file]

# Merge dictionaries with the same occupation-type
merged_data = {}
for item in data:
    occupation_type = item['Occupation-type']
    if occupation_type not in merged_data:
        merged_data[occupation_type] = {
            'label': occupation_type,
            'skills': []
        }
    for skill in item['Skills']:
        skill_found = False
        for existing_skill in merged_data[occupation_type]['skills']:
            if existing_skill['name'] == skill:
                existing_skill['count'] += 1
                skill_found = True
                break
        if not skill_found:
            merged_data[occupation_type]['skills'].append({
                'name': skill,
                'count': 1
            })

# Sort skills based on the count
for occupation_type in merged_data.values():
    occupation_type['skills'] = sorted(occupation_type['skills'], key=lambda x: x['count'], reverse=True)

# Convert merged_data into a list of dictionaries
merged_data_list = list(merged_data.values())

# Save the merged data to a new JSON file
with open('merged_jobdictionary.json', 'w') as file:
    json.dump(merged_data_list, file, ensure_ascii=False, indent=4)

print("Done")
