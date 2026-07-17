import requests
from bs4 import BeautifulSoup


URL = "https://www.samsclub.com/s/pokemon"


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


        for a in soup.find_all(
            "a",
            href=True
        ):

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

                link = a["href"]

                if link.startswith("/"):
                    link = "https://www.samsclub.com" + link


                products.append(
                    {
                        "name": name,
                        "link": link
                    }
                )


    except Exception as e:

        print(
            "Sam's Club error:",
            e
        )


    return products
