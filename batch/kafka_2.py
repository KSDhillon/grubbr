from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

consumer = KafkaConsumer('rec-topic', group_id='rec-indexer', bootstrap_servers=['kafka:9092'])
for access in consumer:
    o = json.loads((access.value).decode('utf-8'))
    with open('/app/data/workfile', 'r') as f:
