import streamlit as st
import mysql.connector

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="atharva",
    database="ElectricityBillingSystem"
)

mycursor = mydb.cursor()

# In the global scope, initialize the flag using st.session_state
if 'flag' not in st.session_state:
    st.session_state.flag = 0

# CRUD Operations for Customers
def create_customer(customer_name, address, contact_number):
    sql = "INSERT INTO Customer (customer_name, address, contact_number) VALUES (%s, %s, %s)"
    val = (customer_name, address, contact_number)
    mycursor.execute(sql, val)
    mydb.commit()

def read_customers():
    mycursor.execute("SELECT * FROM Customer")
    return mycursor.fetchall()

def update_customer(customer_id, new_customer_name, new_address, new_contact_number):
    sql = "UPDATE Customer SET customer_name = %s, address = %s, contact_number = %s WHERE customer_id = %s"
    val = (new_customer_name, new_address, new_contact_number, customer_id)
    mycursor.execute(sql, val)
    mydb.commit()

def delete_customer(customer_id):
    # Check if there are related meters for the customer
    mycursor.execute("SELECT * FROM Meter WHERE customer_id = %s", (customer_id,))
    related_meters = mycursor.fetchall()

    if related_meters:
        # Delete related readings for each meter
        for meter in related_meters:
            mycursor.execute("DELETE FROM Reading WHERE meter_id = %s", (meter[0],))

        # Delete the meters
        mycursor.execute("DELETE FROM Meter WHERE customer_id = %s", (customer_id,))
    
    # Delete the customer
    sql = "DELETE FROM Customer WHERE customer_id = %s"
    val = (customer_id,)
    mycursor.execute(sql, val)
    mydb.commit()

# CRUD Operations for Meters
def create_meter(customer_id, meter_number, meter_type, installation_date):
    sql = "INSERT INTO Meter (customer_id, meter_number, meter_type, installation_date) VALUES (%s, %s, %s, %s)"
    val = (customer_id, meter_number, meter_type, installation_date)
    mycursor.execute(sql, val)
    mydb.commit()

def read_meters():
    mycursor.execute("SELECT * FROM Meter")
    return mycursor.fetchall()

def update_meter(meter_id, new_meter_number, new_meter_type, new_installation_date):
    sql = "UPDATE Meter SET meter_number = %s, meter_type = %s, installation_date = %s WHERE meter_id = %s"
    val = (new_meter_number, new_meter_type, new_installation_date, meter_id)
    mycursor.execute(sql, val)
    mydb.commit()

def delete_meter(meter_id):
    sql = "DELETE FROM Meter WHERE meter_id = %s"
    val = (meter_id,)
    mycursor.execute(sql, val)
    mydb.commit()

# CRUD Operations for Readings
def create_reading(meter_id, reading_date, units_consumed):
    # Check if the meter_id exists in the Meter table
    mycursor.execute("SELECT * FROM Meter WHERE meter_id = %s", (meter_id,))
    meter = mycursor.fetchone()

    if meter is not None:
        # Meter exists, proceed with creating the reading
        sql = "INSERT INTO Reading (meter_id, reading_date, units_consumed) VALUES (%s, %s, %s)"
        val = (meter_id, reading_date, units_consumed)
        mycursor.execute(sql, val)
        mydb.commit()
        st.write("Reading created successfully!")
    else:
        st.write(f"Error: Meter with ID {meter_id} does not exist.")

def read_readings():
    mycursor.execute("SELECT * FROM Reading")
    return mycursor.fetchall()

# User registration function
def register_user(name, email, password):
    sql = "INSERT INTO User (full_name, username, email, password) VALUES (%s, %s, %s, %s)"
    val = (name, email, email, password)
    mycursor.execute(sql, val)
    mydb.commit()

# User login function
def login_user(email, password):
    sql = "SELECT * FROM User WHERE email = %s AND password = %s"
    val = (email, password)
    mycursor.execute(sql, val)
    user = mycursor.fetchone()
    if user is not None:
        st.session_state.flag = 1  # Update flag in st.session_state
    return user

# User logout function
def logout_user():
    st.session_state.flag = 0  # Reset flag in st.session_state

st.title("Electricity Billing Management System")

# Display only "Register" and "Login" options if not logged in
if st.session_state.flag == 0:
    options = st.sidebar.selectbox("Select an Operation", ("Register", "Login"))
else:
    # Display all options after successful login
    options = st.sidebar.selectbox("Select an Operation", (
        "Create Customer", "Read Customers", "Update Customer", "Delete Customer",
        "Create Meter", "Read Meters", "Update Meter", "Delete Meter",
        "Create Reading", "Read Readings", "Logout"
    ))

# CRUD Operations for Customers
if options == "Create Customer":
    st.subheader("Create Customer")
    customer_name = st.text_input("Enter Customer Name:")
    address = st.text_input("Enter Address:")
    contact_number = st.text_input("Enter Contact Number:")

    if st.button("Create"):
        create_customer(customer_name, address, contact_number)
        st.write("Customer created successfully!")

if options == "Read Customers":
    st.subheader("Read Customers")
    customers = read_customers()

    if customers:
        st.write("List of Customers:")
        for customer in customers:
            st.write(f"Customer ID: {customer[0]}, Name: {customer[1]}, Address: {customer[2]}, Contact Number: {customer[3]}")
    else:
        st.write("No customers found.")

if options == "Update Customer":
    st.subheader("Update Customer")
    customer_id = st.text_input("Enter Customer ID:")
    new_customer_name = st.text_input("Enter New Customer Name:")
    new_address = st.text_input("Enter New Address:")
    new_contact_number = st.text_input("Enter New Contact Number:")

    if st.button("Update"):
        update_customer(customer_id, new_customer_name, new_address, new_contact_number)
        st.write("Customer updated successfully!")

if options == "Delete Customer":
    st.subheader("Delete Customer")
    customer_id = st.text_input("Enter Customer ID:")

    if st.button("Delete"):
        delete_customer(customer_id)
        st.write("Customer deleted successfully!")

# CRUD Operations for Meters
if options == "Create Meter":
    st.subheader("Create Meter")
    customer_id = st.text_input("Enter Customer ID:")
    meter_number = st.text_input("Enter Meter Number:")
    meter_type = st.text_input("Enter Meter Type:")
    installation_date = st.date_input("Enter Installation Date:")

    if st.button("Create"):
        create_meter(customer_id, meter_number, meter_type, installation_date)
        st.write("Meter created successfully!")

if options == "Read Meters":
    st.subheader("Read Meters")
    meters = read_meters()

    if meters:
        st.write("List of Meters:")
        for meter in meters:
            st.write(f"Meter ID: {meter[0]}, Customer ID: {meter[1]}, Meter Number: {meter[2]}, Meter Type: {meter[3]}, Installation Date: {meter[4]}, Total Units Consumed: {meter[5]}")
    else:
        st.write("No meters found.")

if options == "Update Meter":
    st.subheader("Update Meter")
    meter_id = st.text_input("Enter Meter ID:")
    new_meter_number = st.text_input("Enter New Meter Number:")
    new_meter_type = st.text_input("Enter New Meter Type:")
    new_installation_date = st.date_input("Enter New Installation Date:")

    if st.button("Update"):
        update_meter(meter_id, new_meter_number, new_meter_type, new_installation_date)
        st.write("Meter updated successfully!")

if options == "Delete Meter":
    st.subheader("Delete Meter")
    meter_id = st.text_input("Enter Meter ID:")

    if st.button("Delete"):
        delete_meter(meter_id)
        st.write("Meter deleted successfully!")

# CRUD Operations for Readings
if options == "Create Reading":
    st.subheader("Create Reading")
    meter_id = st.text_input("Enter Meter ID:")
    reading_date = st.date_input("Enter Reading Date:")
    units_consumed = st.number_input("Enter Units Consumed:")

    if st.button("Create"):
        create_reading(meter_id, reading_date, units_consumed)

if options == "Read Readings":
    st.subheader("Read Readings")
    readings = read_readings()

    if readings:
        st.write("List of Readings:")
        for reading in readings:
            st.write(f"Reading ID: {reading[0]}, Meter ID: {reading[1]}, Reading Date: {reading[2]}, Units Consumed: {reading[3]}")
    else:
        st.write("No readings found.")

# User registration, login, and logout
if options == "Register":
    st.subheader("User Registration")
    name = st.text_input("Enter UserName")
    email = st.text_input("Enter Email")
    password = st.text_input("Enter Password", type="password")
    if st.button("Register"):
        register_user(name, email, password)
        st.write("Registration successful!")
        st.write("Now you can log in with your credentials")

if options == "Login":
    st.subheader("User Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.write(f"Welcome, {user[1]}!")
        else:
            st.write("Login failed. Please check your credentials")

if options == "Logout":
    logout_user()
    st.write("You have been logged out")

# Close the database connection
mydb.close()
