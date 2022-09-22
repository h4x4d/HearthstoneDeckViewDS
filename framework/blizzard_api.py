import time

import requests

from db.config import BATTLE_NET_TOKEN


class BlizzardAPI:
    def __init__(self, auth_token, locale="en_US", url="https://us.api.blizzard.com/hearthstone"):
        self.auth_token = auth_token
        self.access_token = self.convert_access_token()
        self.locale = locale
        self.url = url

        self.session = requests.Session()

    def convert_access_token(self):
        url = "https://us.battle.net/oauth/token"

        payload = 'grant_type=client_credentials'
        headers = {
            'Authorization': f'Basic {self.auth_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()["access_token"]

    def get(self, *args, **kwargs):
        response = None

        while not response:
            try:
                response = self.session.get(*args, **kwargs)
            except requests.exceptions.JSONDecodeError:
                time.sleep(5)

        return response

    def get_from_code(self, deck_code):
        params = {
            'locale': self.locale,
            'code': deck_code,
            'access_token': self.access_token,
        }
        response = self.get(self.url + "/deck", params=params)
        json = response.json()

        return json

    def get_card_from_id(self, card_id):
        params = {
            'locale': self.locale,
            'access_token': self.access_token,
        }
        response = self.get(self.url + f"/cards/{card_id}", params=params)
        json = response.json()

        return json
