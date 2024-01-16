import sqlite3
import os
import base64


def createVehicleDatabase():
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicles  (
                   ID INTEGER PRIMARY KEY AUTOINCREMENT,  
                   Brand TEXT NOT NULL, 
                   Model TEXT NOT NULL, 
                   Transmission TEXT NOT NULL, 
                   FuelType TEXT NOT NULL, 
                   DepositPrice REAL, 
                   DailyRentPrice REAL, 
                   Mileage REAL,
                   Age REAL, 
                   Image BLOB,
                   CarType TEXT NOT NULL,
                   OfficeID INTEGER,
                   FOREIGN KEY (OfficeID) REFERENCES offices(ID))
            
        ''')    
    connection.commit()
    connection.close()


def insert_vehicles():
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()

    vehicles = [
        ('Renault', 'Clio', 'Manuel', 'Dizel/Benzin', 2500, 1914.18, 1000, 21, 'Renault_Clio.jpg', 'EKONOMİK'),
        ('Fiat', 'Egea', 'Manuel', 'Dizel/Benzin', 2500, 2071.03, 1000, 21, 'Fiat_Egea.jpg', 'EKONOMİK'),
        ('Renault', 'Clio AT', 'Otomatik', 'Dizel/Benzin', 2500, 2179.64, 1000, 21, 'Renault_Clio_AT.jpg', 'EKONOMİK'),
        ('Fiat', 'Egea', 'Otomatik', 'Hybrid/Benzin/Dizel', 2500, 2461.67, 1000, 21, 'Fiat_Egea_Hybrid.jpg', 'EKONOMİK'),
        ('Ford', 'Focus', 'Otomatik', 'Hybrid/Benzin/Dizel', 3000, 2929.08, 1000, 23, 'Ford_Focus.jpg', 'KONFOR'),
        ('Peugeot', '2008', 'Otomatik', 'Hybrid/Benzin/Dizel', 3000, 3049.19, 1000, 23, 'Peugeot_2008.jpg', 'KONFOR'),
        ('Ford', 'Kuga', 'Otomatik', 'Dizel/Benzin', 3500, 3731.12, 1000, 25, 'Ford_Kuga.jpg', 'PRESTİJ'),
        ('Audi', 'A3', 'Otomatik', 'Dizel/Benzin', 3500, 4342.39, 1000, 25, 'Audi_A3.jpg', 'PRESTİJ'),
        ('Volkswagen', 'Passat Variant', 'Otomatik', 'Dizel/Benzin', 3500, 4376.64, 1000, 25, 'VW_Passat_Variant.jpg', 'PRESTİJ'),
        ('Peugeot', '5008', 'Otomatik', 'Dizel', 5000, 5353.33, 1000, 27, 'Peugeot_5008.jpg', 'PREMIUM'),
        ('Volvo', 'XC40 Recharge', 'Otomatik', 'Elektrik', 5000, 5684.29, 1000, 27, 'Volvo_XC40_Recharge.jpg', 'PREMIUM'),
        ('Volvo', 'XC40', 'Otomatik', 'Dizel/Benzin', 5000, 5777.74, 1000, 27, 'Volvo_XC40.jpg', 'PREMIUM'),
        ('BMW', '3 Serisi', 'Otomatik', 'Dizel/Benzin', 5000, 6136.64, 1000, 27, 'BMW_3_Serisi.jpg', 'PREMIUM'),
        ('BMW', '5 Serisi', 'Otomatik', 'Dizel/Benzin', 5000, 8562.78, 1000, 27, 'BMW_5_Serisi.jpg', 'PREMIUM'),
        ('Volvo', 'XC90', 'Otomatik', 'Dizel', 8500, 16306.12, 1000, 27, 'Volvo_XC90.jpg', 'LÜKS'),
    ]

    offices_count = 3  # Update based on your actual number of offices
    current_office_index = 0

    for vehicle in vehicles:
        # Get the OfficeID based on the current index
        office_id = current_office_index + 1  # Assuming office IDs start from 1

        image_path = os.path.join('app/car_images', vehicle[8])
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            vehicle_data = vehicle[:8] + (image_data, vehicle[-1], office_id)
            cursor.execute('''
                            INSERT INTO vehicles (Brand, Model, Transmission, FuelType, DepositPrice, DailyRentPrice, 
                            Mileage, Age, Image, CarType, OfficeID)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', vehicle_data)

        # Move to the next office in a round-robin fashion
        current_office_index = (current_office_index + 1) % offices_count

    connection.commit()
    connection.close()


def drop_vehicle_table():
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()
    cursor.execute('''DROP TABLE IF EXISTS vehicles''')
    
    connection.commit()
    connection.close()

def get_filtered_vehicles(selected_office):
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT office_id FROM office WHERE office_title = ?", (selected_office,))
    office_id = cursor.fetchone()
    if office_id is not None:
        # Use the retrieved OfficeID in the query
        query = "SELECT * FROM vehicles WHERE OfficeID = ?"
        result = cursor.execute(query, (office_id[0],)).fetchall()
    else:
        result = []

    connection.close()
    return result

def get_all_vehicles():
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM vehicles")
    offices = cursor.fetchall()
    connection.close()
    return offices

def insert_vehicles_2(vehicles):
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()

    offices_count = 3  
    current_office_index = 0

    for vehicle in vehicles:
        
        office_id = current_office_index + 1  

        image_path = os.path.join('app/car_images', vehicle[8])
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            vehicle_data = vehicle[:-2] + (image_data, office_id)
            cursor.execute('''
                            INSERT INTO vehicles (Brand, Model, Transmission, FuelType, DepositPrice, DailyRentPrice, 
                            Mileage, Age, Image, CarType, OfficeID)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', vehicle_data)

        # Move to the next office in a round-robin fashion
        current_office_index = (current_office_index + 1) % offices_count


    for vehicle in vehicles:
        image_path = os.path.join('app/car_images', vehicle[8])
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            vehicle_data = vehicle[:-2] + (image_data,) + vehicle[-1:]  # Remove the extra comma
            cursor.execute('''
                            INSERT INTO vehicles (Brand, Model, Transmission, FuelType, DepositPrice, DailyRentPrice, 
                            Mileage, Age, Image, CarType)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', vehicle_data)    

    connection.commit()
    connection.close()
    
  

