from typing import Dict, Optional
from dataclasses import dataclass
import openai
from .energy_manager import EnergyManager
from .guest_interface import SmartRoomController

@dataclass
class GuestPreferences:
    preferred_temperature: float
    preferred_lighting: str
    language: str
    notifications_enabled: bool

class SmartRoomAssistant:
    def __init__(self, room_id: str, openai_api_key: str):
        self.room_id = room_id
        self.controller = SmartRoomController(room_id)
        self.energy_manager = EnergyManager()
        openai.api_key = openai_api_key
        self.guest_preferences = {}

    async def process_request(self, user_message: str, guest_id: str) -> Dict:
        # Get current room status
        room_status = self.controller.get_realtime_data()
        
        # Build context for LLM
        system_prompt = self._build_system_prompt(room_status, guest_id)
        
        # Get AI response
        response = await openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=150
        )

        # Extract and execute actions
        actions = self._parse_actions(response.choices[0].message.content)
        if actions:
            await self._execute_actions(actions)

        return {
            "response": response.choices[0].message.content,
            "room_status": room_status,
            "actions_taken": actions
        }

    def _build_system_prompt(self, room_status: Dict, guest_id: str) -> str:
        prefs = self.guest_preferences.get(guest_id, GuestPreferences(23.0, "medium", "en", True))
        
        return f"""You are a smart hotel room assistant. Current room conditions:
- Temperature: {room_status['iaq']['temperature']}°C
- Humidity: {room_status['iaq']['humidity']}%
- CO2 Level: {room_status['iaq']['co2']} ppm
- Guest preferences: {prefs.preferred_temperature}°C, {prefs.preferred_lighting} lighting

You can control the room's AC, lights, and provide room status information.
Please respond naturally and execute requested actions."""

    async def _execute_actions(self, actions: Dict) -> None:
        for device, command in actions.items():
            await self.controller.control_device(device, command['action'], command.get('parameters'))

    def update_guest_preferences(self, guest_id: str, preferences: Dict) -> None:
        self.guest_preferences[guest_id] = GuestPreferences(
            preferred_temperature=preferences.get('temperature', 23.0),
            preferred_lighting=preferences.get('lighting', 'medium'),
            language=preferences.get('language', 'en'),
            notifications_enabled=preferences.get('notifications', True)
        ) 