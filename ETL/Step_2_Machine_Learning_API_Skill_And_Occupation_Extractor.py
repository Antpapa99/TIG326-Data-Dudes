import requests
import json
from concurrent.futures import ThreadPoolExecutor
import time

#Vår AI API
url = "https://jobad-enrichments-api.jobtechdev.se/enrichtextdocuments"

start_time = time.time()

with open (r'/Users/anto/JSON_DATA/filtered_data_IT_jobs.json', 'r', encoding="utf-8") as f:
    data = json.load(f)

Job_Class = []
occupation_list = []

#funktionen som gör att programmet skicker en request till APIn med de olika json filerna som input
def send_request(i):
    sample = data[i]
    params = {
        "documents_input": [
            {
                "doc_id": data[i]["id"],
                "doc_headline": data[i]["headline"],
                "doc_text": data[i]["annonstext"], 
                "doc_text": data[i]["description"]["text"]
            }
            
        ]
    }
    max_retries = 3
    retries = 0
    occupation_list.append(data[i]["occupation"]["label"])
    while retries < max_retries:
        try:
            response = requests.post(url, json=params,timeout=15)
            if response.status_code == 200:
                json_response = response.json()
                enriched_candidates_skills = json_response[0]["enriched_candidates"]["competencies"]
                enriched_candidates_occupation = json_response[0]["enriched_candidates"]["occupations"]
                output = {"Job Title": data[i]["headline"],
                "Occupation-type":  (data[i]["occupation"]["label"]),
                "Occupation-AI_classify":  enriched_candidates_occupation,
                    "Skills": enriched_candidates_skills
                }
                return output
            else:
                print(f"Request {i} failed with status code:", response.status_code)
                print("Error message:", response.text)
                retries += 1
                time.sleep(10)  # You can adjust the sleep duration based on your needs
        except requests.exceptions.RequestException as e:
            print(f"Request {i} encountered an exception: {e}")
            retries += 1
            time.sleep(5)  # You can adjust the sleep duration based on your needs
    print(f"Request {i} failed after {max_retries} retries")

#Gör så att programmet skickar mer än ett request åt gången
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
        if i["prediction"] > 0.80:
            Skills.add(i["concept_label"].lower())
    Skills = list(Skills)
    Ai_Occupation = list(Ai_Occupation)
    output = {"Job Title": Job_Class[loop]["Job Title"].lower(),
                "Occupation-type":  Job_Class[loop]["Occupation-type"].lower(),
                #"Occupation-AI_classify":  Ai_Occupation,
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

