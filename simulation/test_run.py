from battery_pack import BatteryPack

pack = BatteryPack("PACK_01", num_series=4, num_parallel=1)

for i in range(10000):
    pack.update()
    if i % 100 == 0:
        reading = pack.get_reading()
        print(f"t={i}s | voltage={reading['pack_voltage']}V | state={reading['state']} | cycles={reading['cycle_count']}")
