import cloud_sync
import asyncio

class CloudConfig:
    CLOUD_API_BASE = 'https://api.smarthotel.cloud'
    CLOUD_SYNC_INTERVAL = 300  # 5 minutes
    CLOUD_BATCH_SIZE = 100
    CLOUD_RETRY_ATTEMPTS = 3
    
    # AWS Configuration
    AWS_REGION = 'us-west-2'
    AWS_IOT_ENDPOINT = 'your-iot-endpoint.iot.region.amazonaws.com'
    
    # Azure Configuration (if using Azure)
    AZURE_IOT_HUB_CONNECTION_STRING = 'your-connection-string'

async def start_cloud_sync(room_id):
    while True:
        await cloud_sync.sync_room_data(room_id)
        await asyncio.sleep(CloudConfig.CLOUD_SYNC_INTERVAL)
