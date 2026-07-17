import os
import json
import requests
from datetime import datetime

from retailers import pokemon_center
from retailers import walmart


WEBHOOK = os.environ["DISCORD_WEBHOOK"]

SEEN_FILE = "seen_products.json"
SETTINGS_FILE = "settings.json"


def load_file(filename, default):
    try:
        with open(filename) as f:
            return json.load(f)
    except:
        return default


def save_seen(data):
    with open(SEEN_FILE, "w") as f:
        json.dump(data, f)


def send_alert(product):

    message = f"""
🚨 POKÉMON MSRP ALERT 🚨

🔥 {product['name']}

Store:
{product['store']}

Price:
{product.get('price','Check link')}

Status:
{product.get('status','Possible preorder/restock')}

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


seen = load_file(
    SEEN_FILE,
    {}
)

settings = load_file(
    SETTINGS_FILE,
    {}
)


retailers = [
    pokemon_center,
    walmart
]


for retailer in retailers:

    try:

        products = retailer.check()

        for item in products:

            product = {
                "name": item["name"],
                "link": item["link"],
                "store": retailer.__name__.split(".")[-1],
                "status": "Possible preorder/restock"
            }


            product_id = (
                product["store"]
                +
                product["link"]
            )


            if product_id not in seen:

                send_alert(product)

                seen[product_id] = str(
                    datetime.now()
                )


    except Exception as e:
        print(
            retailer,
            e
        )


save_seen(seen)
