import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import hashlib
import ssl

db = '/home/matt/825/mitm/fbs.db'
use_https = False

def validate_transaction(post_data):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT transfer_number FROM balances WHERE account=?", (post_data["src"][0],))
    transfer_number = c.fetchone()
    t = hashlib.md5(bytes(str(transfer_number[0]) + ":" + post_data["src"][0], "ASCII")).hexdigest()

    c.close()
    conn.close()
    return t == post_data["t"][0]

def get_balance(acct):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT balance FROM balances WHERE account=?", (acct,))
    balance = c.fetchone()[0]

    c.close()
    conn.close()
    return balance
    

class FBSRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        resource, _, query = self.path.partition("?")
        query_params = urllib.parse.parse_qs(query)
        acct = query_params['acct'][0]
        balance = get_balance(acct)
        self.wfile.write(bytes(str(balance), "ASCII"))
        return

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))

        # make sure we have all the headers we expect
        if "src" in post_data and "dest" in post_data and "amt" in post_data and "t" in post_data and validate_transaction(post_data):
            send_money(int(post_data["src"][0]), int(post_data["dest"][0]), int(post_data["amt"][0]))
            self.send_response(200)
        else:
            self.send_response(400)
        self.end_headers()
        return

def init():
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS balances")
    c.execute("CREATE TABLE balances (balance INTEGER, account INTEGER, transfer_number INTEGER)")

    # create empty accounts for student groups
    c.execute("INSERT INTO balances (balance, account, transfer_number) VALUES (0, 19001, 1)")
    c.execute("INSERT INTO balances (balance, account, transfer_number) VALUES (0, 19002, 1)")
    c.execute("INSERT INTO balances (balance, account, transfer_number) VALUES (0, 19003, 1)")
    c.execute("INSERT INTO balances (balance, account, transfer_number) VALUES (0, 19004, 1)")
    c.execute("INSERT INTO balances (balance, account, transfer_number) VALUES (0, 19005, 1)")

    # create account, transfer_numbers with dollars that will pass money around the network
    c.execute("INSERT INTO balances (balance, account, transfer_number) VALUES (70000, 10293, 1)")
    c.execute("INSERT INTO balances (balance, account, transfer_number) VALUES (92000, 1293, 1)")
    c.execute("INSERT INTO balances (balance, account, transfer_number) VALUES (22000, 10277, 1)")
    c.execute("INSERT INTO balances (balance, account, transfer_number) VALUES (1300, 13333, 1)")
    c.execute("INSERT INTO balances (balance, account, transfer_number) VALUES (81200, 11210, 1)")
    c.execute("INSERT INTO balances (balance, account, transfer_number) VALUES (73300, 7466, 1)")
    c.execute("INSERT INTO balances (balance, account, transfer_number) VALUES (60000, 4137, 1)")

    conn.commit()
    c.close()
    conn.close()

def send_money(src, dest, amt):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("SELECT balance FROM balances WHERE account=?", (src,))
    src_balance = c.fetchone()

    c.execute("SELECT balance FROM balances WHERE account=?", (dest,))
    dest_balance = c.fetchone()

    if (src_balance != None and dest_balance != None):
        c.execute("UPDATE balances SET balance=? WHERE account=?", (src_balance[0] - amt, src))
        c.execute("UPDATE balances SET transfer_number=transfer_number+1 WHERE account=?", (src,))
        c.execute("UPDATE balances SET balance=? WHERE account=?", (dest_balance[0] + amt, dest))

    conn.commit()
    c.close()
    conn.close()

def main():
    init()
    server_address = ("", 9999)
    httpd = HTTPServer(server_address, FBSRequestHandler)
    if use_https:
        httpd.socket = ssl.wrap_socket(httpd.socket,
                                       server_side=True,
                                       certfile="/root/cert.pem",
                                       keyfile="/root/key.pem",
                                       ssl_version=ssl.PROTOCOL_TLSv1)
    httpd.serve_forever()


if __name__ == "__main__":
    main()

