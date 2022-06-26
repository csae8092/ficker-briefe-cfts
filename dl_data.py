import os
import json
import requests
import time
from tqdm import tqdm

DATA_DIR = './data/editions'
APP_BASE = "https://edition.ficker-gesamtbriefwechsel.net/api/letter/"
HEADERS = {'Accept': 'application/json'}
os.makedirs(DATA_DIR, exist_ok=True)

r = requests.request("GET", f"{APP_BASE}byYear", headers=HEADERS)
data = r.json()
with open('./data/itmes.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, ensure_ascii=False))

year_letter_list = data['yearLetterList']

letters = []
for year in year_letter_list:
    for x in year['letterList']:
        letters.append([year['year'], x['id']])

for x in tqdm(letters, total=len(letters)):
    r = requests.request(
        "GET", f"{APP_BASE}{x[1]}", headers=HEADERS
    )
    data = r.json()
    with open(f'./data/editions/{x[0]}__{x[1]}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
    time.sleep(0.3)
