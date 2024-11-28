from app import create_app
from app.simulation_manager import SimulationManager
from app.models import Hotel
import time

def run_demo_simulation():
    """Start simulation for demo hotel"""
    app = create_app()
    sim_manager = SimulationManager(max_workers=15)
    
    with app.app_context():
        hotel = Hotel.query.first()
        if not hotel:
            print("Error: No hotel found. Run setup_demo_data.py first.")
            return
        
        print(f"Starting simulation for hotel: {hotel.name}")
        rooms_count = sim_manager.start_simulation(hotel_id=hotel.id)
        print(f"Simulating {rooms_count} rooms...")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping simulation...")
            sim_manager.stop_all_simulations()
            print("Simulation stopped.")

if __name__ == "__main__":
    run_demo_simulation() 