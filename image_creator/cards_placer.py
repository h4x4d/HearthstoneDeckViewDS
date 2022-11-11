from PIL import Image, ImageDraw

from db.config import FOLDER
from db.font import FONT

from .place_runes import place_runes


def place_cards(counters, mana, class_id, deck_cost, response):
    if len(counters) <= 18:
        size = 500
        water = Image.open('x2.png').resize((214, 121))
    elif 19 <= len(counters) <= 32:
        size = 375
        water = Image.open('x2.png').resize((141, 80))
    else:
        size = 300
        water = Image.open('x2.png').resize((124, 70))

    sizes = (size, int(size * 1.354))
    row, col = 0, 0

    counters = [[i, counters[i]] for i in counters]
    counters = sorted(counters, key=lambda card_: mana[card_[0]])
    counters = {i[0]: i[1] for i in counters}

    temp = Image.open(f'backs/{class_id}.png')
    image = Image.new('RGBA', temp.size, (0, 0, 0, 0))
    image.paste(temp, (0, 0))

    for card in counters:
        im = Image.open(f"{FOLDER}{card}.png").convert("RGBA").resize(sizes)

        if counters[card] == 2:
            if size == 375:
                image.paste(water, (col + 117, row + 480), mask=water)
            elif size == 500:
                image.paste(water, (col + 143, row + 640), mask=water)
            else:
                image.paste(water, (col + 90, row + 380), mask=water)

        image.paste(im, (col, row), mask=im)

        col += sizes[0]
        if col > 2900:
            col = 0
            row += sizes[1] + 20

    draw = ImageDraw.ImageDraw(image)
    draw.text((170, 2205), str(deck_cost), (255, 255, 255), FONT)

    if class_id == 1:
        image = place_runes(image, response)

    return image
