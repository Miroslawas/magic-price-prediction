import json
import os
import urllib
from datetime import datetime
from time import sleep
from urllib.request import urlopen

with open('/development/datasets/magic-gathering/magic-the-gathering-cards/AllCards.json', 'r') as in_str:
    content = in_str.read()
    cards = json.loads(content)

i = 0
j = 0
result = {}
prev_timestamp = {}

for key, card in cards.items():

    if 'purchaseUrls' in  card:
        urls = card['purchaseUrls']
        if 'cardmarket' in urls:
            url = urls['cardmarket']

            card_id = card['uuid']
            f_path = '/development/datasets/magic-gathering/cards/{}'.format(card_id)
            if os.path.exists(f_path):
                i += 1
                result = 'Skipped'
                continue

            try:

                hdr = {
                    'Cookie': 'cookies_consent=accepted; PHPSESSID=5e2nfod6ina9vqoqrvmfhv8hd1; '
                              '__cfduid=d195459d06788541de5a5080fa98874281571383952',
                    'User-Agent': "Mozilla/5.0"}

                req = urllib.request.Request(url, headers=hdr)
                response = urllib.request.urlopen(req)
                result = response.read()
                j += 1

                with open(f_path, 'wb') as out_str:
                    out_str.write(result)
                    result = 'Success'

            except Exception as e:
                result = 'Fail'

    output_str = """
    {} \t {} \t Total scraped {}\{} \t Scraped during this batch {}""".format(datetime.now(), result, i, len(cards), j)

    print(output_str)
    i += 1
