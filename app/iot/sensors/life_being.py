import asyncio
from datetime import datetime
import random
from .base import BaseSensor, SensorReading

class LifeBeingSensor(BaseSensor):
    def __init__(self, sensor_id: str, room_id: str):
        super().__init__(sensor_id, room_id)
        self.sensitivity = 0.85
        self._last_motion = False

    async def get_reading(self) -> SensorReading:
        # Simulate motion detection
        motion_detected = random.random() < self.sensitivity
        
        # Add some persistence to motion detection
        if self._last_motion:
            motion_detected = random.random() < 0.8
        
        self._last_motion = motion_detected

        return SensorReading(
            timestamp=datetime.now(),
            sensor_id=self.sensor_id,
            room_id=self.room_id,
            value={
                "presence_state": "present" if motion_detected else "absent",
                "sensitivity": self.sensitivity,
                "online_status": self.status
            }
        ) 