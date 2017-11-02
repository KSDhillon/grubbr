from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

es = Elasticsearch(['es'])
fixtures = [
    {
        'name': 'pasta',
        'price': 10,
        'portions': 5,
        'desciption': 'cheesy',
        'id': 1
    },
    {
        'name': 'hamburger',
        'price': 10,
        'portions': 5,
        'desciption': 'meaty',
        'id': 2
    },
    {
        'name': 'lasanga',
        'price': 10,
        'portions': 5,
        'desciption': 'silent G',
        'id': 3
    },
]
for fix in fixtures:
    es.index(index='listing_index', doc_type='listing', id=fix['id'], body=fix)
es.indices.refresh(index='listing_index')

consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
for message in consumer:
    o = json.loads((message.value).decode('utf-8'))
    es.index(index='listing_index', doc_type='listing', id=o['id'], body=o)
    es.indices.refresh(index='listing_index')
