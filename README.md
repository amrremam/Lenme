# Lenme

# Loan Management API

## Local Setup
1. Clone repository 
    ```
    git clone https://github.com/amrremam/Lenme.git
    
    ```
2. Create virtual environment
    ```
    python3 -m venv venv
    ```
3. Activate virtual environment
    ```
    ./env/bin/activate
    ```
4. Install requirements
    ```
    pip install -r requirements.txt
    ```
5. Migrate to database
    ```
    python manage.py migrate
    ```
6. Run server
    ```
    python manage.py runserver
    ```
---

## Swagger API Documentation
1.  Run server
    ```
    python manage.py runserver
    http://localhost:8000/swagger/
    ```
