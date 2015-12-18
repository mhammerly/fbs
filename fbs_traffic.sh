#! /bin/bash

python3 client.py 10.1.1.2 400
python3 client.py 10.1.1.4 200
sleep 1
python3 client.py 10.1.1.3 500
sleep 3
python3 client.py 10.1.1.4 500
sleep 2
# python3 client.py 10.1.1.1 1100
sleep 4
python3 client.py 10.1.1.5 100
sleep 2
/root/fbs_traffic.sh &

