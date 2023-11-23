# DBMS_Project_EBMS


**Project Description: Electricity Billing Management System**

**Objective:**
The Electricity Billing Management System is designed to streamline and automate the processes related to electricity billing. It provides functionalities for managing customer information, meters, readings, and user authentication.

**Components:**

1. **MySQL Database Schema:**
   - **Database Creation:**
     - A MySQL database named `ElectricityBillingSystem` is created to store all the relevant information.
   
   - **Customer Table:**
     - Stores customer details, including a unique contact number.
   
   - **Meter Table:**
     - Manages information about electricity meters, including the customer they are associated with, meter number, type, installation date, and total units consumed.
   
   - **Reading Table:**
     - Keeps track of meter readings, recording the meter ID, reading date, and units consumed.
   
   - **Function: CalculateTotalUnitsConsumed:**
     - A MySQL function that calculates the total units consumed by a meter between two specified dates.

   - **Trigger: UpdateTotalUnits:**
     - A MySQL trigger that updates the total units consumed in the Meter table when a new reading is inserted.

   - **User Table:**
     - Stores user information for system access, including full name, username, email, and password.

2. **Streamlit Application (Python):**
   - A web-based user interface is created using Streamlit, providing the following functionalities:
   
   - **User Authentication:**
     - Users can register, log in, and log out. Passwords are securely stored in the User table.
   
   - **Customer Management:**
     - CRUD (Create, Read, Update, Delete) operations for managing customer information.
   
   - **Meter Management:**
     - CRUD operations for managing meter information, including creating, reading, updating, and deleting meters.
   
   - **Reading Management:**
     - CRUD operations for managing meter readings, allowing users to input new readings and view existing ones.
   
   - **User Interface:**
     - A user-friendly interface provides a sidebar for selecting operations, and each operation is presented with relevant input fields and buttons.

**How to Run:**
1. Set up a MySQL database and execute the provided SQL script to create the necessary schema, tables, function, trigger, and user table.
2. Run the provided Python code using a Streamlit-compatible environment.
3. Use the Streamlit web application to perform various operations such as customer management, meter management, reading management, and user authentication.

**Note:** Ensure that the MySQL server is running and accessible from the Streamlit application. Adjust MySQL connection parameters in the Python code as needed.
