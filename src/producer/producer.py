from kafka import KafkaProducer
import json
import time
import random

# Connect to Kafka broker
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'battery_data'

# Initialize battery states
batteries = {
    i: {
        "voltage": random.uniform(3.7, 4.2),
        "current": 0.0,
        "temperature": random.uniform(25, 30)
    }
    for i in range(1, 11)
}

print("Starting stateful battery data producer...")

while True:
    for battery_id, state in batteries.items():
        # Gradual drift for realism
        state["voltage"] += random.uniform(-0.01, 0.01)
        state["voltage"] = max(3.0, min(4.2, state["voltage"]))  # clamp voltage

        state["current"] = random.uniform(-2, 2)

        state["temperature"] += random.uniform(-0.2, 0.2)
        state["temperature"] = max(20, min(45, state["temperature"]))  # clamp temp

        data = {"battery_id": battery_id, **state}
        producer.send(topic, data)
        print(f"Sent: {data}")

    time.sleep(2)
