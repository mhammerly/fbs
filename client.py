import sys
import os
from urllib.request import urlopen
import hashlib

# each node on the network gets one hardcoded account number
accts = {'10.1.1.1':10293,
         '10.1.1.2':1293,
         '10.1.1.3':13333,
         '10.1.1.4':7466,
         '10.1.1.5':4137,
         'localhost':19001}

# server_host = 'http://10.1.1.5:9999'
server_host = 'http://127.0.0.1:9999'

# f = os.popen('ifconfig eth1 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
# ip = f.read()[:-1]
# f.close()

ip = '10.1.1.1'

def main(args):
    if len(args) != 3:
        print("Usage: client.py <destination address> <amount>")
        return
    dest = args[1]
    amt = args[2]
    f = open("rolling_code", "r+t")
    transfer_number = int(f.read()[:-1] or 1)
    rolling_code = hashlib.md5(bytes(str(transfer_number)+":"+str(accts[ip]), "ASCII")).hexdigest()
    data = bytes("src="+str(accts[ip]) + "&dest="+str(accts[dest]) + "&amt="+amt + "&t="+rolling_code, "ASCII")
    response = urlopen(server_host, data)
    if response.code == 200:
        f.seek(0)
        f.truncate()
        f.write(str(transfer_number + 1) + "\n")
    f.close()

if __name__ == "__main__":
    main(sys.argv)
