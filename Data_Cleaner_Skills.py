import json
import pandas
with open('Skills_whitelist.json', "r", encoding="utf-8") as f:
 data =  json.load(f)


Skills_list = []

for unpack in data["data"]["concepts"]:
 for more_unpack in unpack["narrower"]:
  for pack in more_unpack["related"]:
        Skills_list.append(pack["preferred_label"].strip(","))

new_strings = []
for string in Skills_list:
    new_string = string.split(',')[0]
    new_strings.append(new_string)

clean_duplicates = set(new_strings)
clean_duplicates = list(clean_duplicates)

print(new_strings)
with open("Skills.csv", "w", encoding="utf-8") as file:
  for i in clean_duplicates:
    file.write(i + "\n")  
