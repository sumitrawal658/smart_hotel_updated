import random

def simulate_life_being_sensor():
    """Simulate data for the Life Being Sensor."""
    return {
        'presence_state': random.choice(['present', 'absent']),
        'sensitivity': random.uniform(0.1, 1.0),
        'online_status': random.choice(['online', 'offline'])
    }

def simulate_iaq_sensor():
    """Simulate data for the IAQ Sensor."""
    return {
        'noise': random.randint(30, 70),   # in dB
        'co2': random.randint(400, 1000),  # ppm
        'pm25': random.randint(10, 40),    # µg/m³
        'humidity': random.uniform(30.0, 50.0),  # %
        'temperature': random.uniform(18.0, 28.0),  # °C
        'illuminance': random.randint(100, 500),    # lux
        'online_status': 'online',
        'device_status': 'active'
    }

def simulate_sensor_data(room_id):
    """Combine data from both sensors for a room."""
    return {
        'room_id': room_id,
        'life_being': simulate_life_being_sensor(),
        'iaq': simulate_iaq_sensor()
    }
