import json

# Load the JSON data from file
with open('data/updated_occupation_list.json', 'r+') as file:
    data = json.load(file)

    # Calculate the average value for each skill
    for job in data:
        skills = job['skills']
        total_count = job['count']
        filtered_skills = []
        for skill in skills:
            skill_count = skill['count']
            skill['average'] = skill_count / total_count
            if skill['average'] >= 0.1:  # only keep skills with average value >= 0.1
                filtered_skills.append(skill)
        job['skills'] = filtered_skills  # replace the original skills list with the filtered list

    # Move the file pointer to the beginning of the file
    file.seek(0)

    # Write the updated JSON data back to the file
    json.dump(data, file, indent=4)
    file.truncate()