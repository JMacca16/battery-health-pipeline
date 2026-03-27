from simulation.battery_cell import BatteryCell

cell = BatteryCell("CELL_001")

print("Simulating 10 second discharge at 10A...\n")


cell = BatteryCell("CELL_001")
for i in range(10):
    if i == 5:
        cell.inject_anomaly("internal short")
    cell.update(current=-10.0)
    reading = cell.get_reading()
    print(f"t={i+1}s | voltage={reading['voltage']}V | temp={reading['temperature']}°C | anomaly={reading['anomaly']}")
