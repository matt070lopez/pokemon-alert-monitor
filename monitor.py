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

WATCHLIST_FILE = "watchlist.json"
SEEN_FILE = "seen_products.json"
PRICE_FILE = "price_rules.json"
PACK_FILE = "pack_value_rules.json"
AVAILABILITY_FILE = "availability_rules.json"


def load_json(file, default):
    try:
        with open(file) as f:
            return json.load(f)
    except Exception:
        return default


watchlist = load_json(
    WATCHLIST_FILE,
    {
        "watchlist": [],
        "ignore": [],
        "priority_sets": []
    }
)

price_rules = load_json(
    PRICE_FILE,
    {
        "categories": {}
    }
)

pack_rules = load_json(
    PACK_FILE,
    {
        "pack_values": {}
    }
)

availability_rules = load_json(
    AVAILABILITY_FILE,
    {
        "positive": [],
        "negative": []
    }
)

seen = load_json(
    SEEN_FILE,
    {}
)


def save_seen():

    with open(SEEN_FILE, "w") as f:
        json.dump(
            seen,
            f,
            indent=2
        )


def should_alert(name):

    name = name.lower()

    for word in watchlist["ignore"]:

        if word.lower() in name:
            return False


    return any(
        word.lower() in name
        for word in watchlist["watchlist"]
    )


def check_availability(name):

    name = name.lower()

    for word in availability_rules.get("negative", []):

        if word.lower() in name:
            return False


    return True


def get_priority(name):

    name = name.lower()

    for word in watchlist.get("priority_sets", []):

        if word.lower() in name:
            return "🔴 HIGH"


    if any(
        x in name
        for x in [
            "elite trainer box",
            "etb",
            "booster bundle",
            "booster box"
        ]
    ):
        return "🟡 MEDIUM"


    return "🟢 NORMAL"


def price_status(name, price=None):

    if price is None:
        return "⚪ PRICE UNKNOWN"


    name = name.lower()

    for category, data in price_rules["categories"].items():

        if category in name:

            if price <= data["msrp"]:
                return "🟢 AT MSRP"

            elif price <= data["max"]:
                return "🟡 ACCEPTABLE"

            else:
                return "🔴 OVER MSRP"


    return "⚪ NO DATA"


def pack_value(name, price=None):

    if price is None:
        return "⚪ UNKNOWN"


    name = name.lower()

    for product, data in pack_rules["pack_values"].items():

        if product in name:

            packs = data["packs"]

            cost = price / packs

            if cost <= 7:
                return f"🟢 EXCELLENT ${cost:.2f}/pack"

            elif cost <= 10:
                return f"🟡 GOOD ${cost:.2f}/pack"

            else:
                return f"🔴 LOW ${cost:.2f}/pack"


    return "⚪ UNKNOWN"


def send_alert(product, store):

    payload = {

        "embeds": [
            {

                "title": "🚨 POKÉMON DROP FOUND 🚨",

                "fields": [

                    {
                        "name": "📦 Product",
                        "value": product["name"][:1024],
                        "inline": False
                    },

                    {
                        "name": "🏪 Store",
                        "value": store,
                        "inline": True
                    },

                    {
                        "name": "⭐ Priority",
                        "value": get_priority(product["name"]),
                        "inline": True
                    },

                    {
                        "name": "💰 Price",
                        "value": price_status(product["name"]),
                        "inline": True
                    },

                    {
                        "name": "📦 Pack Value",
                        "value": pack_value(product["name"]),
                        "inline": True
                    }

                ],

                "url": product["link"],

                "footer": {
                    "text": f"Detected {datetime.now()}"
                }

            }
        ]

    }


    requests.post(
        WEBHOOK,
        json=payload,
        timeout=15
    )


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


for store, retailer in retailers:

    try:

        products = retailer.check()

        for product in products:

            product_id = (
                store +
                product["link"]
            )


            if product_id in seen:
                continue


            if not should_alert(product["name"]):
                continue


            if not check_availability(product["name"]):
                continue


            send_alert(
                product,
                store
            )


            seen[product_id] = str(
                datetime.now()
            )


    except Exception as e:

        print(
            store,
            "error:",
            e
        )


save_seen()
