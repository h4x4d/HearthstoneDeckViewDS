import numpy as np
from PIL import Image, ImageDraw

from db.config import FOLDER
from db.font import FONT

from .place_runes import place_runes


async def place_cards(counters, mana, class_id, deck_cost, response, sideboard):
    default_water = Image.open("labels/x2.png")

    if len(counters) + len(sideboard) <= 18:
        size = 500
        water = default_water.resize((214, 121))
    elif len(counters) + len(sideboard) <= 21:
        size = 428
        water = default_water.resize((180, 91))
    elif len(counters) + len(sideboard) <= 32:
        size = 375
        water = default_water.resize((141, 80))
    else:
        size = 300
        water = default_water.resize((124, 70))

    water_size = water.size

    sizes = (size, int(size * 1.35))
    row, col = 0, 0

    counters = [[i, counters[i]] for i in counters]
    counters = sorted(counters, key=lambda card_: mana[card_[0]])
    counters = {i[0]: i[1] for i in counters}

    temp = Image.open(f"backs/{class_id}.png")
    image = Image.new("RGBA", temp.size, (0, 0, 0, 0))
    image.paste(temp, (0, 0))
    stack = list(counters.keys())

    while len(stack) > 0:
        card = stack.pop(0)

        im = Image.open(f"{FOLDER}{card}.png").convert("RGBA")

        if card == '102983-zilliax-deluxe-000':
            try:
                im = Image.open(f"zilliax/{response['zilliax']}.png").convert("RGBA")
            except Exception as e:
                print(e)
                im = Image.open(f"{FOLDER}{card}.png").convert("RGBA")

        img = np.array(im)

        idx = np.where(img[:, :, 3] > 0)
        x0, y0, x1, y1 = idx[1].min(), idx[0].min(), idx[1].max(), idx[0].max()

        im = Image.fromarray(img[y0:y1 + 1, x0:x1 + 1, :])
        x = size
        y = round((im.size[1] / im.size[0]) * x)
        # y = sizes[1]
        if y > sizes[1]:
            y = sizes[1]
            x = round((im.size[0] / im.size[1]) * y)

        im = im.resize((x, y))

        if "-side" in card:
            pixels = im.load()

            for i in range(im.size[0]):
                for j in range(im.size[1]):
                    r, g, b, a = pixels[i, j]
                    im.putpixel((i, j), (min(255, r + 100),
                                         min(255, g + 50),
                                         min(255, b + 50), a))

        if card in counters and counters[card] >= 2:
            if counters[card] > 2:
                water = Image.open(f'labels/x{min(counters[card], 9)}.png').resize(water_size)

            if size == 500:
                image.paste(water, (col + 150, row + 650), mask=water)
            elif size == 428:
                image.paste(water, (col + 126, row + 555), mask=water)
            elif size == 375:
                image.paste(water, (col + 125, row + 487), mask=water)
            elif size == 300:
                image.paste(water, (col + 97, row + 390), mask=water)

            if counters[card] > 2:
                water = default_water.resize(water_size)

        image.paste(im, (col, row), mask=im)
        if "sideboardCards" in response:
            for i in response["sideboardCards"]:
                if i['sideboardCard']['slug'] == card:
                    stack = [j['slug'] for j in sorted(i['cardsInSideboard'], key=lambda c_: c_['manaCost']) if
                             not j['isZilliaxCosmeticModule']] + stack

        col += sizes[0]
        if col > 2900:
            col = 0
            row += sizes[1] + 40

    draw = ImageDraw.ImageDraw(image)
    draw.text((170, 2205), str(deck_cost), (255, 255, 255), FONT)

    if class_id == 1:
        image = place_runes(image, response)

    return image
