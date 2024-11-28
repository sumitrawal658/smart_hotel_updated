#!/bin/bash

# Start services
docker-compose up -d
flask run &

# Setup demo data
python scripts/setup_demo_data.py

# Start simulation
python scripts/start_demo_simulation.py &

# Run interactive demo
python scripts/run_demo.py

# Cleanup
trap 'kill $(jobs -p)' EXIT 