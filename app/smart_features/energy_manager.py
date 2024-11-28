from dataclasses import dataclass
from typing import Dict
from datetime import datetime, time
import os
from openai import AzureOpenAI

@dataclass
class RoomEnvironment:
    temperature: float
    occupancy: bool
    ac_status: bool
    lights_status: bool
    last_motion_time: datetime
    iaq_data: Dict

class EnergyManager:
    def __init__(self):
        self.occupied_temp_range = (23.0, 25.0)  # Comfort range when occupied
        self.unoccupied_temp_range = (26.0, 27.0)  # Energy saving range when empty
        self.motion_timeout = 20  # Minutes to wait before entering energy saving mode
        self.rooms: Dict[str, RoomEnvironment] = {}

        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_KEY")
        assistant_id = os.getenv("AZURE_OPENAI_ASSISTANT_ID")

        self.client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,
            api_version="2024-05-01-preview"
        )

        self.thread = self.client.beta.threads.create()

    def update_room_status(self, room_id: str, sensor_data: Dict):
        current_time = datetime.now()
        
        if room_id not in self.rooms:
            self.rooms[room_id] = RoomEnvironment(
                temperature=sensor_data['iaq']['temperature'],
                occupancy=sensor_data['life_being']['presence_state'] == 'present',
                ac_status=False,
                lights_status=False,
                last_motion_time=current_time,
                iaq_data=sensor_data['iaq']
            )
        else:
            room = self.rooms[room_id]
            room.temperature = sensor_data['iaq']['temperature']
            room.iaq_data = sensor_data['iaq']
            
            if sensor_data['life_being']['presence_state'] == 'present':
                room.last_motion_time = current_time
                room.occupancy = True
            else:
                # Check if room has been empty long enough to enter energy saving mode
                minutes_since_motion = (current_time - room.last_motion_time).total_seconds() / 60
                room.occupancy = minutes_since_motion < self.motion_timeout
        
        return self._optimize_energy(room_id)

    def _optimize_energy(self, room_id: str) -> Dict:
        room = self.rooms[room_id]
        actions = {}

        if room.occupancy:
            # Occupied room - maintain comfort settings
            if room.temperature < self.occupied_temp_range[0]:
                actions['ac'] = {'status': 'on', 'mode': 'heat', 'temperature': self.occupied_temp_range[0]}
            elif room.temperature > self.occupied_temp_range[1]:
                actions['ac'] = {'status': 'on', 'mode': 'cool', 'temperature': self.occupied_temp_range[1]}
            else:
                actions['ac'] = {'status': 'off'}
            
            # Keep lights on if CO2 levels indicate occupancy
            actions['lights'] = {'status': 'on'} if room.iaq_data['co2'] > 600 else {'status': 'off'}
        
        else:
            # Unoccupied room - energy saving mode
            if room.temperature < self.unoccupied_temp_range[0]:
                actions['ac'] = {'status': 'on', 'mode': 'heat', 'temperature': self.unoccupied_temp_range[0]}
            elif room.temperature > self.unoccupied_temp_range[1]:
                actions['ac'] = {'status': 'on', 'mode': 'cool', 'temperature': self.unoccupied_temp_range[1]}
            else:
                actions['ac'] = {'status': 'off'}
            
            actions['lights'] = {'status': 'off'}

        # Update room state
        room.ac_status = actions['ac']['status'] == 'on'
        room.lights_status = actions['lights']['status'] == 'on'

        return actions

    def ask_assistant(self, question: str) -> str:
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=question
        )

        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=os.getenv("AZURE_OPENAI_ASSISTANT_ID")
        )

        while run.status in ["queued", "in_progress", "cancelling"]:
            time.sleep(1)
            run = self.client.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=run.id)

        if run.status == "completed":
            messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
            for message in messages.data:
                if message.role == "assistant":
                    return message.content[0].text.value
        elif run.status == "requires_action":
            pass
        else:
            raise Exception(run.status)