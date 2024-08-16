import requests

SHORTENER_URL = "https://is.gd/create.php?format=simple"

class UrlShortener:

    def shorten(self, url):
        response = requests.post(SHORTENER_URL, data=dict(url=url))
        return response.text.strip()
