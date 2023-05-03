import json

def read_job_directory(file_path):
    with open(file_path, 'r') as file:
        job_data = [json.loads(line) for line in file]

    return job_data

def skills_by_occupation_type(job_data):
    occupation_skills = {}

    for job in job_data:
        occupation_type = job["Occupation-type"]
        skills = job["Skills"]

        if occupation_type not in occupation_skills:
            occupation_skills[occupation_type] = set()

        occupation_skills[occupation_type].update(skills)

    return occupation_skills

def write_occupation_skills_to_json(occupation_skills, file_path):
    # Convert sets to lists before writing to JSON
    occupation_skills_lists = {k: list(v) for k, v in occupation_skills.items()}
    
    with open(file_path, "w") as file:
        json.dump(occupation_skills_lists, file, ensure_ascii=False, indent=4)

def main():
    job_data = read_job_directory("/Users/anto/Data_Dudes/TIG326-Data-Dudes/ETL/Job_Dictionary.json")
    occupation_skills = skills_by_occupation_type(job_data)
    write_occupation_skills_to_json(occupation_skills, "occupation_list.json")

if __name__ == "__main__":
    main()
