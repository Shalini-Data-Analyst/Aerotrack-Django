AEROTRACK - DJANGO PAGINATION PROJECT

1. Open this folder in VS Code.
2. Open Terminal in VS Code.
3. (Recommended) Create and activate a virtual environment:
   py -m venv venv
   venv\Scripts\activate
4. Install Django:
   py -m pip install -r requirements.txt
5. Create database tables:
   py manage.py makemigrations
   py manage.py migrate
6. Insert 50 sample telemetry records:
   py manage.py seed_telemetry
7. Start the website:
   py manage.py runserver
8. Open http://127.0.0.1:8000/

The project uses Django's Paginator class and SQLite database.
Search, status filtering, page-size selection and CSV export are included.
