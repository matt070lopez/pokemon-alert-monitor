import os
import json
import requests
from datetime import datetime

from retailers import pokemon_center


WEBHOOK = os.environ["DISCORD_WEBHOOK"]

SEEN_FILE = "seen_products.json"


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
        return {}


def save_seen(data):
    with open(SEEN_FILE, "w") as f:
        json.dump(data, f)


seen = load_seen()


def process_products(products, store):

    for product in products:

        product_id = (
            store +
            product["link"]
        )

        if product_id in seen:
            continue


        send_alert(
f"""
🚨 POKÉMON MSRP DROP DETECTED 🚨

Product:
{product['name']}

Store:
{store}

Price:
Check link

Status:
Possible preorder/restock

Link:
{product['link']}

Detected:
{datetime.now()}
"""
        )

        seen[product_id] = str(datetime.now())


products = pokemon_center.check()

process_products(
    products,
    "Pokémon Center"
)


save_seen(seen)
