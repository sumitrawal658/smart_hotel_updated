-- Creating the Role Table
CREATE TABLE Role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) NOT NULL
);

-- Creating the User Table
CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES Role(id) ON DELETE SET NULL
);

-- Creating the Hotel Table
CREATE TABLE Hotel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100)
);

-- Creating the Floor Table
CREATE TABLE Floor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    number INT NOT NULL,
    hotel_id INT,
    FOREIGN KEY (hotel_id) REFERENCES Hotel(id) ON DELETE CASCADE
);

-- Creating the Room Table
CREATE TABLE Room (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_number VARCHAR(20) NOT NULL,
    floor_id INT,
    FOREIGN KEY (floor_id) REFERENCES Floor(id) ON DELETE CASCADE
);

-- Creating the SensorLog Table
CREATE TABLE SensorLog (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT,
    sensor_type VARCHAR(50) NOT NULL,
    data JSON,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES Room(id) ON DELETE CASCADE
);

-- Creating the RolePermissions Table (optional)
CREATE TABLE RolePermissions (
    role_id INT,
    permission VARCHAR(100) NOT NULL,
    FOREIGN KEY (role_id) REFERENCES Role(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission)
);
