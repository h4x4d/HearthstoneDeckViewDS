from db.config import CLIENT_ID, CLIENT_SECRET
from framework import BlizzardAPI


async def retrieve_deck(deck_code):
    api = BlizzardAPI(CLIENT_ID, CLIENT_SECRET)
    response = await api.get_from_code(deck_code)
    if "error" in response:
        print("error")
        return [0, 0, 0]

    duels_class = None
    sideboard = []

    if "sideboardCards" in response:
        sideboard = response["sideboardCards"][0]["cardsInSideboard"]
        for i in sideboard:
            i["slug"] += "-side"

    if response["cardCount"] == 15 and len(response["cards"]) < 15:

        for card_id in response["invalidCardIds"]:
            resp_card = await api.get_card_from_id(card_id)
            response["cards"].append(await api.get_card_from_id(card_id))

        duels_class = resp_card["classId"]

    if duels_class:
        deck_class = int(str(response["class"]["id"]) + str(duels_class))
    else:
        deck_class = response["class"]["id"]

    return response, deck_class, sideboard
