import json

# Load the post-whitelisted occupation list
with open('updated_occupation_list.json', 'r') as f:
    updated_occupation_list = json.load(f)

exact_skills = set()

for occupation in updated_occupation_list:
    for skill in occupation['skills']:
        exact_skills.add(skill['name'])

exact_skills_dict = {
    "label": list(exact_skills),
    "value": list(exact_skills)
}

with open('exact_skills.json', 'w') as f:
    json.dump(exact_skills_dict, f, indent=4)
