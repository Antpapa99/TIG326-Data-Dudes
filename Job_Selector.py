import json

def jobs():
    with open("desired_skills.json", "r", encoding="utf-8") as file:
        job_data = json.load(file)

    jobs_select = [{"title": occupation, "skills": skills} for occupation, skills in job_data.items()]

    return jobs_select

