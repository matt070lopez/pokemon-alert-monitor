import requests
from bs4 import BeautifulSoup


URL = "https://www.costco.com/CatalogSearch?dept=All&keyword=pokemon"


KEYWORDS = [
    "pokemon",
    "elite trainer box",
    "booster",
    "collection",
    "bundle"
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


        for a in soup.find_all(
            "a",
            href=True
        ):

            name = a.get_text(
                " ",
                strip=True
            )


            if any(
                word in name.lower()
                for word in KEYWORDS
            ):

                products.append(
                    {
                        "name": name,
                        "link": a["href"]
                    }
                )


    except Exception as e:

        print(
            "Costco error:",
            e
        )


    return products
