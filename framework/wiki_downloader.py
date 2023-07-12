import requests

from db.config import FOLDER


def download_from_wiki(slug, name):
    name = "_".join(name.split())

    response = requests.get(f"https://hearthstone.fandom.com/wiki/{name}")

    r = response.text
    r = r[:r.index('width="270"')]
    r = r[r.rindex("img"):]
    url = r[r.index('src="') + 5:r.index("png") + 3]

    with open(f"{FOLDER}{slug}.png", "wb") as photo:
        photo.write(requests.get(url).content)
