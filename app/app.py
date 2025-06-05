# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_connection
from handi_funcs import handi_funcs
app = Flask(__name__)
CORS(app)  # allows requests from your iOS frontend

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return jsonify({"success": True}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    print("Received:", data)
    username = data.get("username")
    password = data.get("password")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        print("Login success")
        return jsonify({"success": True}), 200
    else:
        print("Login failed")
        return jsonify({"success": False, "error": "Invalid credentials"}), 401

@app.route("/add_round", methods=["POST"])
def add_round():
    data = request.get_json()
    username = data.get("username")
    score = data.get("score")

    if not username or not score:
        return jsonify({"success": False, "error": "Username and score are required"}), 400

    handi = handi_funcs()
    rid = handi.add_round(username, score)

    if rid:
        return jsonify({"success": True, "rid": rid}), 201
    else:
        return jsonify({"success": False, "error": "Failed to add round"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5070)
