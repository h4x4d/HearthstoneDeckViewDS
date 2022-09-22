from .deck_retriever import retrieve_deck
from .cards_downloader import download_cards
from .card_counter import count_cards
from .cost_getter import get_cost_of_deck
from .cards_placer import place_cards


def create_picture(deck_code):
    response, deck_class = retrieve_deck(deck_code)

    download_cards(response['cards'])
    counters, mana = count_cards(response['cards'])

    cost = get_cost_of_deck(response)

    image = place_cards(counters, mana, deck_class, cost)

    return image
