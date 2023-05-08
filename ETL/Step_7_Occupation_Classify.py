import json

# Load the JSON data
with open('updated_occupation_list.json', 'r') as file:
    data = json.load(file)

# Print ai_occupations for occupations that don't match the label
mismatched_occupations = []
for occupation in data:
    label = occupation['label']
    ai_occupations = occupation['ai_occupations']
    for ai_occupation in ai_occupations:
        if ai_occupation['name'] != label:
            mismatched_occupations.append(ai_occupation)

# Merge dictionaries with the same name and combine skills and counts
merged_dict = {}
for dictionary in mismatched_occupations:
    name = dictionary['name']
    count = dictionary['count']
    skills = dictionary['skills']

    if count > 30:
        if name not in merged_dict:
            merged_dict[name] = {'name': name, 'count': count, 'skills': skills}
        else:
            merged_skills = merged_dict[name]['skills']
            for skill in skills:
                skill_name = skill['name']
                skill_count = skill['count']
                skill_exists = False
                for merged_skill in merged_skills:
                    if merged_skill['name'] == skill_name:
                        merged_skill['count'] += skill_count
                        skill_exists = True
                        break
                if not skill_exists:
                    merged_skills.append({'name': skill_name, 'count': skill_count})

# Convert the merged dictionary values to a list
merged_list = list(merged_dict.values())

# Sort the merged list by count in descending order
sorted_list = sorted(merged_list, key=lambda x: x['count'], reverse=True)

# Write the sorted occupation names and their skills to a text file
with open("mismatched_jobs.txt", "w") as file:
    for item in sorted_list:
        file.write(f"Name: {item['name']}\n")
        file.write("Skills:\n")
        for skill in item['skills']:
            file.write(f"- {skill['name']}, Count: {skill['count']}\n")
        file.write("\n")
