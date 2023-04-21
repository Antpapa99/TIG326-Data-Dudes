import requests
import json

url = "https://jobad-enrichments-api.jobtechdev.se/enrichtextdocuments"

with open (r'C:\Users\Anthony\Desktop\JSON_data\afiltered_data.json', 'r', encoding="UTF-8") as f:
    data = json.load(f)

Job_Class = []

for i in range(99):
    sample = data[i]
    params = {
    "documents_input": [
        {
        "doc_id": data[i]["id"],
        "doc_headline": data[i]["headline"],
        "doc_text": data[i]["description"]["text_formatted"],
        }
        ]
    }
    response = requests.post(url, json=params)
    if response.status_code == 200:
        #print("Request successful")
        json_response = response.json()
        # Make sure to access the correct element of the list
        enriched_candidates = json_response
        Job_Class.append(enriched_candidates)
        #Jobs[job_title] = skills
        #print("Traits:", enriched_candidates["traits"])
        #print("Geos:", enriched_candidates["geos"])
        
    else:
        print("Request failed with status code:", response.status_code)
        print("Error message:", response.text)


Keywords = []
loop = 0
dict_list = []
while loop < len(Job_Class):
    for i in Job_Class[loop]:
        occupations = set()
        skills = set()
        for data in i["enriched_candidates"]["occupations"]:
            if data["prediction"] > 0.8:
                occupations.add(data["concept_label"])
        for data in i["enriched_candidates"]["competencies"]:
            if data["prediction"] > 0.8:
                skills.add(data["concept_label"])

        occupations = list(occupations)   
        skills = list(skills)
        output = {"Job Title": i["doc_headline"],
                "Occupations": occupations,
                    "Skills": skills
                }
        dict_list.append(output)
        loop += 1

Unique_Dict_List = []

for i in range(len(dict_list)):
    if dict_list[i] not in dict_list[i + 1:]:
        Unique_Dict_List.append(dict_list[i])

for i, x in enumerate(Unique_Dict_List):
    print(i, x)

#for y in skills_list:
  #skills = y[0]
  #print(skills["concept_label"],skills["prediction"])
