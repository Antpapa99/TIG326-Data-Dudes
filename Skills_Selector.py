import json
def select_skills():
    with open("skills_combined.json", "r", encoding="utf-8") as file1:
        data = json.load(file1)

        skills_select = [{"label": label, "value": value} for label, value in zip(data["label"], data["value"])]

        return skills_select
