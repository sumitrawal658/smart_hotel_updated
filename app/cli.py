import click
from app import create_app
from app.simulation_manager import SimulationManager
from app.models import Hotel, Floor, Room, db

@click.group()
def cli():
    """Smart Hotel Simulation CLI"""
    pass

@cli.command()
@click.option('--hotels', default=1, help='Number of hotels to simulate')
@click.option('--floors', default=5, help='Number of floors per hotel')
@click.option('--rooms', default=10, help='Number of rooms per floor')
def setup(hotels, floors, rooms):
    """Set up simulation infrastructure"""
    app = create_app()
    with app.app_context():
        for h in range(hotels):
            hotel = Hotel(name=f"Hotel_{h+1}")
            db.session.add(hotel)
            db.session.flush()
            
            for f in range(floors):
                floor = Floor(hotel_id=hotel.id, number=f+1)
                db.session.add(floor)
                db.session.flush()
                
                for r in range(rooms):
                    room = Room(
                        floor_id=floor.id,
                        room_number=f"{f+1}{r+1:02d}"
                    )
                    db.session.add(room)
        
        db.session.commit()
        click.echo(f"Created {hotels} hotels with {floors} floors each and {rooms} rooms per floor")

@cli.command()
@click.argument('hotel_id', type=int)
def start(hotel_id):
    """Start simulation for a hotel"""
    app = create_app()
    with app.app_context():
        sim_manager = SimulationManager()
        rooms_count = sim_manager.start_simulation(hotel_id=hotel_id)
        click.echo(f"Started simulation for {rooms_count} rooms in hotel {hotel_id}")

if __name__ == '__main__':
    cli() 