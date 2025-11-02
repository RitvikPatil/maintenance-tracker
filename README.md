# 🚗 Vehicle Maintenance Tracker API

A comprehensive Django REST API for tracking vehicle maintenance schedules, service history and reminders with JWT authentication.

## ✨ Features

- 🔐 JWT Authentication & Authorization
- 👥 User Management (Registration, Login, Profile)
- 🚗 Vehicle Management
- 🔧 Maintenance Tracking & Scheduling
- 🔔 Service Reminders
- 📝 Service History & Records
- 📚 RESTful API Endpoints
- 📖 Interactive API Documentation

## 🛠 Tech Stack

- **Backend**: Django 4.2 & Django REST Framework
- **Database**: SQLite (Development) / PostgreSQL (Production-ready)
- **Authentication**: JWT (Simple JWT)
- **API Documentation**: DRF Spectacular (Swagger/OpenAPI)
- **Package Management**: pip

## 🚀 Prerequisites

- Python 3.8+
- pip (Python package manager)
- (Optional) PostgreSQL for production

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RitvikPatil/maintenance-tracker.git
   cd maintenance-tracker
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root and add:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 📚 API Documentation

Once the server is running, access the interactive API documentation at:
- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **ReDoc**: http://localhost:8000/api/schema/redoc/

## 🔧 Available Endpoints

- `/api/users/` - User management
- `/api/auth/` - Authentication (login, register, token refresh)
- `/api/vehicles/` - Vehicle CRUD operations
- `/api/maintenance/` - Maintenance records and scheduling

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

🔗 **GitHub**: [github.com/RitvikPatil/maintenance-tracker](https://github.com/RitvikPatil/maintenance-tracker)
📧 **Contact**: [Your Email]
💡 **Issues**: Please use GitHub issues for any bugs or feature requests
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