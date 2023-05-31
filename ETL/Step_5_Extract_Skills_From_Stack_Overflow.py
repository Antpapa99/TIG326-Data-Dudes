import pandas as pd
import json

data = pd.read_csv(r"Here you put in the path where you put the stackoverflow latest survey")

#Ideally we would have both the main jobtech dataset and the stackoverflow dataset in the git repo but sadly github can't handle too large files

# List of columns you want to get unique values from
columns = ["DatabaseHaveWorkedWith", "LanguageHaveWorkedWith", "PlatformHaveWorkedWith", "WebframeHaveWorkedWith", "MiscTechHaveWorkedWith", "ToolsTechHaveWorkedWith", "NEWCollabToolsHaveWorkedWith", "VersionControlSystem"]

unique_values = set()

# Iterate through the columns and get unique values
for column in columns:
    # Split the column values by the delimiter
    split_values = data[column].str.split(';')

    # Flatten the list of lists
    flat_list = [item for sublist in split_values.dropna() for item in sublist]

    # Get unique values and update the set
    unique_values.update(flat_list)

print(unique_values)
#same thing we did in the previous skills whitelist
for elements in unique_values:
    output = {"label": [elements.lower() for elements in unique_values],
              "value": [elements.lower() for elements in unique_values]}

with open ("Stack_Overflow_Skills.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(output) + "\n")