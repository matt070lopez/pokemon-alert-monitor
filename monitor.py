import os
import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin


WEBHOOK = os.environ["DISCORD_WEBHOOK"]

SEEN_FILE = "seen_products.json"
CONFIG_FILE = "store_config.json"
MSRP_FILE = "msrp_database.json"


KEYWORDS = [
    "pokemon",
    "elite trainer box",
    "etb",
    "booster bundle",
    "booster box",
    "premium collection",
    "collection",
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
        json={"content": message}
    )


def load_file(filename, default):
    try:
        with open(filename) as f:
            return json.load(f)
    except:
        return default


seen = load_file(SEEN_FILE, {})
config = load_file(CONFIG_FILE, {})
msrp = load_file(MSRP_FILE, {})


for store in config.get("stores", []):

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

        for a in soup.find_all("a", href=True):

            title = a.get_text(
                " ",
                strip=True
            )

            if not title:
                continue


            lower = title.lower()


            if not any(k in lower for k in KEYWORDS):
                continue


            if any(i in lower for i in IGNORE):
                continue


            price_match = re.search(
                r"\$(\d+\.\d{2})",
                title
            )


            price = None

            if price_match:
                price = float(
                    price_match.group(1)
                )


            allowed = False


            for product_type, data in msrp.get("products", {}).items():

                if product_type in lower:

                    if price is None:
                        allowed = True

                    elif price <= data["max_price"]:
                        allowed = True


            if not allowed:
                continue


            link = urljoin(
                store["url"],
                a["href"]
            )


            product_id = (
                store["name"]
                +
                link
            )


            if product_id not in seen:


                send_alert(
f"""
🚨 POKÉMON MSRP ALERT 🚨

Product:
{title}

Store:
{store['name']}

Price:
{price if price else "Check link"}

Link:
{link}

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


with open(SEEN_FILE, "w") as f:
    json.dump(
        seen,
        f
    )
