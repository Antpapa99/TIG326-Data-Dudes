import json

def select_skills():
    with open("updated_occupation_list.json", "r", encoding="utf-8") as file1:
        data = json.load(file1)
    
    

    skills_select = []
    for job in data:
        skills_select.extend([skill['name'] for skill in job['skills']])

    exact_skills = list(set(skills_select))
    return exact_skills

# Call the function and print the result



