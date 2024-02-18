# Role-Based Authentication System with REST APIs and Relational Database

## Objective
Create a role-based authentication system that allows CRUD operations on a dummy employee database. Users will be assigned different roles, and the system should enforce role-based access control.

## Technologies Used
- **Programming Language:** Python
- **Database:** SQLite
- **JWT for Authentication**

![Flask Logo](https://upload.wikimedia.org/wikipedia/commons/3/3c/Flask_logo.svg)

## Endpoints

### Authentication
- **POST /api/auth/login:** Allows user login with credentials. Returns a JWT token upon successful authentication.

### Employee Operations
- **GET /api/employees:** Retrieves all employees.
- **GET /api/employees/<id>:** Retrieves a specific employee by ID.
- **POST /api/employees:** Adds a new employee (accessible to Admin role).
- **PUT /api/employees/<id>:** Updates an existing employee by ID (accessible to Admin role).
- **DELETE /api/employees/<id>:** Deletes an employee by ID (accessible to Admin role).

### Authorization Middleware
- Implemented as `token_required(role)` decorator.
- Ensures that each API endpoint is accessible based on the user's role.
- Validates JWT token and enforces role-based access.

## Database Schema
- `employees` table with fields: id, name, email, role, created_at.

## JWT Authentication
- Generates a JWT token upon successful login.
- Token includes user role and expiration time.
- Used for subsequent authorization in API requests.

## Error Handling
- Provides proper error messages for missing, expired, or invalid tokens.
- Returns appropriate status codes for successful and failed requests.

## Setup and Run Instructions
### Requirements
- Python installed on your system.
- Flask and PyJWT libraries installed (use `pip install Flask PyJWT`).

### Run Application
1. Save the code in a file (e.g., `app.py`).
2. Open a terminal, navigate to the directory containing the file.
3. Run the application using `python app.py`.
