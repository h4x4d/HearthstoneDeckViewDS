from db.constants import COST_OF_CARDS


def get_cost_of_deck(response):
    cost = 0

    for card in response['cards']:
        cost += COST_OF_CARDS[card['rarityId']]

    return cost