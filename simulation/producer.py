import json
import time
from ensurepip import bootstrap

from kafka import KafkaProducer
from simulation.battery_pack import BatteryPack

producer = KafkaProducer(
    bootstrap_servers = "localhost:9092",
    value_serializer = lambda v: json.dumps(v).encode("utf-8")
)

def run():
    pack = BatteryPack("PACK_01", num_series=4, num_parallel=1)
    print("Starting battery Simulation - streaming data to Kafka...")

    while True:
        pack.update()
        reading = pack.get_reading()
        producer.send("battery.telemetry", value = reading)
        print(f"Sent | voltage={reading['pack_voltage']}V | state={reading['state']} | cycle={reading['cycle_count']}")
        time.sleep(1)

if __name__ == "__main__":
    run()
