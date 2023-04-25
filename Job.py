from collections import defaultdict
import json
# Sample input dictionaries
with open ("Job_Dictionary.json", "r", encoding="utf-8") as file:
    job_data = [json.loads(line) for line in file]



# Initialize an empty dictionary to store the occupations and their associated skills
occupation_skills = defaultdict(lambda: defaultdict(int))
occupation_counts = defaultdict(int)

# Iterate through each job data dictionary
for job in job_data:
    # Extract the occupations and skills
    occupations = job["Occupation-AI_classify"]
    skills = job["Skills"]

    # Count the occurrences of each skill for each occupation
    for occupation in occupations:
        occupation_counts[occupation] += 1
        for skill in skills:
            occupation_skills[occupation][skill] += 1

# Calculate the percentage of occurrence for each skill in each occupation
percentage_threshold = 0.9   
desired_skills = {}
for occupation, skills in occupation_skills.items():
    desired_skills[occupation] = [
        skill for skill, count in skills.items()
        if (count / occupation_counts[occupation]) >= percentage_threshold
    ]

# Print the final dictionary containing occupations and their desired skills
with open("desired_skills.json", "w", encoding="utf-8") as f:
    json.dump(desired_skills, f, indent=4)