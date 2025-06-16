import json
import os

from time import sleep
from pymongo import MongoClient
from confluent_kafka import Consumer, KafkaException


user = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASSWORD")

MONGO_URI = f"mongodb+srv://{user}:{password}@cluster0.zbgwwti.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)

# 指定資料庫與 collection
db = client['kafka_db']
collection = db['kafka_collection']

def insert_to_db(data):
    try:
        # 將資料插入 collection
        collection.insert_one({
            'application_id': data['application_id'],
            'agent_id': data['agent_id'],
            'customer_name': data['customer_name'],
            'plan': data['plan'],
            'timestamp': data['timestamp'],
        })
        print("[DB] Inserted document")
    except Exception as err:
        print(f"[DB ERROR] {err}")

consumer = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'notifier-group-test',
    'auto.offset.reset': 'earliest'
})

# Wait for topic to exist
for _ in range(10):
    md = consumer.list_topics(timeout=5.0)
    if 'insurance_applications' in md.topics:
        print("[Consumer] Topic ready.")
        break
    print("[Consumer] Waiting for topic...")
    sleep(2)
else:
    raise Exception("Topic 'insurance_applications' not found after retries.")

consumer.subscribe(['insurance_applications'])

print("[Consumer] Listening for events...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        data = json.loads(msg.value().decode('utf-8'))
        print(f"[Consumer] Received: {data}")
        if data.get("init"):
            continue
        insert_to_db(data)
except KeyboardInterrupt:
    print("Stopping consumer...")
finally:
    consumer.close()
