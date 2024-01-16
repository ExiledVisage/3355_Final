Hello this is my final project. I have made a website application about car rental site


Video: https://drive.google.com/file/d/15fmLuGnJgG1q34pWxNW-iQ_Tx492V_b4/view?usp=sharing


I have utilized:
JS
HTML
CSS
Python
MVC design pattern

I pages I have are:
Login
Register
Main page
Car rental page

Database structures are : 

office (
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

users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
surname TEXT NOT NULL,            
email TEXT UNIQUE NOT NULL,
password TEXT NOT NULL,
country TEXT NOT NULL,
city TEXT NOT NULL                       
)

vehicles  (
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


I have encountered some of the problems below: 
Image encoding decoding problems.
Working with googlemaps API
Working and understanding session.
Listing offices that shows on the map.
Front end design problems.
Making pages responsive.
I am 4-5 commits behind because I forgot to open a repo before and 
still couldn't figure it out.


Overall:
I fell short in front end design while I executed backend structure.

