import pprint

from db.config import CLIENT_ID, CLIENT_SECRET, PROXY
from framework import BlizzardAPI


async def retrieve_deck(deck_code):
    api = BlizzardAPI(CLIENT_ID, CLIENT_SECRET, proxies=PROXY)
    response = await api.get_from_code(deck_code)
    if "error" in response:
        print("error")
        return [0, 0, 0]

    duels_class = None
    sideboard = []

    pprint.pp(response)

    if "sideboardCards" in response:
        for side in response["sideboardCards"]:
            if side['sideboardCard']['id'] == 102983:
                pprint.pp(side)
                for i in range(len(response['cards'])):
                    if response['cards'][i]['id'] == 102983:
                        response['cards'][i]['manaCost'] = sum(i['manaCost'] for i in side["cardsInSideboard"])
                        response['zilliax'] = '-'.join(map(str, sorted(
                            [i['id'] for i in side["cardsInSideboard"] if i['isZilliaxFunctionalModule']])))
            sideboard += side["cardsInSideboard"]

    if response["cardCount"] == 30 and len(response["cards"]) < 30:
        for card_id in response["invalidCardIds"]:
            response["cards"].append(await api.get_card_from_id(card_id))

    for i in sideboard:
        i["slug"] += "-side"

    return response, response["class"]["id"], sideboard
