from ..models import SensorLog, Device, Room, Floor, Hotel
from ..cloud_db import CloudDatabaseManager
import asyncio
import aiohttp

class CloudSyncService:
    def __init__(self):
        self.cloud_db = CloudDatabaseManager()
        
    async def sync_device_data(self, device_id):
        """Sync device data to cloud in real-time"""
        device = Device.query.get(device_id)
        if not device:
            return False
            
        try:
            # Sync to cloud database
            await self.cloud_db.sync_device_async(device)
            return True
        except Exception as e:
            print(f"Error syncing device {device_id}: {e}")
            return False
            
    async def sync_room_data(self, room_id):
        """Sync all devices and sensors in a room"""
        devices = Device.query.filter_by(room_id=room_id).all()
        tasks = [self.sync_device_data(device.id) for device in devices]
        await asyncio.gather(*tasks) 