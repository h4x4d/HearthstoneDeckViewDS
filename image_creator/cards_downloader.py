import os
import shutil

from db.config import FOLDER
from framework import GRequestsDownloader
from threader import to_thread


@to_thread
def download_cards(cards):
    if os.path.exists(FOLDER):
        shutil.rmtree(FOLDER)
    os.mkdir(FOLDER)

    cards_api = GRequestsDownloader()
    cards_api.process_cards(cards)
