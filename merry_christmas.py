import argparse
import pandas as pd
import random
from rich.console import Console
import smtplib, ssl

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "mail@gmail.com"
password = "password"

class SecretSanta:
    def __init__(self,klaus_list, chain_number=1,blind=False):
        self.klaus_list = klaus_list
        random.shuffle(klaus_list)
        self.chain_number = chain_number
        self.blind = blind
        self.number_of_participants = len(klaus_list)

    def create_pairing(self)->dict:
        self.giver_receiver = dict()
        for index, klaus in enumerate(self.klaus_list):
            self.giver_receiver[klaus.name] = klaus_list[(index+1)%self.number_of_participants]
        return self.giver_receiver

    def show_pairing(self):
        for key, value in self.giver_receiver.items() :
            console.print(f"[bold] {key:<15} -> {value.name:<15}")
    def send_game(self):
        for klaus in self.klaus_list:
            message = f"""\
                Subject: Secret_Santa

                Hello {klaus.name}, you will be the secret santa of: {self.giver_receiver[klaus.name]}.
                """
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, klaus.mail, message)
                server.quit()
# In a secret santa, everyone participant is a santa klaus.
class Klaus:
    def __init__(self,name,mail,belsnickel=None):
        self.name = name
        self.mail = mail
        self.belsnickel = belsnickel
    
def parse_args():
    """
    Parse command line flags.
    :return results: Namespace of the arguments to pass to the main run function.
    """
    parser = argparse.ArgumentParser()




    results = parser.parse_args()

    return results

if __name__ == '__main__':
    args = parse_args()
    participants = pd.read_csv("participants.csv")
    console = Console()
    klaus_list = []
    for _, klaus in participants.iterrows():
        klaus_list.append(Klaus(klaus['name'],klaus['mail'],klaus['belsnickel']))
    secret_santa = SecretSanta(klaus_list)
    secret_santa.create_pairing()
    secret_santa.show_pairing()
    secret_santa.send_game()

