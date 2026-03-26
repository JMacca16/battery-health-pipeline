import random
import time
from enum import Enum


class BatteryState(Enum):
    IDLE = "idle"
    CHARGING = "charging"
    DISCHARGING = "discharging"
    FAULT = "fault"


class BatteryCellConfig:
    def __init__(self):
        self.capacity_ah = 50.0
        self.r0 = 0.01
        self.r1 = 0.02
        self.c1 = 2000.0
        self.v_max = 4.2
        self.v_min = 2.5
        self.temp_nominal = 25.0


class BatteryCell:
    def __init__(self, cell_id, config=None):
        self.cell_id = cell_id
        if config:
            self.config = config
        else:
            self.config = BatteryCellConfig()

        # State Variables
        self.soc = 1.0
        self.soh = 1.0
        self.v_rc = 0.0
        self.temperature = self.config.temp_nominal
        self.state = BatteryState.IDLE
        self.cycle_count = 0

        # Flags
        self.is_anomaly = False

    def get_ocv(self):
        soc = self.soc
        return self.config.v_min + (self.config.v_max - self.config.v_min) * (
            (3.5 * soc**3) - (6.5 * soc**2) + (4.0 * soc)
        )

    def update(self, current, dt=1.0):
        # current is positive for charging, negative for discharging.
        # Time step is 1.0 seconds by default
        self.current = current

        # update battery state
        if current > 0.1:
            self.state = BatteryState.CHARGING
        elif current < -0.1:
            self.state = BatteryState.DISCHARGING
        else:
            self.state = BatteryState.IDLE

        # Update current across RC pair
        dv_rc = (current / self.config.c1) - (
            self.v_rc / (self.config.r1 * self.config.c1)
        )
        self.v_rc += dv_rc * dt

        # Calculate terminal voltage
        voltage = self.get_ocv() - (current * self.config.r0) - self.v_rc

        # Update SOC from current
        self.soc += (current * dt) / (self.config.capacity_ah * 3600)
        self.soc = max(
            0.0, min(1.0, self.soc)
        )  # Check that the SOC is in bounds (0.0 - 1.0)

        # Calculate temperature
        heating_power = (current**2) * self.config.r0
        self.temperature += (heating_power * 0.01) - (
            0.005 * (self.temperature - self.config.temp_nominal)
        )

        # Add gaussian sensor noise
        voltage += random.gauss(0, 0.005)
        self.temperature += random.gauss(0, 0.1)

    def get_reading(self):
        return {
            "timestamp": time.time(),
            "battery_id": self.cell_id,
            "voltage": round(
                (self.get_ocv() - (self.current * self.config.r0) - self.v_rc), 4
            ),
            "current": round(self.current, 4),
            "temperature": round(self.temperature, 4),
            "soc": round(self.soc, 4),
            "soh": round(self.soh, 4),
            "nominal_capacity": self.config.capacity_ah,
            "available capacity": round((self.config.capacity_ah * self.soc), 4),
            "internal resistance": round(self.config.r0, 4),
            "cycle count": self.cycle_count,
            "state": self.state.value,
            "anomaly": self.is_anomaly,
        }
