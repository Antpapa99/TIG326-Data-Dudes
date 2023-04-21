import requests
import json

url = "https://jobad-enrichments-api.jobtechdev.se/enrichtextdocuments"

with open('filtered_data.json', 'r') as f:
    data = json.load(f)

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
        print("Request successful")
        json_response = response.json()
        # Make sure to access the correct element of the list
        enriched_candidates = json_response[0]["enriched_candidates"]
        print("Occupations:", enriched_candidates["occupations"])
        print("Competencies:", enriched_candidates["competencies"])
        print("Traits:", enriched_candidates["traits"])
        print("Geos:", enriched_candidates["geos"])
    else:
        print("Request failed with status code:", response.status_code)
        print("Error message:", response.text)