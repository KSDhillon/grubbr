from kafka import KafkaConsumer
consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
for message in consumer:
    print(json.loads((message.value).decode('utf-8')))
