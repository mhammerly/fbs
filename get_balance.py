import os
from urllib.request import urlopen
import json

use_https = False

accts = {'grp1': 19001,
         'grp2': 19002,
         'grp3': 19003,
         'grp4': 19004,
         'grp5': 19005}

# server_host = ("https" if use_https else "http") + '://10.1.1.5:9999'
server_host = ("https" if use_https else "http") + '://127.0.0.1:9999'

def main():
    user = os.getlogin()
    # user = 'grp1'
    acct = accts[user]
    url = server_host + "?acct=" + str(acct)
    response = urlopen(url)
    if (response.code == 200):
        balance = response.readall().decode("ASCII")
        print("Balance for " + str(acct) + ": " + balance)


if __name__ == "__main__":
    main()
