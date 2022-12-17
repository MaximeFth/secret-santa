import argparse
import pandas as pd
import random
from rich.progress import track
import json
from email.mime.text import MIMEText
import pickle
import smtplib, ssl

class SecretSanta:
    def __init__(self,klaus_list, chain_number=1,blind=False):
        """
        The list is shuffled wrt the seed given, because I know youll forget which seed you put in it will dumnp the pairings in a file, in case anything goes wrong...
        """
        self.klaus_list = klaus_list
        random.shuffle(klaus_list)
        self.chain_number = chain_number
        self.blind = blind
        self.number_of_participants = len(klaus_list)
        with open('pairings.pkl', 'wb') as f:
            pickle.dump(self.klaus_list, f)

    def create_pairing(self):
        """
        Creates a pairing list by taking into account the impish list. This function has been implemented by a blind donkey, and has a worst case complexity probably of O(Tree(n!)), use it with care.
        """
        self.giver_receiver = dict()
        for index, klaus in enumerate(self.klaus_list):
            self.giver_receiver[klaus.name] = klaus_list[(index+1)%self.number_of_participants]
        for index, klaus in enumerate(self.klaus_list):
            if not (klaus.impish_list==0):
                if self.giver_receiver[klaus.name].name in (klaus.impish_list):
                    random.shuffle(self.klaus_list)
                    self.create_pairing()
        return self.giver_receiver

    def show_pairing(self):
        """
        Show the pairing list
        """
        for key, value in self.giver_receiver.items() :
            print(f"{key:<18} -> {value.name:<18}")
            
    def send_game(self,secrets):
        """
        Send game to all participants by mail.
        """
        smtp_server = "smtp.gmail.com"
        port = 587  
        email_sender = secrets["EMAIL_SENDER"]
        password =secrets["PASSWORD"]
        context = ssl.create_default_context()
        for klaus in track(self.klaus_list,description="Sending HOHOHOs"):
            # Don't forget to change the mail content, unless your name is stan.
            message=MIMEText(f"""\
            Dear {klaus.name}! 
            
            You will be the secret santa of: {self.giver_receiver[klaus.name].name}.

            Yours sincerely,

            Stan
            """)

            email_receiver=klaus.mail
            message["To"] = klaus.mail
            message['From'] = email_sender
            message['Subject'] = 'Secret Santa HO HO HO'

            try:
                server = smtplib.SMTP(smtp_server,port)
                server.starttls(context=context) 
                server.login(email_sender, password)
                server.sendmail(email_sender, email_receiver, message.as_string())

            except Exception as e:
                print(e)
            finally:
                server.quit() 
            
# In a secret santa, everyone participant is a santa klaus.
class Klaus:
    def __init__(self,name,mail,impish_list=None):
        self.name = name.replace("_"," ")
        self.mail = mail
        self.impish_list = impish_list

        if not (self.impish_list==0):
            print(self.impish_list)
            self.impish_list=self.impish_list.replace("_"," ").split(":")
    
def parse_args():
    """
    Parse command line flags.
    :return results: Namespace of the arguments to pass to the main run function.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--send', action='store_true',default=False,help="Add this arg to send all mails.")
    parser.add_argument('--blind', action='store_true',default=False,help="Add this arg to not be spoiled")
    parser.add_argument('--seed', type=int,default=-1 ,help='Seed for the pairing randomness')
    results = parser.parse_args()

    return results


if __name__ == '__main__':
    try:
        with open("secrets.json", mode='r') as f:
            secrets = json.loads(f.read())
    except FileNotFoundError:
            print("filenotfound")
    args = parse_args()
    if args.seed>=0:
        random.seed(args.seed)
    
    participants = pd.read_csv("participants.csv")
    participants['impish_list']= participants['impish_list'].fillna(0)
    klaus_list = []
    for _, klaus in participants.iterrows():
        klaus_list.append(Klaus(klaus['name'],klaus['mail'],klaus['impish_list']))
    secret_santa = SecretSanta(klaus_list)
    secret_santa.create_pairing()
    if not args.blind:
        secret_santa.show_pairing()
        secret_santa.write_list()
    if args.send:
        secret_santa.send_game(secrets)
    
    
