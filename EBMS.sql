-- Create the database
CREATE DATABASE IF NOT EXISTS ElectricityBillingSystem;
USE ElectricityBillingSystem;

-- Create the Customer table
CREATE TABLE IF NOT EXISTS Customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    contact_number VARCHAR(15) NOT NULL,
    UNIQUE KEY unique_contact_number (contact_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create the Meter table
CREATE TABLE IF NOT EXISTS Meter (
    meter_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    meter_number VARCHAR(20) NOT NULL,
    meter_type VARCHAR(50) NOT NULL,
    installation_date DATE NOT NULL,
    total_units_consumed INT DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    UNIQUE KEY unique_meter_number (meter_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create the Reading table
CREATE TABLE IF NOT EXISTS Reading (
    reading_id INT AUTO_INCREMENT PRIMARY KEY,
    meter_id INT,
    reading_date DATE NOT NULL,
    units_consumed INT NOT NULL,
    FOREIGN KEY (meter_id) REFERENCES Meter(meter_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create a function to calculate total units consumed between two dates
DELIMITER //
CREATE FUNCTION CalculateTotalUnitsConsumed(meterID INT, startDate DATE, endDate DATE) RETURNS INT
BEGIN
    DECLARE totalUnits INT;
    SELECT SUM(units_consumed) INTO totalUnits
    FROM Reading
    WHERE meter_id = meterID AND reading_date BETWEEN startDate AND endDate;
    RETURN COALESCE(totalUnits, 0);
END //
DELIMITER ;

-- Create a trigger to update the total units consumed when a new reading is inserted
DELIMITER //
CREATE TRIGGER UpdateTotalUnits AFTER INSERT ON Reading
FOR EACH ROW
BEGIN
    DECLARE totalUnits INT;
    SELECT SUM(units_consumed) INTO totalUnits
    FROM Reading
    WHERE meter_id = NEW.meter_id;

    UPDATE Meter
    SET total_units_consumed = totalUnits
    WHERE meter_id = NEW.meter_id;
END //
DELIMITER ;

-- Create the User table
CREATE TABLE IF NOT EXISTS User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
