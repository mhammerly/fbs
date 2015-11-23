import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib

db = '/home/matt/825/mitm/fbs.db'

class FBSRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        return

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))

        # make sure we have all the headers we expect
        if "src" in post_data and "dest" in post_data and "amt" in post_data:
            send_money(int(post_data["src"][0]), int(post_data["dest"][0]), int(post_data["amt"][0]))
            self.send_response(200)
        else:
            self.send_response(400)
        return

def init():
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS balances")
    c.execute("CREATE TABLE balances (balance INTEGER, account INTEGER)")

    # create empty accounts for student groups
    c.execute("INSERT INTO balances (balance, account) VALUES (0, 19001)")
    c.execute("INSERT INTO balances (balance, account) VALUES (0, 19002)")
    c.execute("INSERT INTO balances (balance, account) VALUES (0, 19003)")
    c.execute("INSERT INTO balances (balance, account) VALUES (0, 19004)")
    c.execute("INSERT INTO balances (balance, account) VALUES (0, 19005)")

    # create accounts with dollars that will pass money around the network
    c.execute("INSERT INTO balances (balance, account) VALUES (70000, 10293)")
    c.execute("INSERT INTO balances (balance, account) VALUES (92000, 1293)")
    c.execute("INSERT INTO balances (balance, account) VALUES (22000, 10277)")
    c.execute("INSERT INTO balances (balance, account) VALUES (1300, 13333)")
    c.execute("INSERT INTO balances (balance, account) VALUES (81200, 11210)")
    c.execute("INSERT INTO balances (balance, account) VALUES (73300, 7466)")
    c.execute("INSERT INTO balances (balance, account) VALUES (60000, 4137)")

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
        c.execute("UPDATE balances SET balance=? WHERE account=?", (dest_balance[0] + amt, dest))

    conn.commit()
    c.close()
    conn.close()

def main():
    init()
    server_address = ("", 9999)
    httpd = HTTPServer(server_address, FBSRequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()

