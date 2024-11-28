from datetime import datetime
import random
from .base import BaseSensor, SensorReading

class IAQSensor(BaseSensor):
    def __init__(self, sensor_id: str, room_id: str):
        super().__init__(sensor_id, room_id)
        self._last_readings = {
            "temperature": 23.0,
            "humidity": 45.0,
            "co2": 400,
            "noise": 35
        }

    async def get_reading(self) -> SensorReading:
        # Simulate gradual changes in environment
        self._last_readings["temperature"] += random.uniform(-0.5, 0.5)
        self._last_readings["humidity"] += random.uniform(-2, 2)
        self._last_readings["co2"] += random.uniform(-50, 50)
        self._last_readings["noise"] += random.uniform(-5, 5)

        # Keep values in realistic ranges
        self._last_readings["temperature"] = max(18, min(30, self._last_readings["temperature"]))
        self._last_readings["humidity"] = max(30, min(70, self._last_readings["humidity"]))
        self._last_readings["co2"] = max(350, min(2000, self._last_readings["co2"]))
        self._last_readings["noise"] = max(30, min(90, self._last_readings["noise"]))

        return SensorReading(
            timestamp=datetime.now(),
            sensor_id=self.sensor_id,
            room_id=self.room_id,
            value=self._last_readings.copy()
        ) 