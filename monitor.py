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
def load_availability():

    try:
        with open(AVAILABILITY_FILE) as f:
            return json.load(f)

    except:
        return {
            "positive": [],
            "negative": []
        }

def load_seen():
    prices = load_prices()
    def check_price(name, price=None):
        if price is None:
        return "⚪ PRICE UNKNOWN"

    name = name.lower()

    for category, data in prices["categories"].items():

        if category in name:

            if price <= data["msrp"]:
                return "🟢 AT MSRP"

            elif price <= data["max"]:
                return "🟡 ACCEPTABLE"

            else:
                return "🔴 OVER MSRP"


    return "⚪ NO DATA"
def load_prices():
    pack_rules = load_pack_rules()
    availability = load_availability()
    def check_availability(text):

    text = text.lower()

    for word in availability["negative"]:
        if word in text:
            return False

    for word in availability["positive"]:
        if word in text:
            return True

    return True
    def pack_value(name, price=None):

        if price is None:
           return "⚪ UNKNOWN"

    name = name.lower()

    for product, data in pack_rules["pack_values"].items():

        if product in name:

            packs = data["packs"]

            cost = price / packs

            if cost <= 7:
                return f"🟢 EXCELLENT (${cost:.2f}/pack)"

            elif cost <= 10:
                return f"🟡 GOOD (${cost:.2f}/pack)"

            else:
                return f"🔴 LOW (${cost:.2f}/pack)"


    return "⚪ UNKNOWN"
    def load_pack_rules():

    try:
        with open(PACK_FILE) as f:
            return json.load(f)

    except:
        return {
            "pack_values": {}
        }

    try:
        with open(PRICE_FILE) as f:
            return json.load(f)

    except:
        return {
            "categories": {}
        }
def load_watchlist():

    try:
        with open(WATCHLIST_FILE) as f:
            return json.load(f)

    except:
        return {
            "watchlist": [],
            "ignore": [],
            "priority_sets": []
        }  

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
                        {
    "name": "💰 Price Check",
    "value": check_price(product["name"]),
    "inline": True
},
                        "name": "📦 Pack Value",
                        "value": pack_value(product["name"]),
                        "inline": True
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
watchlist = load_watchlist()
def should_alert(name):

    name = name.lower()

    for word in watchlist["ignore"]:

        if word.lower() in name:
            return False


    return any(
        word.lower() in name
        for word in watchlist["watchlist"]
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


for store_name, retailer in retailers:

    try:

        products = retailer.check()

        for item in products:

            product_id = (
                store_name +
                item["link"]
            )


           if (
    product_id not in seen
    and should_alert(item["name"])
    and check_availability(item["name"])
):

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
