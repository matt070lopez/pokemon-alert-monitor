import requests
from bs4 import BeautifulSoup


URL = "https://www.pokemon.com/us/pokemon-news/"


KEYWORDS = [
    "tcg",
    "trading card",
    "booster",
    "elite trainer box",
    "collection",
    "pokemon center"
]


def check():

    alerts = []

    try:

        r = requests.get(
            URL,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        soup = BeautifulSoup(
            r.text,
            "lxml"
        )


        for article in soup.find_all("a", href=True):

            title = article.get_text(
                " ",
                strip=True
            )


            if not title:
                continue


            if any(
                word in title.lower()
                for word in KEYWORDS
            ):

                alerts.append(
                    {
                        "name": title,
                        "link": article["href"]
                    }
                )


    except Exception as e:

        print(
            "Pokemon news error:",
            e
        )


    return alerts
