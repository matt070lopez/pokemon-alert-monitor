import json
import requests
from datetime import datetime

from retailers import pokemon_center
from retailers import walmart
from retailers import target
from retailers import gamestop
from retailers import bestbuy


WEBHOOK = "DISCORD_WEBHOOK"

SEEN_FILE = "seen_products.json"


def load_seen():

    try:
        with open(SEEN_FILE) as f:
            return json.load(f)

    except:
        return {}


def save_seen(data):

    with open(SEEN_FILE, "w") as f:
        json.dump(data, f)


def send_alert(product):

    message = f"""
🚨 POKÉMON MSRP ALERT 🚨

🔥 {product['name']}

Store:
{product['store']}

Status:
Possible preorder/restock

Link:
{product['link']}

Detected:
{datetime.now()}
"""

    requests.post(
        WEBHOOK,
        json={
            "content": message
        }
    )


seen = load_seen()


retailers = [
    ("Pokémon Center", pokemon_center),
    ("Walmart", walmart),
    ("Target", target),
    ("GameStop", gamestop),
    ("Best Buy", bestbuy)
]


for store_name, retailer in retailers:

    try:

        products = retailer.check()

        for item in products:

            product_id = (
                store_name +
                item["link"]
            )


            if product_id not in seen:

                send_alert(
                    {
                        "name": item["name"],
                        "store": store_name,
                        "link": item["link"]
                    }
                )

                seen[product_id] = str(
                    datetime.now()
                )


    except Exception as e:

        print(
            store_name,
            e
        )


save_seen(seen)
