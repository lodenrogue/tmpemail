import re
import requests

BASE_URL = "https://www.1secmail.com/api/v1/"

GET_DOMAINS_LIST_URL = BASE_URL + "?action=getDomainList"

GET_RANDOM_EMAIL_URL = BASE_URL + "?action=genRandomMailbox&count=1"

BANNED_USERS = ["abuse", "webmaster", "contact", "postmaster", "hostmaster", "admin"]

SIMPLE_EMAIL_PREFIX_PATTERN = "[a-z0-9]+@"


class OneSecMail:

    def get_domains(self):
        response = requests.get(GET_DOMAINS_LIST_URL)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error getting domains list")


    def get_random_email(self):
        response = requests.get(GET_RANDOM_EMAIL_URL)

        if response.status_code == 200:
            return response.json()[0]
        else:
            raise Exception("Error getting random email")


    def is_allowed_email(self, email):
        pattern = re.compile(SIMPLE_EMAIL_PREFIX_PATTERN)

        if pattern.match(email) is None:
            print("Error: Invalid email format")
            return False

        user = email.split("@")[0]

        if user in BANNED_USERS:
            print(f"Error: User {user} not allowed")
            print(f"Banned users: {BANNED_USERS}")
            return False

        domain = email.split("@")[1]
        domains = self.get_domains()

        if domain not in self.get_domains():
            print(f"Error: Invalid domain")
            print(f"Domain must be one of: {domains}")
            return False
        else:
            return True
