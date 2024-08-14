import argparse
from one_sec_mail import OneSecMail

def run(get_domains):
    mail_service = OneSecMail()

    if get_domains:
        domains = mail_service.get_domains()
        print_domains(domains)


def print_domains(domains):
    print("List if available domains:")
    for domain in domains:
        print(f"- {domain}")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domains", help="print a list of available domains", action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    run(args.domains)
