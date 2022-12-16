import argparse
import pandas as pd
import random

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
            print(f"Klaus {key} will give a wunderschön gift to Klaus {value.name}")

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
    klaus_list = []
    for _, klaus in participants.iterrows():
        klaus_list.append(Klaus(klaus['name'],klaus['mail'],klaus['belsnickel']))
    secret_santa = SecretSanta(klaus_list)
    secret_santa.create_pairing()
    secret_santa.show_pairing()

