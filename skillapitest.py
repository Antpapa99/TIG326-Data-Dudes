import requests
import json

url = "https://jobad-enrichments-api.jobtechdev.se/enrichtextdocuments"

with open('/Users/anto/JSON_DATA/filtered_data_IT_jobs.json', 'r') as f:
    data = json.load(f)

Jobs = {}

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
        Occupation = (enriched_candidates["occupations"])
        #print(Occupation)
        Skills = (enriched_candidates["competencies"])
        #Jobs[job_title] = skills
        #print("Traits:", enriched_candidates["traits"])
        #print("Geos:", enriched_candidates["geos"])
    else:
        print("Request failed with status code:", response.status_code)
        print("Error message:", response.text)

job_dict = {}
for x in Occupation:
  print(x["concept_label"])

for y in Skills:
  print(y["concept_label"])

