import json

# Load the skills whitelist from the JSON file
with open('Skills.json') as f:
    skills_whitelist = json.load(f)

# Define a function to check if a given skill is in the whitelist
def is_valid_skill(skill):
    # Check if the skill is in the whitelist
    if skill in skills_whitelist["label"]:
        return True
    
    # Check if the skill is an abbreviation or misspelling of a valid skill
    for valid_skill in skills_whitelist["label"]:
        if skill.startswith(valid_skill):
            return True
    
    # If the skill isn't valid or an abbreviation/misspelling, return False
    return False

# Load the occupation list from the JSON file
with open('occupation_list.json') as f:
    occupation_list = json.load(f)

# Loop through each occupation in the occupation list
for occupation in occupation_list:
    # Create a new list to hold the valid skills
    valid_skills = []
    # Loop through each skill in the occupation's skill list
    for skill in occupation['skills']:
        # Check if the skill is valid
        if is_valid_skill(skill):
            # If the skill is valid, add it to the list of valid skills
            valid_skills.append(skill)
    # Replace the occupation's skills with the list of valid skills
    occupation['skills'] = valid_skills

# Save the updated occupation list to a new JSON file
with open('updated_occupation_list.json', 'w') as f:
    json.dump(occupation_list, f, indent=4)

# Create empty lists to hold the labels and values of valid skills
valid_labels = []
valid_values = []

# Loop through each occupation in the occupation list
for occupation in occupation_list:
    # Loop through each skill in the occupation's skill list
    for skill in occupation['skills']:
        # Check if the skill is valid
        if is_valid_skill(skill):
            # If the skill is valid, add its label and value to the corresponding lists
            valid_labels.append(skill)

# Create a dictionary with the valid labels and values
valid_labels = set(valid_labels)
valid_labels = list(valid_labels)
valid_skills_dict = {"label": valid_labels, "value": valid_labels}

# Save the valid skills to a new JSON file
with open('valid_skills.json', 'w') as f:
    json.dump(valid_skills_dict, f, indent=4)