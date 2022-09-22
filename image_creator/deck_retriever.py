from db.config import BATTLE_NET_TOKEN
from framework import BlizzardAPI


def retrieve_deck(deck_code):
    api = BlizzardAPI(BATTLE_NET_TOKEN)
    response = api.get_from_code(deck_code)

    duels_class = None

    if response['cardCount'] == 15 and len(response['cards']) < 15:

        for card_id in response['invalidCardIds']:
            resp_card = api.get_card_from_id(card_id)
            response['cards'].append(api.get_card_from_id(card_id))

        duels_class = resp_card['classId']

    if duels_class:
        deck_class = int(str(response['class']['id']) + str(duels_class))
    else:
        deck_class = response['class']['id']

    return response, deck_class
