import sqlite3
import googlemaps

gmaps=googlemaps.Client(key="AIzaSyDvVgkgvhFDwZ8JwDLLEGOnCG8UAZF4DMI")

def geocode_address(address):
    # Perform geocoding for the given address
    geocode_result = gmaps.geocode(address)
    
    if geocode_result and len(geocode_result) > 0:
        # Extract latitude and longitude from the geocoding result
        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']
        return latitude, longitude
    else:
        return None, None  # Return None for latitude and longitude if geocoding fails

def update_office_coordinates():
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM office WHERE office_latitude IS NULL OR office_longitude IS NULL")
    offices_without_coordinates = cursor.fetchall()
    
    for office in offices_without_coordinates:
        office_address = office[3]  # Assuming office_address is at index 3 in the fetched data
        
        # Perform geocoding for the office address
        latitude, longitude = geocode_address(office_address)
        
        if latitude is not None and longitude is not None:
            # Update the database with obtained coordinates
            cursor.execute("UPDATE office SET office_latitude=?, office_longitude=? WHERE office_id=?",
                           (latitude, longitude, office[0]))  # Assuming office_id is at index 0
    
    connection.commit()
    connection.close()

def get_all_offices():
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM office")
    offices = cursor.fetchall()
    connection.close()
    return offices

def get_office_names():
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()

    # Example query to retrieve office names
    query = "SELECT office_title FROM office"
    result = cursor.execute(query).fetchall()

    connection.close()
    # Extract office names from the result
    office_names = [row[0] for row in result]
    return office_names

def get_office_id_by_name(office_name):
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()

    # Query to retrieve office_id based on office_name
    query = "SELECT office_id FROM office WHERE office_title = ?"
    result = cursor.execute(query, (office_name,)).fetchone()

    connection.close()

    # Check if the office exists and return the office_id, otherwise return None
    if result:
        return result[0]
    else:
        return None


def connectionOffice():
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS office (
            office_id INTEGER PRIMARY KEY AUTOINCREMENT,
            office_city TEXT,
            office_title TEXT,
            office_address TEXT,
            office_number TEXT,      
            office_opening_hour TEXT,
            office_closing_hour TEXT,
            office_latitude REAL,  
            office_longitude REAL  
        );
    ''')
    print("merhaba office!")
    connection.commit()
    connection.close()

def insert_offices():
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()
    
    offices = [
        ('İZMİR', 'BAYRAKLI OFİS', 'Manavkuyu, Yüzbaşı İbrahim Hakkı Cd. No: 243/B, 35535 Bayraklı/İzmir', '505 283 98 94', '09:00 AM', '05:00 PM',),
        ('İZMİR', 'BORNOVA OFİS', 'Ergene, Yüzbaşı İbrahim Hakkı Cd. No:25, 35040 Bornova/İzmir', '506 177 38 65', '08:00 AM', '06:00 PM',),
        ('İZMİR', 'ALSANCAK OFİS', 'Alsancak, Mahmut Esat Bozkurt Cd. 21 A, 35220 Konak/İzmir', '531 428 39 21', '08:00 AM', '06:00 PM',),
    ]

    cursor.executemany('''
        INSERT INTO office (office_city, office_title, office_address, office_number, 
                            office_opening_hour, office_closing_hour)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', offices)

    connection.commit()
    connection.close()


def drop_office_table():
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()
    cursor.execute('''DROP TABLE IF EXISTS office''')
    
    connection.commit()
    connection.close()