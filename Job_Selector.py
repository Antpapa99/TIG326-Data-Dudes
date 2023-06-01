import json
#basically the controller for the jobs
def jobs():
    with open("data/updated_occupation_list.json", "r", encoding="utf-8") as file:
        job_data = json.load(file)

    return job_data


