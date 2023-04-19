import requests
import json


jobs_url = "https://jobsearch.api.jobtechdev.se/search?occupation-field=apaJ_2ja_LuF&municipality=PVZL_BQT_XtL&region=&offset=0&limit=100"



def fetch_data(url):
    headers = {"api-key": "your_api_key_here"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from {url}. Status code: {response.status_code}")

def process_jobs(jobs_data):
    jobs = []
    for job_data in jobs_data["hits"]:
        job_title = job_data["headline"]
        jobs.append(job_title)
    return jobs

def main():
    try:
        jobs_data = fetch_data(jobs_url)

        jobs = process_jobs(jobs_data)

        print("Jobs:")
        for i, job in enumerate(jobs):
            print(f"{i + 1}. {job}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()