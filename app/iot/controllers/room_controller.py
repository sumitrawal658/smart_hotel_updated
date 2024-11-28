from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime

@dataclass
class DeviceState:
    is_on: bool
    settings: Dict

class RoomController:
    def __init__(self, controller_id: str, room_id: str):
        self.controller_id = controller_id
        self.room_id = room_id
        self.ac_state = DeviceState(False, {"temperature": 24.0, "mode": "auto"})
        self.light_state = DeviceState(False, {"brightness": 100})

    async def control_ac(self, command: str, settings: Optional[Dict] = None) -> Dict:
        self.ac_state.is_on = command == "on"
        if settings:
            self.ac_state.settings.update(settings)
        return self._get_ac_state()

    async def control_lights(self, command: str, settings: Optional[Dict] = None) -> Dict:
        self.light_state.is_on = command == "on"
        if settings:
            self.light_state.settings.update(settings)
        return self._get_light_state()

    def _get_ac_state(self) -> Dict:
        return {
            "is_on": self.ac_state.is_on,
            "settings": self.ac_state.settings,
            "timestamp": datetime.now().isoformat()
        }

    def _get_light_state(self) -> Dict:
        return {
            "is_on": self.light_state.is_on,
            "settings": self.light_state.settings,
            "timestamp": datetime.now().isoformat()
        } 