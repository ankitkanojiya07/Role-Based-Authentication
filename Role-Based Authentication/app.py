  # Import necessary libraries
from flask import Flask, request, jsonify
import sqlite3
import jwt
from functools import wraps
import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

# Connect to SQLite database
conn = sqlite3.connect('employee.db')
c = conn.cursor()

# Create employee table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS employees (
             id INTEGER PRIMARY KEY,
             name TEXT NOT NULL,
             email TEXT NOT NULL,
             role TEXT NOT NULL,
             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
             )''')
conn.commit()

# Middleware to check JWT token
def token_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                if data['role'] != role:
                    return jsonify({'message': 'Unauthorized access!'}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token is expired!'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token!'}), 401
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Authentication endpoint
@app.route('/api/auth/login', methods=['POST'])
def login():
    auth = request.authorization
    if auth and auth.username == 'admin' and auth.password == 'password':
        token = jwt.encode({'username': auth.username, 'role': 'Admin', 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token.decode('UTF-8')}), 200
    return jsonify({'message': 'Invalid credentials!'}), 401

# Employee endpoints
@app.route('/api/employees', methods=['GET'])
def get_employees():
    c.execute("SELECT * FROM employees")
    employees = c.fetchall()
    return jsonify({'employees': employees}), 200

@app.route('/api/employees/<int:id>', methods=['GET'])
def get_employee(id):
    c.execute("SELECT * FROM employees WHERE id=?", (id,))
    employee = c.fetchone()
    if employee:
        return jsonify({'employee': employee}), 200
    return jsonify({'message': 'Employee not found!'}), 404

@app.route('/api/employees', methods=['POST'])
@token_required('Admin')
def add_employee():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    role = data.get('role')
    c.execute("INSERT INTO employees (name, email, role) VALUES (?, ?, ?)", (name, email, role))
    conn.commit()
    return jsonify({'message': 'Employee added successfully!'}), 201

@app.route('/api/employees/<int:id>', methods=['PUT'])
@token_required('Admin')
def update_employee(id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    role = data.get('role')
    c.execute("UPDATE employees SET name=?, email=?, role=? WHERE id=?", (name, email, role, id))
    conn.commit()
    return jsonify({'message': 'Employee updated successfully!'}), 200

@app.route('/api/employees/<int:id>', methods=['DELETE'])
@token_required('Admin')
def delete_employee(id):
    c.execute("DELETE FROM employees WHERE id=?", (id,))
    conn.commit()
    return jsonify({'message': 'Employee deleted successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
