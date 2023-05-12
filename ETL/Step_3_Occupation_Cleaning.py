import json

with open('Job_Dictionary.json', 'r') as file:
    data = [json.loads(line) for line in file]

# Merge dictionaries with the same occupation-AI_classify
merged_data = {}
occupation_counts = {}

for item in data:
    for occupation_ai_classify in item['Occupation-AI_classify']:
        if occupation_ai_classify not in merged_data:
            merged_data[occupation_ai_classify] = {
                'label': occupation_ai_classify,
                'skills': [],
                'count': 1  # Increment count for each occupation encountered
            }
            occupation_counts[occupation_ai_classify] = 1  # Initialize occupation count
        else:
            merged_data[occupation_ai_classify]['count'] += 1
            occupation_counts[occupation_ai_classify] += 1

        for skill in item['Skills']:
            skill_found = False
            for existing_skill in merged_data[occupation_ai_classify]['skills']:
                if existing_skill['name'] == skill:
                    existing_skill['count'] += 1
                    skill_found = True
                    break
            if not skill_found:
                merged_data[occupation_ai_classify]['skills'].append({
                    'name': skill,
                    'count': 1
                })

# Sort skills based on the count
for occupation_ai_classify in merged_data.values():
    occupation_ai_classify['skills'] = sorted(occupation_ai_classify['skills'], key=lambda x: x['count'], reverse=True)

# Convert merged_data into a list of dictionaries
merged_data_list = list(merged_data.values())

# Save the merged data to a new JSON file
with open('merged_jobdictionary.json', 'w') as file:
    json.dump(merged_data_list, file, ensure_ascii=False, indent=4)

# Print occupation counts
for occupation, count in occupation_counts.items():
    print(f"{occupation}: {count}")

print("Done")
