from simulation.battery_cell import BatteryCell, BatteryState

class BatteryPack:
    def __init__(self, pack_id, num_series, num_parallel, config = None):
        self.pack_id = pack_id
        self.num_series = num_series
        self.num_parallel = num_parallel

        # Create all the cells in the pack
        self.cells = [
            BatteryCell(f"{pack_id}_CELL_{i+1}", config = config)
            for i in range(num_series * num_parallel)
        ]

        # Pack level state
        self.cycle_count = 0
        self.state = BatteryState.CHARGING

    def get_pack_voltage(self):
        return sum(cell.voltage for cell in self.cells[:self.num_series])

    def get_pack_current(self):
        return self.cells[0].steady_state_current * self.num_parallel

    def update(self, dt=1.0):
        # Determine current based on state
        if self.state == BatteryState.CHARGING:
            current = 50.0  # 1C charge
        else:
            current = -50.0  # 1C discharge

        # Update all cells
        for cell in self.cells:
            cell.update(current=current, dt=dt)

        # Check switching conditions
        if self.state == BatteryState.CHARGING:
            if self.cells[0].soc >= 0.99:
                self.state = BatteryState.DISCHARGING
                self.cycle_count += 1
                print(f"Cycle {self.cycle_count} complete - switching to discharge")

        elif self.state == BatteryState.DISCHARGING:
            if self.cells[0].soc <= 0.20:
                self.state = BatteryState.CHARGING
                print(f"Switching to charge")

    def get_reading(self):
        return {
            "pack_id": self.pack_id,
            "cycle_count": self.cycle_count,
            "state": self.state.value,
            "pack_voltage": round(self.get_pack_voltage(), 4),
            "pack_current": round(self.get_pack_current(), 4),
            "cells": [cell.get_reading() for cell in self.cells]
        }
