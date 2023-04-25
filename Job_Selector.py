import json

def jobs():
    with open("occupation_list.json", "r", encoding="utf-8") as file:
        job_data = json.load(file)

    return tuple(job_data)
