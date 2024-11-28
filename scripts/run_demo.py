import click
import requests
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live
from datetime import datetime

console = Console()

class DemoRunner:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.room_id = None
    
    def show_sensor_data(self, room_id):
        """Display real-time sensor data"""
        url = f"{self.base_url}/rooms/{room_id}/smart/status"
        response = requests.get(url)
        data = response.json()
        
        table = Table(title=f"Room {room_id} - Live Sensor Data")
        table.add_column("Sensor")
        table.add_column("Value")
        
        if 'iaq' in data:
            for key, value in data['iaq'].items():
                table.add_row(key, str(value))
        
        console.clear 