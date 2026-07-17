import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

STORES = [
    {
        "name": "Walmart",
        "url": "https://www.walmart.com/search?q=pokemon+cards"
    },
    {
        "name": "Target",
        "url": "https://www.target.com/s?searchTerm=pokemon+cards"
    }
]

KEYWORDS = [
    "pokemon",
    "elite trainer box",
    "booster bundle",
    "booster box",
    "premium collection",
    "pokemon center"
]

IGNORE = [
    "case",
    "sleeves",
    "binder",
    "protector"
]


def alert(message):
    requests.post(
        WEBHOOK,
        json={"content": message}
    )


def check_store(store):

    try:
        r = requests.get(
            store["url"],
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=15
        )

        soup = BeautifulSoup(r.text, "lxml")
        text = soup.get_text(" ").lower()

        found = []

        for word in KEYWORDS:
            if word in text:
                found.append(word)

        for word in IGNORE:
            if word in text:
                return

        if found:
            alert(
f"""
🚨 POKÉMON DROP ALERT 🚨

Store:
{store['name']}

Possible MSRP product activity detected!

Keywords:
{', '.join(found)}

Link:
{store['url']}

Time:
{datetime.now()}
"""
            )

    except Exception as e:
        print(e)


for store in STORES:
    check_store(store)
