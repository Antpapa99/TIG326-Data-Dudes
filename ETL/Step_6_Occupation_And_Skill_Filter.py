import json

# Load the skills whitelist from the JSON file
with open('Skills.json') as file1:
    skills_whitelist = json.load(file1)

with open('Stack_Overflow_Skills.json') as file2:
    dict2 = json.load(file2)

skills_whitelist.update(dict2)

# Define a function to check if a given skill is in the whitelist
def is_valid_skill(skill):
    if skill in skills_whitelist["label"]:
        return True

    for valid_skill in skills_whitelist["label"]:
        if skill.startswith(valid_skill):
            return True

    return False

# Load the occupation list from the JSON file
with open('merged_jobdictionary.json') as f:
    occupation_list = json.load(f)

filtered_skills_counts = {}

for occupation in occupation_list:
    valid_skills = []

    for skill in occupation['skills']:
        if is_valid_skill(skill['name']):
            valid_skills.append(skill)
        else:
            if skill['name'] not in filtered_skills_counts:
                filtered_skills_counts[skill['name']] = {'name': skill['name'], 'count': skill['count']}
            else:
                filtered_skills_counts[skill['name']]['count'] += skill['count']
    
    occupation['skills'] = valid_skills

with open('updated_occupation_list.json', 'w') as f:
    json.dump(occupation_list, f, indent=4)

filtered_skills_sorted = sorted(filtered_skills_counts.values(), key=lambda x: x['count'], reverse=True)

with open('filtered_skills.json', 'w') as f:
    json.dump(list(filtered_skills_sorted), f, indent=4)

