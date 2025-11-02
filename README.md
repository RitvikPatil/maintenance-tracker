# Vehicle Maintenance Tracker API

A Django REST API for tracking vehicle maintenance schedules and reminders.

## Features

- JWT Authentication
- User Management
- Vehicle Management
- Maintenance Tracking
- Reminder System
- RESTful API Endpoints

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_NAME=maintenance_tracker
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

## Running the Project

1. Run migrations:
   ```
   python manage.py migrate
   ```
2. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
3. Run the development server:
   ```
   python manage.py runserver
   ```

## API Documentation

Once the server is running, access the API documentation at:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

## Testing

To run tests:
```
python manage.py test
```
