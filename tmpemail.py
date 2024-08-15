import argparse
import os
import subprocess
from one_sec_mail import OneSecMail

TEMP_EMAIL_DIRECTORY = "/tmp/tmpemail"

EMAIL_ADDRESS_FILE = TEMP_EMAIL_DIRECTORY + "/email_address"

TEMP_EMAIL_MESSAGE_FILE = TEMP_EMAIL_DIRECTORY + "/tmpemail.html"


def print_domains():
    mail_service = OneSecMail()

    domains = mail_service.get_domains()
    print("List if available domains:")

    for domain in domains:
        print(f"- {domain}")


def generate_email(email):
    mail_service = OneSecMail()
    email_address = ""

    if email == "random":
        email_address = mail_service.get_random_email()
    else:
        if mail_service.is_allowed_email(email):
            email_address = email
        else:
            exit(1)
        
    save_email(email_address)
    print(email_address)


def save_email(email):
    # Create the temp email directory if it doesn't exist
    os.makedirs(TEMP_EMAIL_DIRECTORY, exist_ok=True)

    with open(EMAIL_ADDRESS_FILE, "w") as f:
        f.write(email)


def get_messages():
    mail_service = OneSecMail()
    email = get_email()

    if email is None:
        email = mail_service.get_random_email()
        save_email(email)

    messages = mail_service.get_messages(email)
    print(f"[ Inbox for {email} ]\n")

    for message in messages:
        print(f"{message['id']}\t{message['from']}\t{message['subject']}")


def get_email():
    if not os.path.exists(EMAIL_ADDRESS_FILE):
        return None
    else:
        with open(EMAIL_ADDRESS_FILE, "r") as f:
            return f.readline()


def get_message(message_id):
    mail_service = OneSecMail()

    email = get_email()
    message = mail_service.get_message(email, message_id)

    if message == "Message not found":
        print(message)
        exit(1)
    else:
        to = email
        sender = message["from"]
        subject = message["subject"]
        body = message["htmlBody"] if message["htmlBody"] else message["textBody"]

        content = f"To: {to}\nFrom: {sender}\nSubject: {subject}\n{body}"

        with open(TEMP_EMAIL_MESSAGE_FILE, "w") as f:
            f.write(content)

        subprocess.run(["w3m", TEMP_EMAIL_MESSAGE_FILE])


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domains", help="print a list of available domains", action="store_true")
    parser.add_argument("-g", "--generate", help="generate a new email address", nargs="?", const="random")
    parser.add_argument("message", help="id of email message to retrieve", nargs="?")
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    if args.domains:
        print_domains()
    elif args.generate:
        generate_email(args.generate)
    elif args.message:
        get_message(args.message)
    else:
        get_messages()
