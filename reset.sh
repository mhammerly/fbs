#!/bin/bash

echo "Resetting..."
{
# reset the server
ssh root@10.1.1.5 pkill python3
ssh root@10.1.1.5 "cp /root/fbs/fbs.db /root/fbs/db_backups/$(date '+%d-%m.%H:%M:%S').db"
ssh root@10.1.1.5 python3 /root/fbs/server.py &

sleep 3

# reset all the clients
# pkill fbs_traffic.sh
# echo "" > /root/rolling_code
# /root/fbs_traffic.sh
ssh root@10.1.1.2 pkill fbs_traffic.sh
sleep 1
ssh root@10.1.1.2 'echo "" > /root/rolling_code'
sleep 1
ssh root@10.1.1.2 "/root/fbs_traffic.sh" &
sleep 1
ssh root@10.1.1.3 pkill fbs_traffic.sh
sleep 1
ssh root@10.1.1.3 'echo "" > /root/rolling_code'
sleep 1
ssh root@10.1.1.3 "/root/fbs_traffic.sh" &
sleep 1
ssh root@10.1.1.4 pkill fbs_traffic.sh
sleep 1
ssh root@10.1.1.4 'echo "" > /root/rolling_code'
sleep 1
ssh root@10.1.1.4 "/root/fbs_traffic.sh" &
sleep 1
ssh root@10.1.1.5 pkill fbs_traffic.sh
sleep 1
ssh root@10.1.1.5 'echo "" > /root/rolling_code'
sleep 1
ssh root@10.1.1.5 "/root/fbs_traffic.sh" &
sleep 1
} &

