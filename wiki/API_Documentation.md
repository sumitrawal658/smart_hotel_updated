# Smart Hotel System API Documentation

## Core API Endpoints

### Hotel Management
#### Get All Hotels
```http
GET /hotels
```
**Response:** List of hotels with their IDs and names
(Reference: `app/routes.py`, lines 22-25)

#### Get Hotel Floors
```http
GET /hotels/{hotel_id}/floors
```
**Response:** List of floors for specified hotel
(Reference: `app/routes.py`, lines 27-30)

### Room Management
#### Get Floor Rooms
```http
GET /floors/{floor_id}/rooms
```
**Response:** List of rooms on specified floor
(Reference: `app/routes.py`, lines 32-35)

### Smart Room Features

#### Get Room Status
```http
GET /rooms/{room_id}/smart/status
```
**Authentication:** Required
**Permissions:** VIEW_ROOM
**Response:** Current room sensor data and device states
(Reference: `app/smart_features/routes.py`, lines 11-23)

#### Get Room History
```http
GET /rooms/{room_id}/smart/history
```
**Parameters:**
- `hours` (query, optional): Number of hours of history (default: 24)

**Response:** Historical sensor data and events
(Reference: `app/smart_features/routes.py`, lines 25-31)

#### Control Room Device
```http
POST /rooms/{room_id}/smart/control
```
**Request Body:**
```json
{
    "device_type": "string",  // "ac", "tv", or "lights"
    "command": "string",
    "parameters": {
        // Optional device-specific parameters
    }
}
```
(Reference: `app/smart_features/routes.py`, lines 33-49)

### Simulation API

#### Start Hotel Simulation
```http
POST /simulate/hotel/{hotel_id}
```
**Response:** Number of rooms being simulated
(Reference: `app/routes.py`, lines 280-292)

#### Start Floor Simulation
```http
POST /simulate/floor/{floor_id}
```
**Response:** Number of rooms being simulated
(Reference: `app/routes.py`, lines 294-306)

### Analytics API

#### Get Weekly Summary
```http
GET /analytics/weekly_summary
```
**Response:** Statistical summary of hotel operations
(Reference: `app/routes.py`, lines 173-177)

### Threshold Management

#### Manage Room Thresholds
```http
GET/PUT /rooms/{room_id}/thresholds
```
**PUT Request Body:**
```json
{
    "co2_threshold": float,
    "temperature_threshold": float
}
```
(Reference: `app/routes.py`, lines 179-192)

## Data Models

### Sensor Data Structure
```json
{
    "life_being": {
        "presence_state": "present|absent",
        "sensitivity": float,
        "online_status": "online|offline"
    },
    "iaq": {
        "noise": int,        // dB
        "co2": int,         // ppm
        "pm25": int,        // µg/m³
        "humidity": float,  // %
        "temperature": float, // °C
        "illuminance": int   // lux
    }
}
```
(Reference: `app/iot_simulator.py`, lines 1-30)

## Authentication

All protected endpoints require JWT authentication. Include the token in the Authorization header:
```http
Authorization: Bearer <token>
```

## Error Responses

Standard error format:
```json
{
    "error": "Error message description",
    "status": 400|401|403|404|500
}
```

## Rate Limiting

- Maximum 1000 requests per minute per IP
- Simulation endpoints: 10 requests per minute per IP

## Scaling Considerations

System is designed to handle:
- Up to 100 hotels
- 50 floors per hotel
- 30 rooms per floor
- 2 sensors per room
(Reference: `app/scaling_config.py`, lines 1-13)

## WebSocket Events

Real-time updates are available through WebSocket connections:
```javascript
ws://<base_url>/ws/room/{room_id}
```

### Event Types:
1. sensor_update
2. device_state_change
3. occupancy_change
4. alert_notification

## AI Integration

Natural language processing endpoints for guest interaction:
```http
POST /rooms/{room_id}/smart/chat
```
(Reference: `app/llm_interface/chatbot.py`, lines 8-67)

## Database Schema

The system uses PostgreSQL with the following key tables:
- hotels
- floors
- rooms
- sensor_data
- sensor_logs
(Reference: `app/models.py`, lines 1-38)

## Event Streaming Architecture

### Kafka Topics and Message Formats

1. **iot_data**
   - **Purpose**: Real-time IoT sensor data streaming
   - **Producer**: IoT Simulator
   - **Consumers**: Data Logger, Occupancy Detector
   - **Message Format**:
     ```json
     {
       "room_id": "integer",
       "data": {
         "life_being": {
           "presence_state": "string",
           "sensitivity": "float",
           "online_status": "string"
         },
         "iaq": {
           "temperature": "float",
           "humidity": "float",
           "co2": "integer",
           "noise": "integer"
         }
       },
       "timestamp": "float"
     }
     ```

2. **occupancy_status**
   - **Purpose**: Room occupancy state changes
   - **Producer**: Occupancy Detector
   - **Consumers**: Room Controller, Analytics
   - **Message Format**:
     ```json
     {
       "room_id": "integer",
       "is_occupied": "boolean",
       "occupancy_score": "float",
       "timestamp": "float"
     }
     ```