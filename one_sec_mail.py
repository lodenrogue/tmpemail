import re
import requests

BASE_URL = "https://www.1secmail.com/api/v1/"

GET_DOMAINS_LIST_URL = BASE_URL + "?action=getDomainList"

GET_RANDOM_EMAIL_URL = BASE_URL + "?action=genRandomMailbox&count=1"

GET_ALL_MESSAGES_URL = BASE_URL + "?action=getMessages&login=[USER]&domain=[DOMAIN]"

GET_MESSAGE_URL = BASE_URL + "?action=readMessage&login=[USER]&domain=[DOMAIN]&id=[ID]"

BANNED_USERS = ["abuse", "webmaster", "contact", "postmaster", "hostmaster", "admin"]

SIMPLE_EMAIL_PREFIX_PATTERN = "[a-z0-9]+@"


class OneSecMail:

    def get_domains(self):
        response = requests.get(GET_DOMAINS_LIST_URL)
        return response.json()


    def get_random_email(self):
        response = requests.get(GET_RANDOM_EMAIL_URL)
        return response.json()[0]


    def is_allowed_email(self, email):
        pattern = re.compile(SIMPLE_EMAIL_PREFIX_PATTERN)

        if pattern.match(email) is None:
            print("Error: Invalid email format")
            return False

        user, domain = self.split_email(email)

        if user in BANNED_USERS:
            print(f"Error: User {user} not allowed")
            print(f"Banned users: {BANNED_USERS}")
            return False

        domains = self.get_domains()

        if domain not in self.get_domains():
            print(f"Error: Invalid domain")
            print(f"Domain must be one of: {domains}")
            return False
        else:
            return True

    def get_messages(self, email):
        user, domain = self.split_email(email)

        url = (GET_ALL_MESSAGES_URL
            .replace("[USER]", user)
            .replace("[DOMAIN]", domain))

        return requests.get(url).json()


    def get_message(self, email, message_id):
        user, domain = self.split_email(email)

        url = (GET_MESSAGE_URL
               .replace("[USER]", user)
               .replace("[DOMAIN]", domain)
               .replace("[ID]", message_id))
        
        return requests.get(url).json()


    def split_email(self, email):
        split = email.split("@")
        return (split[0], split[1])
        

        
