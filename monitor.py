import os
import json
import requests
from datetime import datetime

from retailers import pokemon_center
from retailers import walmart
from retailers import target
from retailers import gamestop
from retailers import bestbuy
from retailers import amazon
from retailers import costco
from retailers import samsclub


WEBHOOK = os.environ["DISCORD_WEBHOOK"]

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


def get_priority(name):

    name = name.lower()

    high_priority = [
        "pokemon center",
        "exclusive",
        "151",
        "mega",
        "special",
        "limited"
    ]

    medium_priority = [
        "elite trainer box",
        "etb",
        "booster bundle",
        "booster box"
    ]

    if any(x in name for x in high_priority):
        return "🔴 HIGH"

    if any(x in name for x in medium_priority):
        return "🟡 MEDIUM"

    return "🟢 NORMAL"


def send_alert(product):

    priority = get_priority(
        product["name"]
    )

    payload = {

        "embeds": [
            {
                "title": "🚨 POKÉMON DROP FOUND 🚨",

                "fields": [
                    {
                        "name": "🔥 Product",
                        "value": product["name"],
                        "inline": False
                    },
                    {
                        "name": "🏪 Store",
                        "value": product["store"],
                        "inline": True
                    },
                    {
                        "name": "⭐ Priority",
                        "value": priority,
                        "inline": True
                    },
                    {
                        "name": "📦 Status",
                        "value": "Possible preorder/restock",
                        "inline": False
                    }
                ],

                "url": product["link"],

                "footer": {
                    "text":
                    f"Detected {datetime.now()}"
                }
            }
        ]
    }


    requests.post(
        WEBHOOK,
        json=payload
    )


seen = load_seen()


retailers = [

    ("Pokémon Center", pokemon_center),
    ("Walmart", walmart),
    ("Target", target),
    ("GameStop", gamestop),
    ("Best Buy", bestbuy),
    ("Amazon", amazon),
    ("Costco", costco),
    ("Sam's Club", samsclub)

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
