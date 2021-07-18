# a script to migrate from notion-srs (https://github.com/m-danya/notion-srs-cli)
import csv
import json
from pathlib import Path
from datetime import date, datetime, timedelta

SRS_LEVEL_TO_DAYS = {
    1: 0,
    2: 1,
    3: 3,
    4: 8,
    5: 19,
    6: 44,
    7: 100,
    8: 226,
    9: 510,
    10: 1149,
    11: 2561,
    12: 5568,
    13: 11669,
    14: 23422,
    15: 44954
}

input_file = Path(__file__).parent / 'data.csv'
output_file = Path(__file__).parent / 'cards.json'

data = []

with open(input_file, encoding='utf-8-sig') as f:
    csv_reader = csv.DictReader(f)
    for c in csv_reader:
        #print('c =', c)
        try:
            date_wrong = datetime.strptime(c['Date Wrong'], "%B %d, %Y").date()
            back = c['Перевод']
            if c['как читается'] != '':
                back += '\n' + c['как читается']
            card = {
                'front': c['Name'],
                'back': back,
                'level': int(c['Level']),
                'date_wrong': date_wrong,
                'date_next': date_wrong + timedelta(days=SRS_LEVEL_TO_DAYS[int(c['Level'])])
            }
            data.append(card)
        except Exception as e:
            print("Couldn't deal with card: ", c)

with open(output_file, 'w') as f:
    f.write(json.dumps(data, default=str))
