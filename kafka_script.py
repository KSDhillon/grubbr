from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

es = Elasticsearch(['es'])
consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
for message in consumer:
    o = json.loads((message.value).decode('utf-8'))
    es.index(index='listing_index', doc_type='listing', id=o['id'], body=o)
    es.indices.refresh(index='listing_index')
