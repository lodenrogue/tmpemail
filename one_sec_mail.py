import requests

BASE_URL = "https://www.1secmail.com/api/v1/"

GET_DOMAINS_LIST_URL = BASE_URL + "?action=getDomainList"

class OneSecMail:

    def get_domains(self):
        response = requests.get(GET_DOMAINS_LIST_URL)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error getting domains list")
