from app import app
from flask import session
from flask import jsonify
from flask import render_template,request, redirect, url_for
from app.models.user_model import connectionUser,drop_table_users,insert_users,RegisterUser,is_valid_password
from app.models.office_model import connectionOffice, insert_offices, get_all_offices,drop_office_table, update_office_coordinates,get_office_names,get_office_id_by_name 
from app.models.vehicle_model import createVehicleDatabase, insert_vehicles,drop_vehicle_table,get_filtered_vehicles
import sqlite3
import base64

app.config['SESSION_TYPE'] = 'filesystem'  # You can change this to other storage types

# Example route handling the update of office coordinates
@app.route('/update_coordinates', methods=['GET'])
def office_table_create_and_update():
    # Call the function to update office coordinates
    connectionOffice()
    update_office_coordinates()
    print("create offices 2!")     
    # Optionally, provide a response or redirect to another page
    return "Office coordinates updated successfully"


@app.route('/')
def home():
    drop_table_users()
    connectionUser()
    insert_users()

    drop_vehicle_table()
    createVehicleDatabase()
    insert_vehicles()

    drop_office_table()
    connectionOffice()
    insert_offices()
    office_names = get_office_names()     
    #insert_vehicles()  
    office_table_create_and_update()    
    return render_template('index.html',office_names=office_names)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')


@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Connect to the database
        connection = sqlite3.connect('database.sqlite')
        cursor = connection.cursor()

        # Check if the provided credentials are valid
        query = "SELECT * FROM users WHERE email = ? AND password = ?"
        result = cursor.execute(query, (email, password)).fetchone()

        # Close the database connection
        connection.close()

        if result:
            # Set the 'user_id' key in the session to indicate that the user is logged in
            session['user_id'] = result[0]
            session['user_name'] = result[1]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html', error=None)

@app.route('/register')
def register():
    connectionUser()
    return render_template('register.html')

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        surname = request.form.get('surname')
        password = request.form.get('password')
        country = request.form.get('country')
        city = request.form.get('city')
        
        # Validate password match
        password_check = request.form.get('password_check')
        if password != password_check:
            return render_template('register.html', error='Passwords do not match')
        
        if not is_valid_password(password):
            return render_template('register.html', error='Invalid password format')

        # Check if the email is already registered
        # You may want to implement this check using your own logic
        # Example: existing_user = check_if_user_exists(email)
        # if existing_user:
        #     return render_template('register.html', error='Email is already registered')

        # Call the RegisterUser method
        print("Email: " + email)
        RegisterUser(email, name, surname, password, country, city)

        return redirect(url_for('login'))

    return render_template('register.html', error=None)


@app.route('/get_offices', methods=['GET'])
def get_offices_data():
    offices = get_all_offices()
    print("get_offices!")
    return jsonify({'offices': offices})


@app.route('/filter_cars', methods=['POST'])
def filter_cars():
    selected_office = request.form.get('pickupOffice')
    cars = get_filtered_vehicles(selected_office)    
    decoded_cars = []
    for car in cars:
        decoded_image = base64.b64decode(car[9])
        decoded_cars.append(car[:9] + (decoded_image,) + car[10:])  # Replace the original image with the decoded image
    OfficeID = get_office_id_by_name(selected_office)
    session['office_id'] = OfficeID

    return render_template('result_page.html', cars=cars)

@app.route('/filter_cars_form', methods=['POST'])
def filter_cars_form():
    # Get filter parameters and OfficeID from the form submission
    selected_office_id = session.get('office_id', None)
    selected_car_type = request.form.get('carTypeFilter', default='all')
    selected_rent_sort = request.form.get('rentSortFilter', default='asc')
    selected_transmission = request.form.get('transmissionFilter', default='all')

    # Construct SQL query based on filter parameters and OfficeID
    query = """
        SELECT * FROM vehicles
        WHERE (OfficeID = ?)
        AND (CarType = ? OR ? = 'all')
        AND (Transmission = ? OR ? = 'all')
        ORDER BY DailyRentPrice {} NULLS LAST
    """.format('ASC' if selected_rent_sort == 'asc' else 'DESC')

    # Execute query and fetch results
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()
    result = cursor.execute(query, (selected_office_id, selected_car_type, selected_car_type, selected_transmission, selected_transmission)).fetchall()
    connection.close()

    # Render template with filtered cars
    return render_template('result_page.html', cars=result)
