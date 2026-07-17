import requests
from bs4 import BeautifulSoup


URL = "https://www.amazon.com/s?k=pokemon+cards"


KEYWORDS = [
    "pokemon",
    "elite trainer box",
    "etb",
    "booster bundle",
    "booster box",
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


        for item in soup.select(
            "div[data-component-type='s-search-result']"
        ):

            title = item.get_text(
                " ",
                strip=True
            )


            if not any(
                word in title.lower()
                for word in KEYWORDS
            ):
                continue


            link = item.find(
                "a",
                href=True
            )


            if link:

                products.append(
                    {
                        "name": title,
                        "link":
                        "https://www.amazon.com"
                        + link["href"]
                    }
                )


    except Exception as e:

        print(
            "Amazon error:",
            e
        )


    return products
