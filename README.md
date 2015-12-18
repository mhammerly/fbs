# overview
this software was written to be a target for a MITM attack via ARP poisoning.
the scenario is that this terrible bank software will be running on a network
with some automated requests being thrown around to emulate transactions, and
students are to intercept communications between the server and other clients
to redirect transactions. the database is cleared and restored to an initial
state every time the server script is launched, which includes five accounts
with balances and five without; money will be passed between accounts with
money and students will redirect transactions into their groups' own account.  

this application does support ssl if the `use_https` variable is set to True at
the top of each python file. see the setup section below for more details.  

there is a rolling code mechanism that will prevent replay attacks from
happening. when a valid transaction from some source is sent to the server, its
transaction number is incremented in the database, and when the client receives
its 200 response, it increments the transaction number stored in a local file.
currently the rolling code is dependent only on the source and transaction
number as it's mostly a protection against accidental replays; it is thus not
hard to forge at all so i hope you can trust your students lol  

it depends on sqlite and was written against python 3.4.3. it was built with
one particular class and one particular network in mind, but modification
should be fairly easy.

# winning
the original solution to this project uses `ettercap` to ARP poison the network
and hijack traffic between clients and the server.

# setup
#### network setup
the simplest way to set up a network for this would be to connect a router to
the internet, and then to connect all your scenario computers to the router.
the router can forward port 22 to one of the computers on the network, which
you then instruct students to connect to over ssh (the 'endpoint'). install
python3 and sqlite3 on each machine on the network; on Debian-based systems you
can do this with `sudo apt-get install python3 sqlite3`. if using ettercap,
install that as well. then create accounts for each group of students that will
be doing the assignment on the endpoint with `useradd`. ettercap requires sudo,
so ensure sudo is installed and that each account is in the sudoers group (check
the group with `visudo` and add to the group with `usermod -aG <group> <user>`)

###### installing packages with no internet connection
the way that the network was originally set up included one machine that was
WAN-accessible, and we attached to it a router and four other machines. this
machine then had two network interfaces active, and was the only machine on
the LAN that had internet access. since we needed to install python3 and
sqlite3 on other machines, we had to do a dance with our package manager.
first, from the machine without internet access (the 'target'), we ran
`apt-get --print-uris --yes install <your package here> | grep ^\' | cut -d\' -f2 >downloads.list`
to create a list of dependencies for our desired package. next, we copied
that downloads.list file to our internet-connected machine with `scp`. we
then fetched installation packages for these dependencies with the command:
`mkdir ~/tmp && cd ~/tmp && wget --input-file ~/downloads.list`. we then
copy the new `~/tmp` folder to our target with `scp -r`, and on the target
machine we run `dpkg -i ~/tmp/*`.

#### software setup
first, you have to modify `client.py`, `server.py`, and `get_balance.py` to
reflect how your network is set up.
###### client.py
in `client.py` the `accts` dictionary should contain a mapping of each IP in
your network to an account in your database. the `ifconfig` command run from
`os.popen()` should be changed to use the approriate network interface for
your network. `server_host` should contain the IP address of the computer that
`server.py` will be running on.
###### server.py
create an empty sqlite3 database somewhere (`sqlite3 fbs.db ""`) and put its
location in the `db` variable. modify the `init()` function in any way you
please to change the initial database state.
###### get\_balance.py
the `accts` dictionary should include a mapping of linux user account names to
account numbers in your database. `server_host` should contain the IP address
of the computer that `server.py` will be running on.

#### running the software
put `server.py` on one machine on the network. put `client.py` and `fbs_traffic.sh`
on other machines on the network. put `get_balance.py` in the home directory of
each group's user account on the endpoint. put `reset.sh` and `end.sh` somewhere safe.
edit all of the .sh files to use correct filepaths and hosts. finally, to start
the server and the simulated traffic, run the `reset.sh` script. `end.sh` is
used to stop everything.

#### https
set the `use_https` variable to True at the top of each file to enable ssl. it
counts on there being a cert at `/root/cert.pem` and a key at `/root/key.pem`
which you can generate and self-sign with this command:
`openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 30`  

