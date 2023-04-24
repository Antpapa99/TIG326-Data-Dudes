import json
def select_skills():
    with open("Skills.json", "r", encoding="utf-8") as file1, open("Stack_Overflow_Skills.json", "r", encoding="utf-8") as file2:
        data = json.load(file1)
        data2 = json.load(file2)
        data.update(data2)

        skills_select = [{"label": label, "value": value} for label, value in zip(data["label"], data["value"])]

        return skills_select
