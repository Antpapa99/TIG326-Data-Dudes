import json
import re

# Load the skills whitelist from the JSON file
with open('Skills.json') as file1:
    skills_whitelist = json.load(file1)

with open('Stack_Overflow_Skills.json') as file2:
    dict2 = json.load(file2)

# Combine the skills from both JSON files
combined_skills = set(skills_whitelist["label"] + dict2["label"])

# Create a new dictionary with the combined skills
skills_combined = {
    "label": list(combined_skills),
    "value": list(combined_skills)
}

print(skills_combined)

with open('skills_combined_test.json', 'w') as f:
    json.dump(skills_combined, f, indent=4)

# Define a function to check if a given skill is in the whitelist
import re

def is_valid_skill(skill):
    # Check if the skill is in the list
    if skill in skills_combined["label"]:
        return True

    # Check if the skill has an abbreviation within parentheses
    abbreviation_match = re.search(r'\(([^)]+)\)', skill)
    if abbreviation_match:
        abbreviation = abbreviation_match.group(1)
        # Remove abbreviation from skill name
        skill_without_abbreviation = re.sub(r'\s*\([^)]+\)', '', skill).strip()

        # Check if the skill without abbreviation or the abbreviation itself is in the list
        if skill_without_abbreviation in skills_combined["label"] or abbreviation in skills_combined["label"]:
            return True

    # Check if the skill starts with any valid skill in the list
    for valid_skill in skills_combined["label"]:
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

