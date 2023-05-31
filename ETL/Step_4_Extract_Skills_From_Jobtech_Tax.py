import json
import csv

#Here we created our own json file from jobtechs site that listed all the skills related to Data och IT(hopefully this is the correct name of the category)
with open('Skills_whitelist.json', "r", encoding="utf-8") as f:
 data =  json.load(f)


Skills_list = []

#just a bunch of unpacking of the json file to get to the value we desire
for unpack in data["data"]["concepts"]:
 for more_unpack in unpack["narrower"]:
  for pack in more_unpack["related"]:
        Skills_list.append(pack["preferred_label"].strip(","))
#here's just so that we cutoff things like C#, programmeringsspråk
new_strings = []
for string in Skills_list:
    new_string = string.split(',')[0]
    new_strings.append(new_string)

#here's our a way for us to clean the skills data and make it so that the dash can read the skills
clean_duplicates = set(new_strings)
clean_duplicates = list(clean_duplicates)
skills = {"label": [i.lower() for i in clean_duplicates],
          "value": [i.lower() for i in clean_duplicates]}

#here's the skills.json
with open("Skills.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(skills))  
