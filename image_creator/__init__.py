from .card_counter import count_cards
from .cards_downloader import download_cards
from .cards_placer import place_cards
from .cost_getter import get_cost_of_deck
from .deck_retriever import retrieve_deck


async def create_picture(deck_code):
    response, deck_class, sideboard = await retrieve_deck(deck_code)
    if response == 0:
        return None

    await download_cards(response["cards"] + sideboard)
    counters, mana = await count_cards(response["cards"])

    cost = await get_cost_of_deck(response["cards"] + sideboard)

    image = await place_cards(counters, mana, deck_class, cost, response, sideboard)

    return image
