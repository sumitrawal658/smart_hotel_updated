Here’s a structured approach for creating API and technical documentation for your Smart Hotel project:

---

### API & Technical Documentation

#### 1. **Endpoints**

Provide a brief description of each endpoint, along with the HTTP methods and request/response format. Here’s an example structure:

1. **`GET /`**  
   - **Description**: Returns a welcome message for the Smart Hotel API.
   - **HTTP Method**: `GET`
   - **Response**:
     ```json
     {
       "message": "Welcome to the Smart Hotel API!"
     }
     ```

2. **`GET /logs/<int:room_id>/latest`**  
   - **Description**: Retrieves the latest sensor data for a specified room.
   - **HTTP Method**: `GET`
   - **Parameters**:
     - `room_id` (int): ID of the room.
   - **Response**:
     ```json
     {
       "room_id": 101,
       "latest_data": {
         "iaq": { "co2": 880, "temperature": 26.5, ... },
         "life_being": { "online_status": "offline", ... }
       }
     }
     ```

3. **`GET /logs/<int:room_id>/average`**  
   - **Description**: Returns average sensor values for a specified room over a time period.
   - **HTTP Method**: `GET`
   - **Parameters**:
     - `room_id` (int): ID of the room.
     - `start_time` (string, ISO format): Start time of the period.
     - `end_time` (string, ISO format): End time of the period.
   - **Response**:
     ```json
     {
       "room_id": 101,
       "average_co2": 720.5,
       "average_temperature": 24.3
     }
     ```

4. **`POST /simulate/<int:room_id>/data`**  
   - **Description**: Simulates sensor data for a specific room and logs it.
   - **HTTP Method**: `POST`
   - **Parameters**:
     - `room_id` (int): ID of the room.
     - JSON body with simulated sensor data.
   - **Response**:
     ```json
     {
       "status": "Data logged successfully for room 101."
     }
     ```

5. **`POST /alerts`**  
   - **Description**: Endpoint to manually trigger an alert (for testing).
   - **HTTP Method**: `POST`
   - **Parameters**:
     - JSON body with alert details.
   - **Response**:
     ```json
     {
       "status": "Alert triggered successfully."
     }
     ```

6. **`POST /control/<int:room_id>`**  
   - **Description**: Controls IoT devices in a specific room.
   - **HTTP Method**: `POST`
   - **Parameters**:
     - `room_id` (int): ID of the room.
     - JSON body specifying control instructions (e.g., turn on/off devices).
   - **Response**:
     ```json
     {
       "status": "Device control successful for room 101."
     }
     ```

---

#### 2. **Database Models**

Provide a brief documentation for each model used in the application. Here’s an example for key models:

1. **`SensorLog`**
   - **Description**: Stores sensor data for each room over time.
   - **Fields**:
     - `id` (int, primary key): Unique identifier for the log entry.
     - `room_id` (int, foreign key): ID of the room.
     - `sensor_type` (string): Type of sensor data (e.g., temperature).
     - `data` (JSON): Sensor data in JSON format.
     - `timestamp` (datetime): Time the data was recorded.

2. **`Room`**
   - **Description**: Represents a hotel room.
   - **Fields**:
     - `id` (int, primary key): Unique identifier for the room.
     - `hotel_id` (int, foreign key): ID of the hotel.
     - `room_number` (string): Room number.

3. **`User`**
   - **Description**: Stores user information.
   - **Fields**:
     - `id` (int, primary key): Unique identifier for the user.
     - `username` (string): Username for login.
     - `password_hash` (string): Hashed password for security.
     - `role_id` (int, foreign key): Role assigned to the user (e.g., guest, staff).

4. **`Role`**
   - **Description**: Defines different roles for the system.
   - **Fields**:
     - `id` (int, primary key): Unique identifier for the role.
     - `name` (string): Role name (e.g., guest, staff, admin).
     - `permissions` (JSON): Permissions associated with the role.

---

#### 3. **Permissions**

Define user roles and the permissions associated with each role for different endpoints:

1. **Guest**
   - **Access**: Limited to basic interactions with IoT devices and viewing sensor data.
   - **Allowed Endpoints**:
     - `GET /logs/<room_id>/latest`
     - `GET /logs/<room_id>/average`
     - `POST /control/<room_id>`

2. **Staff**
   - **Access**: Can view and control IoT devices across multiple rooms.
   - **Allowed Endpoints**:
     - All guest endpoints
     - `POST /alerts`
     - `POST /simulate/<room_id>/data`

3. **Admin**
   - **Access**: Full access to manage system settings and all data.
   - **Allowed Endpoints**:
     - All endpoints

Each endpoint can enforce these permissions by checking the user’s role before processing the request. For instance, use a decorator in Flask to verify the user’s role and restrict access accordingly.

---

### Event Streaming Endpoints

1. **Kafka Bootstrap Servers**
   - **Development**: `localhost:9092`
   - **Production**: `kafka:9092` (internal Docker network)

2. **Topics**
   - **iot_data**: Sensor data streaming
   - **occupancy_status**: Room occupancy updates

3. **Consumer Groups**
   - **data_logger_group**: Persistent storage of sensor data
   - **occupancy_detector_group**: Real-time occupancy analysis
   - **analytics_group**: Statistical analysis and reporting

---

