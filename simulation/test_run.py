from simulation.battery_cell import BatteryCell

cell = BatteryCell("CELL_001")

print("Simulating 10 second discharge at 10A...\n")

for i in range(3200):
    cell.update(current=-10.0)
    reading = cell.get_reading()
    print(
        f"t={i + 1}s | voltage={reading['voltage']}V | soc={reading['soc']} | temp={reading['temperature']}°C | current={reading['current']}A"
    )
