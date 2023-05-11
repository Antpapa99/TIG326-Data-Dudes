import requests
import json
from concurrent.futures import ThreadPoolExecutor
import time

# Vår AI API
url = "https://jobad-enrichments-api.jobtechdev.se/enrichtextdocuments"

start_time = time.time()

with open (r'C:\Users\Anthony\Desktop\JSON_data\afiltered_data.json', 'r', encoding="utf-8") as f:
    data = json.load(f)

Job_Class = []
occupation_list = []

def send_request(i):
    sample = data[i]

    params_occupation = {
        "documents_input": [
            {
                "doc_id": data[i]["id"],
                "doc_headline": data[i]["headline"],
            }
        ]
    }

    params_skills = {
        "documents_input": [
            {
                "doc_id": data[i]["id"],
                "doc_headline": data[i]["headline"],
                "doc_text": data[i]["description"]["text"]
            }
        ]
    }

    max_retries = 3
    retries = 0
    occupation_list.append(data[i]["occupation"]["label"])

    enriched_candidates_occupation = None
    enriched_candidates_skills = None

    while retries < max_retries:
        try:
            response_occupation = requests.post(url, json=params_occupation, timeout=15)
            response_skills = requests.post(url, json=params_skills, timeout=15)

            if response_occupation.status_code == 200 and response_skills.status_code == 200:
                json_response_occupation = response_occupation.json()
                json_response_skills = response_skills.json()

                enriched_candidates_occupation = json_response_occupation[0]["enriched_candidates"]["occupations"]
                enriched_candidates_skills = json_response_skills[0]["enriched_candidates"]["competencies"]

                output = {
                    "Job Title": data[i]["headline"],
                    "Occupation-type":  (data[i]["occupation"]["label"]),
                    "Occupation-AI_classify":  enriched_candidates_occupation,
                    "Skills": enriched_candidates_skills
                }
                return output
            else:
                print(f"Request {i} failed with status code:", response_occupation.status_code, response_skills.status_code)
                print("Error message:", response_occupation.text, response_skills.text)
                retries += 1
                time.sleep(10)  # You can adjust the sleep duration based on your needs
        except requests.exceptions.RequestException as e:
            print(f"Request {i} encountered an exception: {e}")
            retries += 1
            time.sleep(5)  # You can adjust the sleep duration based on your needs
    print(f"Request {i} failed after {max_retries} retries")

with ThreadPoolExecutor(max_workers=100) as executor:
    indices = range(0, 17000)
    Job_Class = list(executor.map(send_request, indices))


Keywords = []
loop = 0
dict_list = []


Dict_List = []
loop = 0
#En loop som rensar Datan
while loop < len(Job_Class):
    Ai_Occupation = set()
    Skills = set()
    #Här kan ni configuera prediction värde
    #for i in Job_Class[loop]["Occupation-type"]:
        #Ai_Occupation.add(i["concept_label"].lower())
    for i in Job_Class[loop]["Skills"]:
        if i["prediction"] > 0.3:
            Skills.add(i["concept_label"].lower())
    for i in Job_Class[loop]["Occupation-AI_classify"]:
        if i["prediction"] > 0.05:
            Ai_Occupation.add(i["concept_label"].lower())
    
    Skills = list(Skills)
    Ai_Occupation = list(Ai_Occupation)
    output = {"Job Title": Job_Class[loop]["Job Title"].lower(),
                "Occupation-type":  Job_Class[loop]["Occupation-type"].lower(),
                "Occupation-AI_classify":  Ai_Occupation,
                    "Skills": Skills
                }
    Dict_List.append(output)
    loop += 1


Unique_Dict_List = []

for i in range(len(Dict_List)):
    if Dict_List[i] not in Dict_List[i + 1:]:
        Unique_Dict_List.append(Dict_List[i])
with open("Job_Dictionary.json", "w", encoding="utf-8") as file:
    for i in Unique_Dict_List:
        file.write(json.dumps(i) + "\n")

for i in Unique_Dict_List:
    print(i)

end_time = time.time()  # Record the end time
elapsed_time = end_time - start_time  # Calculate the elapsed time

print(f"Elapsed time: {elapsed_time:.2f} seconds")

