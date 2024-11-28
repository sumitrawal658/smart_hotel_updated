
```markdown:wiki/Demo_Guide.md
# Smart Hotel System Demo

## 1. System Setup (CLI Demo)
```bash
# Initialize the system with sample data
python -m flask cli setup --hotels 2 --floors 5 --rooms 10
```
**Screenshot 1:** Show CLI output confirming creation
(Reference: `app/cli.py`, lines 11-37)

## 2. Real-time Sensor Monitoring

### Start Simulation
```bash
# Start simulation for Hotel 1
curl -X POST http://localhost:5000/simulate/hotel/1
```
**Video Segment 1 (30s):** Show real-time sensor data updates
(Reference: `app/routes.py`, lines 280-292)

### Monitor Room Status
**Screenshot 2:** Dashboard showing:
- Life Being sensor status
- IAQ readings (CO2, temperature, humidity)
- Device states
(Reference: `app/iot_simulator.py`, lines 3-22)

## 3. Smart Room Control

### Device Control Demo
**Video Segment 2 (45s):** Show:
1. Adjusting AC temperature
2. Controlling lights
3. Managing TV settings
(Reference: `app/smart_features/guest_interface.py`, lines 29-49)

### Voice Commands
**Video Segment 3 (30s):** Demonstrate:
1. "Turn on the lights"
2. "Set temperature to 23 degrees"
3. "What's the room's air quality?"
(Reference: `app/llm_interface/chatbot.py`, lines 8-67)

## 4. Analytics Dashboard

### Historical Data View
**Screenshot 3:** Show graphs of:
- Occupancy patterns
- Energy consumption
- Air quality trends
(Reference: `app/routes.py`, lines 173-177)

### Real-time Monitoring
**Video Segment 4 (30s):** Display:
1. Live sensor updates
2. Occupancy changes
3. Alert notifications
(Reference: `app/smart_features/routes.py`, lines 11-23)

## 5. Management Interface

### Hotel Overview
**Screenshot 4:** Show:
- All hotels
- Floor status
- Room occupancy
(Reference: `app/routes.py`, lines 22-35)

### System Health
**Screenshot 5:** Display:
- Active simulations
- Sensor status
- System resources
(Reference: `app/scaling_config.py`, lines 1-13)

## Demo Environment Setup

1. Start backend services:
```bash
docker-compose up -d
flask run
```

2. Initialize demo data:
```bash
python setup_demo_data.py
```

3. Start simulation:
```bash
python start_demo_simulation.py
```

## Key Features to Highlight

1. **Real-time Responsiveness**
- Show sensor data updates
- Demonstrate device control latency
- Display occupancy detection

2. **Smart Automation**
- Temperature adjustment based on occupancy
- Lighting control based on time
- Air quality management

3. **User Experience**
- Voice command responsiveness
- Mobile interface adaptability
- Alert notifications

4. **System Scalability**
- Multiple hotel management
- Concurrent room simulations
- Data synchronization

## Demo Preparation Checklist

- [ ] Set up demo environment
- [ ] Initialize sample data
- [ ] Test all features
- [ ] Prepare backup system
- [ ] Check network connectivity
- [ ] Verify sensor simulations
```

This demo guide provides a structured approach to showcase your system's capabilities. The suggested screenshots and video segments will demonstrate both technical functionality and user experience. Each section maps directly to your implementation and highlights key features.

Would you like me to provide more specific details for any section or help create the demo scripts?