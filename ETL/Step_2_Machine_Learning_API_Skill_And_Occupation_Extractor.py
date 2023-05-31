import requests
import json
from concurrent.futures import ThreadPoolExecutor
import time

# Our enrichtextdocuments api url
url = "https://jobad-enrichments-api.jobtechdev.se/enrichtextdocuments"

#a timer to see how long it takes for the script to go through al job postings
start_time = time.time()

#open file where your json data is located in
with open (r'where you put your filtered data json file', 'r', encoding="utf-8") as f:
    data = json.load(f)

#This is code to store in various data from the datasets
Job_Class = []
occupation_list = []

#Here's the script it self sending requests to api to read through the data
def send_request(i):
    sample = data[i]
#the different parameters that we feed into the data so 
#the one above scans potential  occupations through feeding it job titles 
#and the below scans potential skills through feeding it both the title and the job description
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
    #Code for retries in case something goes wrong between communication of this script and the API
    max_retries = 3
    retries = 0
    #appends all the ocucpations
    occupation_list.append(data[i]["occupation"]["label"])

    enriched_candidates_occupation = None
    enriched_candidates_skills = None
    #Here's just the script telling what to do if the communication goes wrong
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

#This is just a function that tells the script to send 100 requests at a time as well specifying how many job postings we should feed it
with ThreadPoolExecutor(max_workers=100) as executor:
    indices = range(0, 17000)
    Job_Class = list(executor.map(send_request, indices))


#various important varibles to make the whole script actually work and store the data in a way that we desire it to
Keywords = []
loop = 0
dict_list = []


Dict_List = []
loop = 0
#A loop that clears the data and stores all the valuable information in this case being skills and occupations
while loop < len(Job_Class):
    Ai_Occupation = set()
    Skills = set()
    #Här kan ni configuera prediction värde
    #for i in Job_Class[loop]["Occupation-type"]:
        #Ai_Occupation.add(i["concept_label"].lower())
    for i in Job_Class[loop]["Skills"]:
        if i["prediction"] > 0.3: #you can configure the prediction values to your liking
            Skills.add(i["concept_label"].lower())
    for i in Job_Class[loop]["Occupation-AI_classify"]:
        if i["prediction"] > 0.05: #you can configure the prediction values to your liking, note on occupations it's recommended to have the prediction value a bit lower 
                                    #because the higher it is the lessl ikely it will actually pick up on job roles
            Ai_Occupation.add(i["concept_label"].lower())
    
    Skills = list(Skills)
    Ai_Occupation = list(Ai_Occupation)
    #This here is the json file that will be written as an output as a result from this script 
    output = {"Job Title": Job_Class[loop]["Job Title"].lower(),
                "Occupation-type":  Job_Class[loop]["Occupation-type"].lower(),
                "Occupation-AI_classify":  Ai_Occupation,
                    "Skills": Skills
                }
    Dict_List.append(output)
    loop += 1


#Basically this code below here just makes sure there are no job postings that are duplicates
Unique_Dict_List = []

for i in range(len(Dict_List)):
    if Dict_List[i] not in Dict_List[i + 1:]:
        Unique_Dict_List.append(Dict_List[i])

#This here just writes a new json file with the transformed data
with open("Job_Dictionary.json", "w", encoding="utf-8") as file:
    for i in Unique_Dict_List:
        file.write(json.dumps(i) + "\n")

for i in Unique_Dict_List:
    print(i)

#end of timer
end_time = time.time()  # Record the end time
elapsed_time = end_time - start_time  # Calculate the elapsed time

print(f"Elapsed time: {elapsed_time:.2f} seconds")

