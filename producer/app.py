import json
import random
import time
from datetime import datetime

from confluent_kafka import Producer

producer = Producer({'bootstrap.servers': 'kafka:9092'})
producer.produce("insurance_applications", key="init", value=json.dumps({"init": True}))

def generate_event():
    return {
        "application_id": f"AP{random.randint(100000,999999)}",
        "agent_id": f"AG{random.randint(1000,9999)}",
        "customer_name": random.choice(["John", "Alice", "Bob", "Mary"]),
        "plan": random.choice(["Whole Life", "Term Life", "Health Plus"]),
        "timestamp": datetime.utcnow().isoformat()
    }

while True:
    event = generate_event()
    producer.produce('insurance_applications', json.dumps(event).encode('utf-8'))
    print(f"[Producer] Sent event: {event}")
    producer.flush()
    time.sleep(3)

