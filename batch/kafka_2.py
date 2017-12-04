from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

consumer = KafkaConsumer('rec-topic', group_id='rec-indexer', bootstrap_servers=['kafka:9092'])
print("hello")
for access in consumer:
    o = json.loads((access.value).decode('utf-8'))
    for key in o:
        with open('/spark/log.txt', 'a') as f:
            f.write(key + "," + o[key] + "\n")
