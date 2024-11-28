from ..cloud_db import CloudDatabaseManager
from .. import db
import time
import schedule

def sync_databases():
    cloud_db = CloudDatabaseManager()
    with db.session() as local_session:
        cloud_db.sync_sensor_logs(local_session)

def start_sync_scheduler():
    # Schedule sync every 5 minutes
    schedule.every(5).minutes.do(sync_databases)
    
    while True:
        schedule.run_pending()
        time.sleep(60) 