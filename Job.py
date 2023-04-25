from collections import defaultdict
import json

# Load sample input dictionaries
with open("Job_Dictionary.json", "r", encoding="utf-8") as file:
    job_data = [json.loads(line) for line in file]

# Initialize dictionaries to store the occupations, their associated skills, and counts
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
percentage_threshold = 0.7  # Change this value to set the threshold
desired_skills = {}
for occupation, skills in occupation_skills.items():
    desired_skills[occupation] = [
        skill for skill, count in skills.items()
        if (count / occupation_counts[occupation])  >= percentage_threshold
    ]

# Create a list of dictionaries with occupation title and desired skills
occupation_list = [{"title": occupation, "skills": skills} for occupation, skills in desired_skills.items()]

#Print the final dictionary containing occupations and their desired skills
with open("occupation_list.json", "w", encoding="utf-8") as f:
    json.dump(occupation_list, f, indent=4)