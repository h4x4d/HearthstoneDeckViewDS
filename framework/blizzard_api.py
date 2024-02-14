import asyncio

import requests


class BlizzardAPI:
    def __init__(self,
                 client_id,
                 client_secret,
                 locale="en_US",
                 url="https://us.api.blizzard.com/hearthstone",
                 proxies=None
                 ):
        if proxies is None:
            proxies = {}

        self.session = requests.Session()
        self.session.proxies = proxies

        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.convert_access_token()
        self.locale = locale
        self.url = url

    def convert_access_token(self):
        url = "https://oauth.battle.net/token"

        payload = {"grant_type": "client_credentials"}
        auth = (self.client_id, self.client_secret)
        response = self.session.post(url, data=payload, auth=auth)
        return response.json()["access_token"]

    async def get(self, *args, **kwargs):
        response = None
        retries = 0

        while not response:
            response = self.session.get(*args, **kwargs)
            if not response:
                retries += 1
                if retries == 2:
                    return response
                await asyncio.sleep(5)

        return response

    async def get_from_code(self, deck_code):
        params = {
            "locale": self.locale,
            "code": deck_code,
            "access_token": self.access_token,
        }
        response = await self.get(self.url + "/deck", params=params)
        if response.status_code >= 500:
            response = await self.get(self.url + "/deck", params=params)

        json = response.json()

        return json

    async def get_card_from_id(self, card_id):
        params = {
            "locale": self.locale,
            "access_token": self.access_token,
        }
        response = await self.get(self.url + f"/cards/{card_id}",
                                  params=params)
        json = response.json()

        return json
