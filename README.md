This project is a backend system built using Flask and PostgreSQL to handle user authentication and monitor login activity.
It provides secure APIs for user management, login tracking, and password recovery.

Features:
User Registration & Login (JWT Authentication)
Secure Password Hashing
Login History Tracking (login & logout timestamps)
Advanced Filtering (name, date range, pagination)
OTP-based Password Reset with expiry & attempt limits
RESTful API Design
Input Validation and Error Handling

Tech Stack
Backend: Python (Flask)
Database: PostgreSQL (pgAdmin 4)
Authentication: JWT (Flask-JWT-Extended)
API Testing: Postman

Project Structure
project/
│── app.py
│── config.py
│── db.py
│
├── models/
│   ├── user_model.py
│   ├── login_history_model.py
│   ├── otp_model.py
│
├── routes/
│   ├── auth_routes.py
│   ├── user_routes.py
│   ├── login_history_routes.py
│
├── services/
│   ├── auth_service.py
│   ├── user_service.py
│
├── utils/
│   ├── security_utils.py

API ENDPOINTS
Authentication
Method	    Endpoint	           Description
POST	    /auth/register	        Register user
POST	    /auth/login	            Login & get JWT
POST	    /auth/forgot-password	  Generate OTP
POST	    /auth/reset-password	  Reset password (OTP required)
POST	    /auth/logout	          Logout user

Users
Method    Endpoint                          Description
GET       /users/                           Get all users
GET       /users/name                       Filter by username
GET       /users/starts_with                Filter by starting letter
GET       /users/letter-range               Filter by letter range
GET       /users/created-from               Filter by created date (from)
GET       /users/created-range              Filter by date range
GET       /users/pagination                 Pagination support
GET       /users/multiple-filters           Combine multiple filters

Login History
Method    Endpoint                          Description
GET       /login-history/                   Get all login history
GET       /login-history/username           Filter by username
GET       /login-history/from               Filter from datetime
GET       /login-history/to                 Filter to datetime
GET       /login-history/date-range         Filter by date range
GET       /login-history/multiple-filters   Combine multiple filters

