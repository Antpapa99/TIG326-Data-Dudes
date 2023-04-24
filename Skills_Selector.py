import json
def select_skills():
    with open("Skills.json", "r", encoding="utf-8") as file:
        data = json.load(file)

        skills_select = [{"label": label, "value": value} for label, value in zip(data["label"], data["value"])]

        return skills_select
