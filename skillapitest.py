import requests
import json

url = "https://jobad-enrichments-api.jobtechdev.se​/enrichtextdocuments"

with open('filtered_data.json', 'r') as f:
    data = json.load(f)


for i in range(10):
    sample = data[i]
    params = {
      "doc_id": data[i]["id"],
      "doc_headline": data[i]["headline"],
      "doc_text": data[i]["description"]["text"]
      
    }
    response = requests.request(url, params)
    print(response)