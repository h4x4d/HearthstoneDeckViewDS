import numpy as np
from PIL import Image, ImageDraw

from db.config import FOLDER
from db.font import FONT
from threader import to_thread

from .place_runes import place_runes


@to_thread
def place_cards(counters, mana, class_id, deck_cost, response):
    if len(counters) <= 18:
        size = 500
        water = Image.open("x2.png").resize((214, 121))
    elif len(counters) <= 21:
        size = 428
        water = Image.open("x2.png").resize((180, 91))
    elif len(counters) <= 32:
        size = 375
        water = Image.open("x2.png").resize((141, 80))
    elif len(counters) <= 43:
        size = 300
        water = Image.open("x2.png").resize((124, 70))

    sizes = (size, int(size * 1.354))
    row, col = 0, 0

    counters = [[i, counters[i]] for i in counters]
    counters = sorted(counters, key=lambda card_: mana[card_[0]])
    counters = {i[0]: i[1] for i in counters}

    temp = Image.open(f"backs/{class_id}.png")
    image = Image.new("RGBA", temp.size, (0, 0, 0, 0))
    image.paste(temp, (0, 0))

    for card in counters:
        im = Image.open(f"{FOLDER}{card}.png").convert("RGBA")

        img = np.array(im)

        idx = np.where(img[:, :, 3] > 0)
        x0, y0, x1, y1 = idx[1].min(), idx[0].min(), idx[1].max(), idx[0].max()

        im = Image.fromarray(img[y0:y1 + 1, x0:x1 + 1, :])

        im = im.resize(sizes)

        if "-side" in card:
            pixels = im.load()

            for i in range(im.size[0]):
                for j in range(im.size[1]):
                    r, g, b, a = pixels[i, j]
                    im.putpixel((i, j), (min(255, r + 100),
                                         min(255, g + 40),
                                         min(255, b + 45), a))

        if counters[card] == 2:
            if size == 500:
                image.paste(water, (col + 150, row + 650), mask=water)
            elif size == 428:
                image.paste(water, (col + 140, row + 555), mask=water)
            elif size == 375:
                image.paste(water, (col + 125, row + 487), mask=water)
            elif size == 300:
                image.paste(water, (col + 97, row + 390), mask=water)

        image.paste(im, (col, row), mask=im)

        col += sizes[0]
        if col > 2900:
            col = 0
            row += sizes[1] + 40

    draw = ImageDraw.ImageDraw(image)
    draw.text((170, 2205), str(deck_cost), (255, 255, 255), FONT)

    if class_id == 1:
        image = place_runes(image, response)

    return image
