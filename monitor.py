import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin


WEBHOOK = os.environ["DISCORD_WEBHOOK"]

SEEN_FILE = "seen_products.json"
CONFIG_FILE = "store_config.json"


KEYWORDS = [
    "pokemon",
    "elite trainer box",
    "etb",
    "booster",
    "bundle",
    "collection",
    "premium",
    "box",
    "tin",
    "blister"
]

IGNORE = [
    "binder",
    "sleeves",
    "protector",
    "single card",
    "graded",
    "psa",
    "cgc"
]


def send_alert(message):
    requests.post(
        WEBHOOK,
        json={
            "content": message
        }
    )


def load_json(file):
    try:
        with open(file) as f:
            return json.load(f)
    except:
        return {}


def save_seen(data):
    with open(SEEN_FILE, "w") as f:
        json.dump(data, f)


seen = load_json(SEEN_FILE)
config = load_json(CONFIG_FILE)


for store in config.get("stores", []):

    try:

        response = requests.get(
            store["url"],
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        soup = BeautifulSoup(
            response.text,
            "lxml"
        )

        links = soup.find_all("a", href=True)

        for link in links:

            title = link.get_text(" ", strip=True)

            if not title:
                continue

            title_lower = title.lower()

            if not any(k in title_lower for k in KEYWORDS):
                continue

            if any(i in title_lower for i in IGNORE):
                continue


            product_url = urljoin(
                store["url"],
                link["href"]
            )


            product_id = (
                store["name"]
                +
                product_url
            )


            if product_id not in seen:

                send_alert(
f"""
🚨 POKÉMON MSRP ALERT 🚨

Product:
{title}

Store:
{store['name']}

Link:
{product_url}

Detected:
{datetime.now()}
"""
                )

                seen[product_id] = str(datetime.now())


    except Exception as e:
        print(
            store["name"],
            e
        )


save_seen(seen)
