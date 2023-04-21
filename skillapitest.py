import requests
import json

url = "https://jobad-enrichments-api.jobtechdev.se/enrichtextdocuments"

with open (r'C:\Users\Anthony\Desktop\JSON_data\afiltered_data.json', 'r') as f:
    data = json.load(f)

Job_Skill_List = []

for i in range(10):
    sample = data[i]
    params = {
    "documents_input": [
        {
        "doc_id": data[i]["id"],
        "doc_headline": data[i]["headline"],
        "doc_text": data[i]["description"]["text"],
        }
        ]
    }
    response = requests.post(url, json=params)
    if response.status_code == 200:
        #print("Request successful")
        json_response = response.json()
        # Make sure to access the correct element of the list
        enriched_candidates = json_response[0]["enriched_candidates"]
        Job_Skill_List.append(enriched_candidates)
        #Jobs[job_title] = skills
        #print("Traits:", enriched_candidates["traits"])
        #print("Geos:", enriched_candidates["geos"])
        
    else:
        print("Request failed with status code:", response.status_code)
        print("Error message:", response.text)


new_lista = []
for x in Job_Skill_List:
  i = 0
  while i < (len(x["competencies"])):
    print(x["competencies"][i]["prediction"])
    print((x["competencies"][i]["concept_label"]))
    new_lista.append(x["competencies"][i]["concept_label"])
    i += 1

print(new_lista)

#for y in skills_list:
  #skills = y[0]
  #print(skills["concept_label"],skills["prediction"])
