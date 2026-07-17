import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

SEEN_FILE = "seen_products.json"


stores = [
    {
        "name": "Pokémon Center",
        "url": "https://www.pokemoncenter.com/en-us/category/trading-card-game"
    },
    {
        "name": "Walmart",
        "url": "https://www.walmart.com/search?q=pokemon+cards"
    },
    {
        "name": "Target",
        "url": "https://www.target.com/s?searchTerm=pokemon+cards"
    },
    {
        "name": "Best Buy",
        "url": "https://www.bestbuy.com/site/searchpage.jsp?st=pokemon+cards"
    }
]


good_words = [
    "pokemon",
    "elite trainer box",
    "etb",
    "booster",
    "bundle",
    "collection",
    "premium",
    "box",
    "tin"
]


bad_words = [
    "single",
    "graded",
    "psa",
    "cgc",
    "binder",
    "sleeves",
    "case"
]


def send_alert(message):
    requests.post(
        WEBHOOK,
        json={
            "content": message
        }
    )


def load_seen():
    try:
        with open(SEEN_FILE) as f:
            return json.load(f)
    except:
        return []


def save_seen(data):
    with open(SEEN_FILE, "w") as f:
        json.dump(data, f)


seen = load_seen()


for store in stores:

    try:

        r = requests.get(
            store["url"],
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        soup = BeautifulSoup(
            r.text,
            "lxml"
        )

        text = soup.get_text(" ").lower()

        if any(word in text for word in good_words):

            if any(word in text for word in bad_words):
                continue

            product_id = store["name"] + store["url"]

            if product_id not in seen:

                send_alert(
f"""
🚨 POKÉMON MSRP ALERT 🚨

Store:
{store['name']}

Possible sealed product activity detected!

Link:
{store['url']}

Detected:
{datetime.now()}
"""
                )

                seen.append(product_id)

    except Exception as e:
        print(store["name"], e)


save_seen(seen)
