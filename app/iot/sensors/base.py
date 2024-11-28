from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SensorReading:
    timestamp: datetime
    sensor_id: str
    room_id: str
    value: dict
    status: str = "online"

class BaseSensor(ABC):
    def __init__(self, sensor_id: str, room_id: str):
        self.sensor_id = sensor_id
        self.room_id = room_id
        self.status = "online"

    @abstractmethod
    async def get_reading(self) -> SensorReading:
        pass

    def get_status(self) -> str:
        return self.status 