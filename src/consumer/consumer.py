from kafka import KafkaConsumer
import psycopg2
import json
import time

#Connect to PostgreSQL
conn = psycopg2.connect(
    host = "localhost",
    database = "battery_data",
    user = "postgres",
    password = "password"
)

cur = conn.cursor()

# Create the postgreSQL database table
cur.execute("""
CREATE TABLE IF NOT EXISTS battery_readings (
    id SERIAL PRIMARY KEY,
    battery_id INT,
    voltage REAL,
    current REAL,
    temperature REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# Connect to Kafka
consumer = KafkaConsumer(
    'battery_data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest',  # start from oldest message
    enable_auto_commit=True
)

print("Starting Kafka consumer...")

for message in consumer:
    data = message.value
    cur.execute("""
        INSERT INTO battery_readings (battery_id, voltage, current, temperature)
        VALUES (%s, %s, %s, %s)
    """, (data['battery_id'], data['voltage'], data['current'], data['temperature']))
    conn.commit()
    print(f"Saved to DB: {data}")
