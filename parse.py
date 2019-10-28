import os

from bs4 import BeautifulSoup
from glob import glob
import json


def parse_card(card_path, card_uuid):
    """

    :param card_path:
    :return:
    """
    with open(card_path, 'r') as in_str:
        content = in_str.read()
        soup = BeautifulSoup(content, 'html.parser')

    title = soup.select_one('.flex-grow-1')

    edition = soup.select_one('.flex-grow-1 span').text
    title = title.text.replace(edition, '').strip()

    info = {}
    for child_info_wrapper in soup.select_one('dl').children:

        if child_info_wrapper.name == 'dt':
            info_class = child_info_wrapper.text.lower()

        if child_info_wrapper.name == 'dd':

            if info_class == 'rarity':
                text = child_info_wrapper.select_one('span').attrs['title'].lower().strip()
                info[info_class] = text
            else:
                info[info_class] = child_info_wrapper.text

    rules_text = soup.select_one('.d-none .d-md-block p').text.lower().strip()

    card_info = {
        'card_uuid': card_uuid,
        'title': title,
        'edition': edition,
        'info': info,
        'rules': rules_text}

    return card_info


if __name__ == '__main__':

    card_paths = glob('/development/datasets/magic-gathering/cards/*')
    card_infos = []
    i = 0
    j = 0

    for card_path in card_paths:

        try:
            card_uuid = card_path.split('/')[-1]
            out_path = '/development/datasets/magic-gathering/cards_infos/{}.json'.format(card_uuid)
            if os.path.exists(out_path):
                continue

            card_info = parse_card(card_path, card_uuid)
            with open(out_path, 'w') as out_str:
                out_str.write(json.dumps(card_info))

            i += 1

        except Exception as e:
            j += 1

        print(i, j, len(card_paths))
