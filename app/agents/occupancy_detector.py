class OccupancyDetector:
    def __init__(self):
        self.weights = {
            'presence': 0.5,
            'co2': 0.3,
            'noise': 0.2
        }
        self.thresholds = {
            'co2_baseline': 400,
            'noise_baseline': 40,
            'occupancy': 0.7
        }
        
    def process_message(self, message):
        """Process sensor data to determine room occupancy"""
        try:
            sensor_data = message['data']
            life_being_data = sensor_data['life_being']
            iaq_data = sensor_data['iaq']

            # Check presence state
            is_present = life_being_data['presence_state'] == 'present'
            sensitivity = life_being_data['sensitivity']

            # Check environmental indicators
            co2_level = iaq_data['co2']
            noise_level = iaq_data['noise']

            # Determine occupancy based on multiple factors
            occupancy_score, features = self._calculate_occupancy_score(
                is_present, sensitivity, co2_level, noise_level, sensor_data['timestamp']
            )

            return {
                'room_id': message['room_id'],
                'is_occupied': occupancy_score > self.thresholds['occupancy'],
                'occupancy_score': occupancy_score,
                'timestamp': message['timestamp']
            }
        except Exception as e:
            print(f"Error detecting occupancy: {e}")
            return None

    def _calculate_occupancy_score(self, is_present, sensitivity, co2_level, noise_level, timestamp):
        """Advanced occupancy scoring with dynamic weights"""
        features = {
            'presence': self._calculate_presence_score(is_present, sensitivity),
            'co2': self._calculate_co2_score(co2_level),
            'noise': self._calculate_noise_score(noise_level)
        }
        
        # Calculate weighted score
        score = sum(self.weights[k] * features[k] for k in features)
        
        # Add time-based adjustments
        score = self._apply_temporal_adjustments(score, timestamp)
        
        return score, features  # Return both for analysis

    def _calculate_presence_score(self, is_present, sensitivity):
        """Calculate presence score based on sensor data"""
        return 0.5 * sensitivity if is_present else 0.0

    def _calculate_co2_score(self, co2_level):
        """Calculate CO2 score based on sensor data"""
        if co2_level > self.thresholds['co2_baseline']:
            normalized_co2 = min((co2_level - self.thresholds['co2_baseline']) / 1000, 1.0)
            return 0.3 * normalized_co2
        else:
            return 0.0

    def _calculate_noise_score(self, noise_level):
        """Calculate noise score based on sensor data"""
        if noise_level > self.thresholds['noise_baseline']:
            normalized_noise = min((noise_level - self.thresholds['noise_baseline']) / 50, 1.0)
            return 0.2 * normalized_noise
        else:
            return 0.0

    def _apply_temporal_adjustments(self, score, timestamp):
        """Add time-based adjustments to the occupancy score"""
        # Implement time-based adjustments logic here
        return score