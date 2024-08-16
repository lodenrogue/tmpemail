import argparse
import os
import subprocess
from one_sec_mail import OneSecMail
from url_shortener import UrlShortener

TEMP_EMAIL_DIRECTORY = "/tmp/tmpemail"

EMAIL_ADDRESS_FILE = TEMP_EMAIL_DIRECTORY + "/email_address"

TEMP_EMAIL_MESSAGE_FILE = TEMP_EMAIL_DIRECTORY + "/tmpemail.html"

EMAIL_MESSAGE_TEMPLATE = """
<pre><b>To: </b>[TO]
<b>From: </b>[FROM]
<b>Subject: </b>[SUBJECT]</pre>
[HTML_BODY]
[ATTACHMENTS]
"""


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
    email = get_email()
    messages = get_messages_from_service()

    print(f"[ Inbox for {email} ]\n")

    for message in messages:
        print(f"{message['id']}\t{message['from']}\t{message['subject']}")


def get_email():
    if not os.path.exists(EMAIL_ADDRESS_FILE):
        return None
    else:
        with open(EMAIL_ADDRESS_FILE, "r") as f:
            return f.readline()


def get_message(message_id, is_plain_text):
    mail_service = OneSecMail()

    email = get_email()
    message = mail_service.get_message(email, message_id)

    if message == "Message not found":
        print(message)
        exit(1)
    else:
        content = create_body_html(email, message)

        if is_plain_text:
            attachments = create_attachments_plain_text(message)
        else:
            attachments = create_attachments_html(message)

        content = content.replace("[ATTACHMENTS]", attachments)

        with open(TEMP_EMAIL_MESSAGE_FILE, "w") as f:
            f.write(content)

        if is_plain_text:
            subprocess.run(["w3m", "-dump", TEMP_EMAIL_MESSAGE_FILE])
        else:
            subprocess.run(["w3m", TEMP_EMAIL_MESSAGE_FILE])


def open_recent(is_plain_text):
    messages = get_messages_from_service()

    if messages:
        message_id = str(messages[0]["id"])
        get_message(message_id, is_plain_text)


def get_messages_from_service():
    mail_service = OneSecMail()
    email = get_email()

    if email is None:
        email = mail_service.get_random_email()
        save_email(email)

    return mail_service.get_messages(email)


def create_attachments_plain_text(message):
    text = ""
    attachments = message["attachments"]

    if attachments:
        text = "[Attachments]<br>"

    for attachment in attachments:
        link = UrlShortener().shorten(attachment["link"])
        filename = attachment["filename"]
        text += f"{link} [{filename}]<br>"

    return text


def create_attachments_html(message):
    html = ""
    attachments = message["attachments"]

    if attachments:
        html = "<br><b>[Attachments]</b><br>"

    for attachment in attachments:
        link = attachment["link"]
        filename = attachment["filename"]
        html += f"<a href={link} download={filename}>{filename}</a><br>"

    return html


def create_body_html(email, message):
    to = email
    sender = message["from"]
    subject = message["subject"]
    body = message["htmlBody"] if message["htmlBody"] else message["textBody"]

    return (EMAIL_MESSAGE_TEMPLATE
            .replace("[TO]", to)
            .replace("[FROM]", sender)
            .replace("[SUBJECT]", subject)
            .replace("[HTML_BODY]", body))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domains", help="print a list of available domains", action="store_true")
    parser.add_argument("-g", "--generate", help="generate a new email address", nargs="?", const="random")
    parser.add_argument("-r", "--recent", help="view the most recent email", action="store_true")
    parser.add_argument("-t", "--text", help="view the email as plain text", action="store_true")
    parser.add_argument("message", help="id of email message to retrieve", nargs="?")
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    if args.domains:
        print_domains()
    elif args.generate:
        generate_email(args.generate)
    elif args.recent:
        open_recent(args.text)
    elif args.message:
        get_message(args.message, args.text)
    else:
        get_messages()
