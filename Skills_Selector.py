import json

def select_skills():
    with open("updated_occupation_list.json", "r", encoding="utf-8") as file1:
        data = json.load(file1)
    
    skills_select = []
    for job in data:
        skills_select.extend([skill['name'] for skill in job['skills']])

<<<<<<< HEAD
    return list(set(skills_select))
=======
    skills_select = []
    for job in data:
        skills_select.extend([skill['name'] for skill in job['skills']])

    exact_skills = list(set(skills_select))

    result = []
    for skill in exact_skills:
        result.append({"label": skill, "value": skill})

    return result
>>>>>>> ead35f40d1a91615e7d45f2ff271ee48bc0eaffb
