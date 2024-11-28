class OccupancyDataCollector:
    def __init__(self):
        self.features = []
        self.ground_truth = []
        
    def collect_training_data(self, sensor_data, actual_occupancy):
        """Collect labeled data for model improvement"""
        features = {
            'presence_state': sensor_data['life_being']['presence_state'],
            'sensitivity': sensor_data['life_being']['sensitivity'],
            'co2_level': sensor_data['iaq']['co2'],
            'noise_level': sensor_data['iaq']['noise'],
            'time_of_day': self._extract_time_features(sensor_data['timestamp']),
            'actual_occupancy': actual_occupancy
        }
        
        self.features.append(features) 