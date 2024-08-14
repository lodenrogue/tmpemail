import argparse
import os
from one_sec_mail import OneSecMail

TEMP_EMAIL_DIRECTORY = "/tmp/tmpemail"


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
        

    # Create the temp email directory if it doesn't exist
    os.makedirs(TEMP_EMAIL_DIRECTORY, exist_ok=True)

    with open(f"{TEMP_EMAIL_DIRECTORY}/email_address", "w") as f:
        f.write(email_address)

    print(email_address)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domains", help="print a list of available domains", action="store_true")
    parser.add_argument("-g", "--generate", help="generate a new email address", nargs="?", const="random")
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    if args.domains:
        print_domains()
    elif args.generate:
        generate_email(args.generate)
