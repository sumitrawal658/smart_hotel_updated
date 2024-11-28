from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from .models import SensorLog, Base
import aiohttp

class CloudDatabaseManager:
    def __init__(self):
        # Get cloud database credentials from environment variables
        db_user = os.getenv('CLOUD_DB_USER', 'default_user')
        db_password = os.getenv('CLOUD_DB_PASSWORD', 'default_password')
        db_host = os.getenv('CLOUD_DB_HOST', 'your-rds-instance.region.rds.amazonaws.com')
        db_name = os.getenv('CLOUD_DB_NAME', 'smart_hotel')

        # Create SQLAlchemy engine for cloud database
        self.engine = create_engine(
            f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
        )
        
        # Create session factory
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def sync_sensor_logs(self, local_session):
        """Sync local sensor logs to cloud database"""
        try:
            # Get all unsynchronized logs (you might want to add a 'synced' column to SensorLog)
            local_logs = local_session.query(SensorLog).filter_by(synced=False).all()
            
            for log in local_logs:
                cloud_log = SensorLog(
                    room_id=log.room_id,
                    sensor_type=log.sensor_type,
                    data=log.data,
                    timestamp=log.timestamp
                )
                self.session.add(cloud_log)
                log.synced = True
            
            # Commit changes to both databases
            self.session.commit()
            local_session.commit()
            return True
        except Exception as e:
            print(f"Error syncing to cloud database: {e}")
            self.session.rollback()
            return False

    def get_cloud_data(self, room_id=None, start_date=None, end_date=None):
        """Retrieve data from cloud database with optional filters"""
        query = self.session.query(SensorLog)
        
        if room_id:
            query = query.filter(SensorLog.room_id == room_id)
        if start_date:
            query = query.filter(SensorLog.timestamp >= start_date)
        if end_date:
            query = query.filter(SensorLog.timestamp <= end_date)
            
        return query.all() 

    async def sync_device_async(self, device):
        """Async method to sync device data to cloud"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.cloud_api_base}/devices/{device.id}/sync"
            payload = {
                'device_id': device.id,
                'room_id': device.room_id,
                'status': device.status,
                'configuration': device.configuration,
                'last_ping': device.last_ping.isoformat()
            }
            async with session.post(url, json=payload) as response:
                return await response.json()