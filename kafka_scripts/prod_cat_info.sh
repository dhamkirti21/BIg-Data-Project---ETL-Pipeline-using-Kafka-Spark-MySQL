tail -n +2 Dataset/prod_cat_info.csv | \
while read line
do
  echo "$line"
  sleep 0.5
done | kafka-console-producer.sh --broker-list 127.0.0.1:9092 --topic prod_cat_info --producer-property acks=all

