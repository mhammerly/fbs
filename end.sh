# reset all the clients
pkill fbs_traffic.sh
echo "" > /root/rolling_code
ssh root@10.1.1.2 pkill fbs_traffic.sh
ssh root@10.1.1.2 'echo "" > /root/rolling_code'
ssh root@10.1.1.3 pkill fbs_traffic.sh
ssh root@10.1.1.3 'echo "" > /root/rolling_code'
ssh root@10.1.1.4 pkill fbs_traffic.sh
ssh root@10.1.1.4 'echo "" > /root/rolling_code'
ssh root@10.1.1.5 pkill fbs_traffic.sh
ssh root@10.1.1.5 'echo "" > /root/rolling_code'

# reset the server
ssh root@10.1.1.5 pkill python3

