from typing import Dict
from .sensors.life_being import LifeBeingSensor
from .sensors.iaq import IAQSensor
from .controllers.room_controller import RoomController

class RoomManager:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.life_being_sensor = LifeBeingSensor(f"lbs_{room_id}", room_id)
        self.iaq_sensor = IAQSensor(f"iaq_{room_id}", room_id)
        self.controller = RoomController(f"ctrl_{room_id}", room_id)

    async def get_room_status(self) -> Dict:
        life_being_reading = await self.life_being_sensor.get_reading()
        iaq_reading = await self.iaq_sensor.get_reading()
        
        return {
            "life_being": life_being_reading.value,
            "iaq": iaq_reading.value,
            "devices": {
                "ac": self.controller._get_ac_state(),
                "lights": self.controller._get_light_state()
            }
        } 