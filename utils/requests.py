import requests
import json
from settings import API


def get_aliases():
    aliases = json.loads(requests.get(
        f'{API.flask_host}/get/aliases/').content)
    return aliases
