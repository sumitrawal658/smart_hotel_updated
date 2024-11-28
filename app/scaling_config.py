class ScalingConfig:
    def __init__(self):
        self.simulation_limits = {
            'max_hotels': 100,
            'max_floors_per_hotel': 50,
            'max_rooms_per_floor': 30
        }
        
        self.resource_limits = {
            'sensors_per_room': 2,  # Life Being and IAQ sensors
            'data_retention_days': 30,
            'max_concurrent_simulations': 1000
        }

def get_resource_requirements(hotels, floors_per_hotel, rooms_per_floor):
    total_rooms = hotels * floors_per_hotel * rooms_per_floor
    return {
        'estimated_memory_mb': total_rooms * 10,  # Approximate memory per room
        'estimated_storage_gb': (total_rooms * 0.1 * 30),  # Monthly storage
        'recommended_cpu_cores': max(2, total_rooms // 100)  # Min 2 cores
    } 