import grequests

from db.config import FOLDER


class GRequestsDownloader:
    def save_photo(self, slug, response):
        with open(f"{FOLDER}{slug}.png", "wb") as photo:
            photo.write(response.content)

    def get_and_save_photos(self, responses, cards):
        for response, card in zip(responses, cards):
            self.save_photo(card['slug'], response)

    def process_cards(self, cards):
        methods = (grequests.get(card['image']) for card in cards)
        response = grequests.map(methods)

        self.get_and_save_photos(response, cards)
