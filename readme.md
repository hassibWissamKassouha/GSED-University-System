# Project Name

## Overview
Brief description of your project and its purpose.

## Prerequisites
- Python 3.8+
- pip
- Django 3.8+

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create a virtual environment
```bash
python -m venv venv
source venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Django Server

1. Apply database migrations
```bash
python manage.py migrate
```

2. Start the development server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000`

## API Documentation
### 1. POST /api/login/
Authenticate a user and return a token.

- URL: `/api/login/`
- Method: `POST`
- Content-Type: `application/json`

Request body:
```json
{
  "id": 123,
  "password": "your-password"
}
```

Successful response (HTTP 200):
```json
{
  "token": "0123456789abcdef...",
  "user_id": 123,
  "role": "admin",
  "name": "FirstName LastName"
}
```

Error response (HTTP 400):
```json
{
  "non_field_errors": ["بيانات الدخول غير صحيحة."]
}
```

Notes:
- Uses Django REST framework Token Authentication via `rest_framework.authtoken`.
- The token should be included in subsequent requests as `Authorization: Token <token>`.

## Frontend Development
Your frontend partner can access the API endpoints at `http://127.0.0.1:8000/api/`

## Project Structure
```
Uni/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __pycache__/
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   └── __pycache__/
│   └── __pycache__/
├── readme.md
├── manage.py
├── pyvenv.cfg
├── CACHEDIR.TAG
├── .gitignore
├── Include/ (virtualenv)
├── Lib/ (virtualenv)
└── Scripts/ (virtualenv)
```

## Contributing
[Add contribution guidelines]

## License
[Specify your license]