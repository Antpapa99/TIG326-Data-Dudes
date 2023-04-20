import json

# read in the dataset
with open('filtered_data_jobs.json') as f:
    job_ads = json.load(f)

#
# loop through each job ad
lista = []
dictcount = {}
for job_ad in job_ads:
    description = job_ad["nice_to_have"]["skills"]
    for i in description:
        lista.append(i["label"])

for job_ad in job_ads:
    description = job_ad["must_have"]["skills"]
    for i in description:
        lista.append(i["label"])

lista = set(lista)
print(lista)
#with open("skills.txt", "w", encoding="utf-8") as skills:
    #for item in lista:
        #skills.write(item + "\n")