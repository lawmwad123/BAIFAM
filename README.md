# Car Bond Management System

A web application for managing car listings and purchases, built with Django and Bootstrap.

## Features

- **Car Listing & API Integration**
  - Fetch and display car details from external API
  - Store car information locally for optimized access
  - Search and filter car listings

- **User Order System**
  - Browse available cars
  - Place and track car purchase orders
  - View order history and status updates

- **User Authentication & Authorization**
  - Secure user authentication ( login, logout)
  - Password change functionality
  - Role-based access control

- **Order Management**
  - Track order status and updates
  - Store order details and user information
  - Real-time order status updates

- **Modern UI/UX**
  - Responsive design using Bootstrap
  - Interactive elements with JavaScript
  - Clean and intuitive interface

## Technology Stack

- **Backend**: Django 5.1.5
- **Frontend**: Django Templates, Bootstrap 5, JavaScript
- **Database**: PostgreSQL (with Neon)
- **API**: Django REST Framework
- **Authentication**: Django's built-in authentication system

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:lawmwad123/BAIFAM.git
   cd car-bond-management
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your environment variables:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=your_neon_database_url
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=5432
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
car_bond_management/
├── cars/                   # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── urls.py            # URL routing
│   └── serializers.py     # API serializers
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── registration/     # Auth templates
│   └── cars/            # Car-related templates
├── static/               # Static files
│   ├── css/             # CSS files
│   ├── js/              # JavaScript files
│   └── img/             # Images
└── car_bond_management/  # Project settings
    ├── settings.py      # Project settings
    └── urls.py          # Main URL routing
```

## API Endpoints

- `GET /cars/api/cars/`: List all cars
- `POST /cars/api/cars/`: Create a new car listing
- `GET /cars/api/cars/<id>/`: Get car details
- `GET /cars/api/orders/`: List user's orders
- `POST /cars/api/orders/`: Create a new order

## Technical Implementation Details

### 1. System Design
The system uses Django models for Cars, Orders, and CarImages with clear relationships:
- Car model stores vehicle details (make, model, year, price)
- Order model tracks purchases with status management
- CarImage model handles multiple images per car
All models are integrated with Django's auth system for user management.

### 2. API Integration
- External car data is fetched via CarAPIService in services.py
- Implements error handling and local caching
- Uses requests library with try-catch blocks
- Falls back to local data if API is unavailable

### 3. User Interaction
- Bootstrap-based responsive UI with car listing and detail views
- Order placement workflow with status tracking
- Comprehensive order history view with filtering
- Interactive elements using custom JavaScript

### 4. Authentication & Authorization
- Uses Django's built-in authentication system
- Role-based access control for admin/regular users
- Custom permissions for order management
- Secure password handling and change functionality

### 5. Order Management
- Status tracking (pending, approved, rejected, completed)
- Order model includes user, car, status, dates, and amount
- Real-time status updates
- Detailed order history view

### 6. Testing & Deployment
- Unit tests for models and views
- Integration tests for API functionality
- Uses PostgreSQL with Neon for production
- Environment variables for configuration

### 7. Scalability and Performance
- Optimized database queries
- Caching of external API data
- Efficient static file handling
- Responsive design for all devices

