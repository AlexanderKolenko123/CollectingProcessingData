import requests
import json
#Task 1
url = 'https://api.github.com'
user ='AlexanderKolenko123'

res = requests.get(f'{url}/users/{user}/repos')
print(res.status_code)
print(res)

all_reps = []
for repos in res.json():
    all_reps.append(repos['name'])

    with open('Task_1.json', 'w') as f:
        to_json = json.dump(all_reps, f)

#Task 2

endpoint = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
api_key = "gZkkDU0fvcsLSzQYuLh2z9pjGQbIksAaMgccSZbH"
query_params = {"api_key": api_key, "earth_date": "2020-10-21"}
response = requests.get(endpoint, params=query_params)
print(response)
photos = response.json()["photos"]
print(f"Found {len(photos)} photos")

with open('Task_2.json', 'w') as f:
       to_json = json.dump(photos, f)