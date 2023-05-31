import json

# Load the JSON data from file
with open('data/updated_occupation_list.json', 'r+') as file:
    data = json.load(file)

    filtered_jobs = []  # List to hold jobs

    for job in data:
        total_count = job['count']
        
        # Here you can decide how you want the job data for the webapp to look like you can configure which jobs will appear based on count or which skills will appear based on percentage
        if total_count >= 20:
            skills = job['skills']
            filtered_skills = []
            for skill in skills:
                skill_count = skill['count']
                skill['average'] = skill_count / total_count
                if skill['average'] >= 0.1:  # only keep skills with average value >= 0.1
                    filtered_skills.append(skill)
            job['skills'] = filtered_skills  # replace the original skills list with the filtered list
            filtered_jobs.append(job)  # add the job to the filtered jobs list

    # Move the file pointer to the beginning of the file
    file.seek(0)

    # Write the updated JSON data back to the file, this basically just updates the updated_occupation_list.json
    json.dump(filtered_jobs, file, indent=4)
    file.truncate()
