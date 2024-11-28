import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db, Hotel, Floor, Room, Device
from app.scaling_config import ScalingConfig

def setup_demo_environment():
    """Initialize the demo environment with sample data"""
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create demo hotel
        hotel = Hotel(name="Demo Hotel")
        db.session.add(hotel)
        db.session.flush()
        
        # Create 3 floors
        for floor_num in range(1, 4):
            floor = Floor(hotel_id=hotel.id, number=str(floor_num))
            db.session.add(floor)
            db.session.flush()
            
            # Create 5 rooms per floor
            for room_num in range(1, 6):
                room = Room(
                    floor_id=floor.id,
                    room_number=f"{floor_num}{room_num:02d}"
                )
                db.session.add(room)
                db.session.flush()
                
                # Add devices to each room
                devices = [
                    Device(room_id=room.id, device_type="ac", status="off"),
                    Device(room_id=room.id, device_type="lights", status="off"),
                    Device(room_id=room.id, device_type="temperature_sensor", status="off"),
                    Device(room_id=room.id, device_type="humidity_sensor", status="off"),
                    Device(room_id=room.id, device_type="motion_sensor", status="off")
                ]
                db.session.add_all(devices)
                db.session.flush() 