import json

with open('job_dictionary.json', 'r') as file:
    data = [json.loads(line) for line in file]

# Merge dictionaries with the same occupation-type and AI occupation classify
merged_data = {}
for item in data:
    occupation_type = item['Occupation-type']
    ai_occupations = item['Occupation-AI_classify']

    if occupation_type not in merged_data:
        merged_data[occupation_type] = {
            'label': occupation_type,
            'skills': [],
            'ai_occupations': []
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

    for ai_occupation in ai_occupations:
        ai_occ_found = False
        for existing_ai_occ in merged_data[occupation_type]['ai_occupations']:
            if existing_ai_occ['name'] == ai_occupation:
                existing_ai_occ['count'] += 1
                skill_found = False
                for existing_skill in existing_ai_occ['skills']:
                    if existing_skill['name'] == skill:
                        existing_skill['count'] += 1
                        skill_found = True
                        break
                if not skill_found:
                    existing_ai_occ['skills'].append({
                        'name': skill,
                        'count': 1
                    })
                ai_occ_found = True
                break

        if not ai_occ_found:
            merged_data[occupation_type]['ai_occupations'].append({
                'name': ai_occupation,
                'count': 1,
                'skills': [{
                    'name': skill,
                    'count': 1
                }]
            })

# Sort skills based on the count
for occupation_type in merged_data.values():
    occupation_type['skills'] = sorted(occupation_type['skills'], key=lambda x: x['count'], reverse=True)
    for ai_occupation in occupation_type['ai_occupations']:
        ai_occupation['skills'] = sorted(ai_occupation['skills'], key=lambda x: x['count'], reverse=True)

# Save the merged data to a new JSON file
with open('merged_jobdictionary.json', 'w') as file:
    json.dump(list(merged_data.values()), file, ensure_ascii=False, indent=4)

print("Done")
