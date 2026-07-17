import requests
import os
from datetime import datetime

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

products = [
    {
        "store": "Pokémon Center",
        "url": "https://www.pokemoncenter.com/en-us/category/tcg",
    },
    {
        "store": "Walmart",
        "url": "https://www.walmart.com/search?q=pokemon+cards",
    },
    {
        "store": "Target",
        "url": "https://www.target.com/s?searchTerm=pokemon+cards",
    }
]


keywords = [
    "pokemon",
    "elite trainer",
    "booster",
    "box",
    "bundle",
    "collection",
    "premium",
    "etb"
]


def send_alert(message):
    requests.post(
        WEBHOOK,
        json={
            "content": message
        }
    )


for item in products:
    try:
        r = requests.get(
            item["url"],
            headers={
                "User-Agent":"Mozilla/5.0"
            },
            timeout=10
        )

        text = r.text.lower()

        found = []

        for word in keywords:
            if word in text:
                found.append(word)

        if found:
            send_alert(
                f"""
🚨 Pokémon Alert

Store:
{item['store']}

Possible product activity detected!

Keywords:
{', '.join(found)}

Time:
{datetime.now()}
"""
            )

    except Exception as e:
        print(e)
