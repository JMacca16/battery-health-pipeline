import json
from kafka import KafkaConsumer
from db.connection import SessionLocal
from db.models import PackReading, CellReading
import datetime

consumer = KafkaConsumer(
    "battery.telemetry",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    group_id="battery-pipeline-consumer",
    auto_offset_reset="earliest"
)

def run():
    print("Consumer started - listening for messages...")
    session = SessionLocal()

    for message in consumer:
        data = message.value

        pack_reading = PackReading(
            timestamp=datetime.datetime.utcnow(),
            pack_id=data["pack_id"],
            cycle_count=data["cycle_count"],
            state=data["state"],
            pack_voltage=data["pack_voltage"],
            pack_current=data["pack_current"]
        )
        session.add(pack_reading)

        for cell in data["cells"]:
            cell_reading = CellReading(
                timestamp=datetime.datetime.utcnow(),
                pack_id=data["pack_id"],
                battery_id=cell["battery_id"],
                voltage=cell["voltage"],
                current=cell["current"],
                temperature=cell["temperature"],
                soc=cell["soc"],
                soh=cell["soh"],
                nominal_capacity=cell["nominal_capacity"],
                available_capacity=cell["available capacity"],
                internal_resistance=cell["internal resistance"],
                cycle_count=cell["cycle count"],
                state=cell["state"],
                is_anomaly=cell["anomaly"]
            )
            session.add(cell_reading)

        session.commit()
        print(f"Written to DB | pack={data['pack_id']} | voltage={data['pack_voltage']}V")

if __name__ == "__main__":
    run()
