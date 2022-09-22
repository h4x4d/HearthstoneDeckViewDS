import json
import os
import time

import requests
from PIL import Image, ImageDraw

import humanize
from constants import COST_OF_CARDS
from font import FONT

from get_code import get_code


def get_from_code(code, token, language="en-US"):
    params = {
        'locale': language,
        'code': code,
        'access_token': token,
    }
    session = requests.session()
    result = None
    while not result:
        try:
            result = session.get('https://us.api.blizzard.com/hearthstone/deck',
                                 params=params).json()
            code = get_code()
        except requests.exceptions.JSONDecodeError:
            time.sleep(5)

    second_class = None

    if result['cardCount'] == 15 and len(result['cards']) < 15:
        for card in result['invalidCardIds']:
            params = {
                'locale': language,
                'access_token': token,
            }
            time.sleep(3)
            print(card)
            c = None
            while not c:
                try:
                    c = session.get(f'https://us.api.blizzard.com/hearthstone/cards/{card}',
                                    params=params).json()
                except requests.exceptions.JSONDecodeError:
                    time.sleep(5)

            card = c

            second_class = card['classId']

            result['cards'].append(card)

    return result, second_class


def get_cards(json_result: dict, folder):
    if os.path.exists(folder):
        # shutil.rmtree(folder)
        pass
    else:
        os.mkdir(folder)
    counters = {}

    for card in json_result['cards']:
        if card['slug'] in counters:
            counters[card['slug']][0] += 1
        else:
            counters[card['slug']] = [1, card["manaCost"]]
        if not os.path.exists(f'{folder}/{card["slug"]}.png'):
            f = open(f'{folder}/{card["slug"]}.png', 'wb')
            f.write(requests.get(card['image']).content)
            f.close()

    c = []
    for key in counters.keys():
        c.append([key, *counters[key]])

    c.sort(key=lambda x: x[2])
    counters = [i[:2] for i in c]

    f = open(f'{folder}/hero.png', 'wb')
    f.write(requests.get(json_result['h ero']['image']).content)

    f = open(f'{folder}/power.png', 'wb')
    f.write(requests.get(json_result['heroPower']['image']).content)

    return counters


def place_cards(counters, folder, class_id, cost):
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
    temp = Image.open(f'backs/{class_id}.png')
    image = Image.new('RGBA', temp.size, (0, 0, 0, 0))
    image.paste(temp, (0, 0))
    for im_path in counters:
        im = Image.open(f'{folder}/{im_path[0]}.png').convert("RGBA").resize(
            sizes)
        if im_path[1] == 2:
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
    draw.text((170, 2205), str(cost), (255, 255, 255), FONT)

    return image


def get_cost_of_deck(response: dict):
    counter = 0
    for card in response['cards']:
        counter += COST_OF_CARDS[card["rarityId"]]

    return counter


def get_image_from_code(code, access, language="en-US", flag=False):
    result, second_class = get_from_code(code, access, language)
    if result['cardCount'] < 15:
        return 'Error'
    new_class = str(result["class"]["id"]) + str(second_class) if second_class else result['class']['id']
    print(new_class)
    counters, class_id = get_cards(result, 'deck'), new_class if not flag else 0
    return place_cards(counters, 'deck', class_id, get_cost_of_deck(result))


def get_local_deck_cost(result, user_id):
    if not os.path.exists(f'data/{user_id}.json'):
        return "Кажется, ваш профиль у меня не зарегистрирован. Используйте команду !коллекция"

    data = json.load(open(f"data/{user_id}.json", encoding="utf-8"))
    cost = 0
    not_enough = []

    for card in result["cards"]:
        if str(card["id"]) not in data or not data[str(card["id"])]:
            cost += COST_OF_CARDS[card["rarityId"]]
            if card["name"] in not_enough:
                not_enough[not_enough.index(card["name"])] = card['name'] + " x2"
            else:
                not_enough.append(card["name"])
        else:
            data[str(card["id"])] -= 1

    return [cost, '\n'.join(not_enough)]


def register_user(user_id, url):
    print(url)
    url = url[32:].split("/")

    api_url = f"https://hsreplay.net/api/v1/collection/?region={url[0]}&account_lo={url[1]}&type=CONSTRUCTED"

    r = requests.get(api_url).json()
    r = humanize.convert_to_human(r)

    r["user"] = url[1]
    r["region"] = url[0]

    json.dump(r, open(f"data/{user_id}.json", "w"))

    return r
