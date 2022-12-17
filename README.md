# Secret-Santa in Python

## Merry Christmas!

This super simple python script will send to all your friends who they need to give a gift to. Note that although this script is wonderful and simple to use, the first step that is to collect your friends mail can be a pain in the ass.

### Create participants list `participants.csv`.
-  If you want someone to avoid giving a gift to someone that they find impish, add them to the `impish_list` field. You can add multiple naughty persons given you separate them using colons `:` (Note that the relation is asymmetric, Chris don't want to give to Will but Will could be ending up giving a present to Chris.)

```
name,mail,impish_list
James,James.Cameron@gmail.com,
Will,Will.Smith@gmail.com,
Chris,Chris.Rock@gmail.com,Will
```

### Setup your secret file `secrets.json`. 
To obtain your secret password, follow this [tutorial](https://stackoverflow.com/questions/72478573/how-to-send-an-email-using-python-after-googles-policy-update-on-not-allowing-j), provided by `X0-user-0X` <3

```
{
    "EMAIL_SENDER": "MySuperGMAILAccount@gmail.com",
    "PASSWORD": "passwooord"
}
```

### `merry-christmas.py`, where the magic happens
```
usage: merry_christmas.py [-h] [--send] [--blind] [--seed SEED] [--pairing PAIRING]

optional arguments:
  -h, --help         show this help message and exit
  --send             Add this arg to send all mails.
  --blind            Add this arg to not be spoiled
  --seed SEED        Seed for the pairing randomness
  --pairing PAIRING  Pairing you already computed and want to send
```

### Requirements
```
pip3 install -r requirements.txt
```