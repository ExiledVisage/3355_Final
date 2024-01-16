from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
from app import route

