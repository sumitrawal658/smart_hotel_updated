from datetime import datetime, timedelta
import json
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

class RoomAnalytics:
    def __init__(self):
        self.usage_data = {}

    def log_room_status(self, room_id: str, data: dict):
        timestamp = datetime.now().isoformat()
        if room_id not in self.usage_data:
            self.usage_data[room_id] = []
        
        self.usage_data[room_id].append({
            "timestamp": timestamp,
            "temperature": data.get("temperature"),
            "occupancy": data.get("occupancy"),
            "co2_level": data.get("co2"),
            "humidity": data.get("humidity")
        })

    def get_room_statistics(self, room_id: str, hours: int = 24):
        if room_id not in self.usage_data:
            return None
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_data = [
            entry for entry in self.usage_data[room_id] 
            if datetime.fromisoformat(entry["timestamp"]) > cutoff_time
        ]
        
        return {
            "occupancy_rate": self._calculate_occupancy_rate(recent_data),
            "avg_temperature": self._calculate_average("temperature", recent_data),
            "avg_co2": self._calculate_average("co2_level", recent_data)
        } 

class AdvancedRoomAnalytics(RoomAnalytics):
    def __init__(self):
        super().__init__()
        self.scaler = StandardScaler()
        self.anomaly_detector = IsolationForest(contamination=0.1)
        
    def detect_anomalies(self, room_id: str, hours: int = 24):
        """Detect unusual patterns in room usage"""
        data = self.get_room_statistics(room_id, hours)
        if not data:
            return None
            
        features = np.array([[
            data['avg_temperature'],
            data['avg_co2'],
            data['occupancy_rate']
        ]])
        
        scaled_features = self.scaler.fit_transform(features)
        anomalies = self.anomaly_detector.fit_predict(scaled_features)
        
        return anomalies[0] == -1  # True if anomaly detected

    def predict_peak_hours(self, room_id: str):
        """Predict likely busy periods based on historical data"""
        if room_id not in self.usage_data:
            return None
            
        hourly_occupancy = self._calculate_hourly_occupancy(room_id)
        return {
            hour: rate for hour, rate in hourly_occupancy.items()
            if rate > 0.7  # 70% occupancy threshold
        }