import requests
import json




def fetch_data(url):
    headers = {"api-key": "your_api_key_here"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from {url}. Status code: {response.status_code}")

def process_jobs(jobs_data):
    jobs = []
    occurence = []
    for job_data in jobs_data["typeahead"]:
        job_title = job_data["value"]
        occurence_title = job_data["occurrences"]
        if job_data["type"] == 'skill':
            jobs.append((job_title, occurence_title))
    return jobs

def main():
    jobs_url = f"https://jobsearch.api.jobtechdev.se/complete?occupation-field=apaJ_2ja_LuF&qfields=skill&limit=50"
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