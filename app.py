from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)  # allows iOS app to talk to Flask from different origin

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="yourdbname",
    user="youruser",
    password="yourpass",
    host="localhost",  # or actual host if deployed
)
cur = conn.cursor()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username']
    password = data['password']

    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return jsonify({'success': True})
    except:
        conn.rollback()
        return jsonify({'success': False, 'error': 'User may already exist'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    if user:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False}), 401
