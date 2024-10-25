import grequests
import requests

from db.config import FOLDER
from framework.wiki_downloader import download_from_wiki


class GRequestsDownloader:
    def save_photo(self, slug, response, name, save_url):
        with open(f"{FOLDER}{slug}.png", "wb") as photo:
            if response is not None:
                photo.write(response.content)
            else:
                try:
                    response = requests.get(save_url)
                    photo.write(response.content)
                except:
                    download_from_wiki(slug, name)

    def get_and_save_photos(self, responses, cards):
        for response, card in zip(responses, cards):
            self.save_photo(card["slug"], response, card["name"], card["image"])

    def process_cards(self, cards):
        methods = (grequests.get(card["image"]) for card in cards)
        response = grequests.map(methods)

        self.get_and_save_photos(response, cards)
