from concurrent.futures import ThreadPoolExecutor
from .iot_simulator import simulate_sensor_data
from .event_stream import event_stream
from .models import Hotel, Floor, Room
from . import db
import time
import logging
from threading import Lock
from datetime import datetime

class SimulationManager:
    def __init__(self, max_workers=10):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.active_simulations = {}
        self.lock = Lock()
        self.logger = logging.getLogger(__name__)

    def simulate_room(self, room_id, interval=5):
        """Simulate a single room's sensor data"""
        while room_id in self.active_simulations:
            try:
                data = simulate_sensor_data(room_id)
                event_stream.publish_sensor_data(room_id, data)
                time.sleep(interval)
            except Exception as e:
                self.logger.error(f"Error simulating room {room_id}: {e}")

    def start_simulation(self, hotel_id=None, floor_id=None, room_id=None):
        """Start simulation for specified scope"""
        try:
            rooms_to_simulate = []

            if hotel_id:
                # Simulate entire hotel
                floors = Floor.query.filter_by(hotel_id=hotel_id).all()
                for floor in floors:
                    rooms = Room.query.filter_by(floor_id=floor.id).all()
                    rooms_to_simulate.extend(rooms)
            elif floor_id:
                # Simulate single floor
                rooms = Room.query.filter_by(floor_id=floor_id).all()
                rooms_to_simulate.extend(rooms)
            elif room_id:
                # Simulate single room
                room = Room.query.get(room_id)
                if room:
                    rooms_to_simulate.append(room)

            with self.lock:
                for room in rooms_to_simulate:
                    if room.id not in self.active_simulations:
                        self.active_simulations[room.id] = True
                        self.executor.submit(self.simulate_room, room.id)

            return len(rooms_to_simulate)

        except Exception as e:
            self.logger.error(f"Error starting simulation: {e}")
            return 0

    def stop_simulation(self, hotel_id=None, floor_id=None, room_id=None):
        """Stop simulation for specified scope"""
        try:
            rooms_to_stop = []

            if hotel_id:
                floors = Floor.query.filter_by(hotel_id=hotel_id).all()
                for floor in floors:
                    rooms = Room.query.filter_by(floor_id=floor.id).all()
                    rooms_to_stop.extend(rooms)
            elif floor_id:
                rooms = Room.query.filter_by(floor_id=floor_id).all()
                rooms_to_stop.extend(rooms)
            elif room_id:
                room = Room.query.get(room_id)
                if room:
                    rooms_to_stop.append(room)

            with self.lock:
                for room in rooms_to_stop:
                    self.active_simulations.pop(room.id, None)

            return len(rooms_to_stop)

        except Exception as e:
            self.logger.error(f"Error stopping simulation: {e}")
            return 0