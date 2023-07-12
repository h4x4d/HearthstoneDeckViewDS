from threader import to_thread


@to_thread
def count_cards(cards):
    counters = {}
    mana = {}
    for card in cards:
        if card["slug"] in counters:
            counters[card["slug"]] += 1
        else:
            counters[card["slug"]] = 1
            mana[card["slug"]] = card["manaCost"]

    return counters, mana
