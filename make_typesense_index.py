import glob
import json
import os

from acdh_cfts_pyutils import CFTS_COLLECTION
from django.utils.html import strip_tags
from tqdm import tqdm

files = sorted(glob.glob('./data/editions/*.json'))
schema_name = 'ficker-briefe'
APP_BASE = "https://edition.ficker-gesamtbriefwechsel.net/#/briefe/nach-jahren/"

records = []
for x in tqdm(files, total=len(files)):
    with open(x, encoding='utf-8') as f:
        doc = json.load(f)['letter']
    record = {
        'project': schema_name,
    }
    rec_id = os.path.split(x)[-1].split('__')[-1].replace('.json', '')
    record['rec_id'] = os.path.split(x)[-1]
    record['id'] = f"{schema_name}__{os.path.split(x)[-1]}"
    record['resolver'] = f"{APP_BASE}{rec_id}"
    record['title'] = doc['title']
    persons = []
    for hansi in ['senders', 'recipients', 'personList']:
        for p in doc[hansi]:
            persons.append(p['key'])
            persons.append(p['gnd'])
    persons = [x for x in persons if x]
    record['persons'] = persons

    places = []
    for p in doc['placeList']:
        places.append(p['key'])
        places.append(p['gnd'])
    places = [x for x in places if x]
    record['places'] = places
    record['year'] = int(record['rec_id'].split('__')[0])

    record['full_text'] = strip_tags(doc['html'])
    records.append(record)
make_index = CFTS_COLLECTION.documents.import_(records, {'action': 'upsert'})
print(make_index)
print('done with central indexing')
