import requests
import json
from concurrent.futures import ThreadPoolExecutor
import time

url = "https://jobad-enrichments-api.jobtechdev.se/enrichtextdocuments"

start_time = time.time()

with open (r'C:\Users\Anthony\Desktop\JSON_data\afiltered_data.json', 'r', encoding="utf-8") as f:
    data = json.load(f)

Job_Class = []

print(data[1]["occupation"])

def send_request(i):
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
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            response = requests.post(url, json=params)
            if response.status_code == 200:
                json_response = response.json()
                enriched_candidates = json_response
                return enriched_candidates
            else:
                print(f"Request {i} failed with status code:", response.status_code)
                print("Error message:", response.text)
                retries += 1
                time.sleep(2)  # You can adjust the sleep duration based on your needs
        except requests.exceptions.RequestException as e:
            print(f"Request {i} encountered an exception: {e}")
            retries += 1
            time.sleep(2)  # You can adjust the sleep duration based on your needs
    print(f"Request {i} failed after {max_retries} retries")


with ThreadPoolExecutor(max_workers=100) as executor:
    indices = range(0, 1)
    Job_Class = list(executor.map(send_request, indices))

Keywords = []
loop = 0
dict_list = []
while loop < len(Job_Class):
    for i in Job_Class[loop]:
        occupations = set()
        skills = set()
        for data in i["enriched_candidates"]["occupations"]:
            if data["prediction"] > 0.9:
                occupations.add(data["concept_label"])
        for data in i["enriched_candidates"]["competencies"]:
            if data["prediction"] > 0.9:
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
with open("Job_Dictionary.txt", "w", encoding="utf-8") as file:
    for i in Unique_Dict_List:
        file.write(json.dumps(i) + "\n")

end_time = time.time()  # Record the end time
elapsed_time = end_time - start_time  # Calculate the elapsed time

print(f"Elapsed time: {elapsed_time:.2f} seconds")

