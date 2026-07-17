import requests
from bs4 import BeautifulSoup


URL = "https://www.pokemoncenter.com/en-us/category/trading-card-game"


KEYWORDS = [
    "pokemon",
    "elite trainer box",
    "etb",
    "booster",
    "bundle",
    "collection",
    "premium",
    "tin"
]


def check():

    products = []

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


        for a in soup.find_all("a", href=True):

            name = a.get_text(
                " ",
                strip=True
            )


            if not name:
                continue


            if any(
                word in name.lower()
                for word in KEYWORDS
            ):

                products.append(
                    {
                        "name": name,
                        "link": "https://www.pokemoncenter.com"
                        + a["href"]
                    }
                )


    except Exception as e:
        print(
            "Pokemon Center error:",
            e
        )


    return products
