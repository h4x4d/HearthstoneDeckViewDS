from db.constants import COST_OF_CARDS
from threader import to_thread


@to_thread
def get_cost_of_deck(cards):
    cost = 0

    for card in cards:
        cost += COST_OF_CARDS[card["rarityId"]]

    return cost
