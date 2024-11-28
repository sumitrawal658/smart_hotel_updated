from typing import Dict, Optional
import asyncio
from datetime import datetime, time

class ContextAwareController:
    def __init__(self, controller_id: str, room_id: str):
        self.controller_id = controller_id
        self.room_id = room_id
        self.scene_presets = {
            "morning": {
                "lights": {"brightness": 80, "temperature": 5000},  # Cooler light
                "ac": {"temperature": 23.5, "mode": "auto"}
            },
            "evening": {
                "lights": {"brightness": 60, "temperature": 2700},  # Warmer light
                "ac": {"temperature": 24.5, "mode": "auto"}
            },
            "night": {
                "lights": {"brightness": 20, "temperature": 2000},  # Very warm
                "ac": {"temperature": 25.0, "mode": "auto"}
            }
        }
        
    async def apply_context_scene(self, time_of_day: time, 
                                occupancy: bool, 
                                outdoor_temp: float) -> Dict:
        """Apply context-appropriate scene"""
        if not occupancy:
            return await self.apply_energy_saving_mode()
            
        hour = time_of_day.hour
        if 6 <= hour < 10:
            scene = "morning"
        elif 18 <= hour < 22:
            scene = "evening"
        else:
            scene = "night"
            
        return await self.apply_scene(scene, outdoor_temp)
        
    async def apply_scene(self, scene: str, outdoor_temp: float) -> Dict:
        """Apply a predefined scene with outdoor temperature compensation"""
        if scene not in self.scene_presets:
            return {"error": "Invalid scene"}
            
        settings = self.scene_presets[scene].copy()
        
        # Adjust AC temperature based on outdoor temperature
        temp_diff = outdoor_temp - settings["ac"]["temperature"]
        if abs(temp_diff) > 10:
            settings["ac"]["temperature"] += 0.5 * (1 if temp_diff > 0 else -1)
            
        return settings 