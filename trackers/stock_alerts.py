import requests


SOURCES = [
    "https://www.pokemon.com/us/pokemon-news/"
]


def check():

    alerts = []

    for source in SOURCES:

        try:

            r = requests.get(
                source,
                headers={
                    "User-Agent": "Mozilla/5.0"
                },
                timeout=20
            )


            if r.status_code == 200:

                alerts.append(
                    {
                        "source": source,
                        "status": "active"
                    }
                )


        except Exception as e:

            print(
                "Tracker error:",
                e
            )


    return alerts
