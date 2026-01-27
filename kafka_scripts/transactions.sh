tail -n +2 Dataset/Transactions.csv | \
while read line
do
  echo "$line"
  sleep 0.5
done | kafka-console-producer.sh --broker-list 127.0.0.1:9092 --topic transactions --producer-property acks=all

