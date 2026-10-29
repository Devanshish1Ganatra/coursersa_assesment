Little Lemon - Back-end Developer Capstone (Django REST Framework + MySQL)

API PATHS TO TEST (base URL: http://127.0.0.1:8000)
All /api/ paths need the header:  Authorization: Token <auth_token>

12
/auth/users/                POST  register (username, email, password)
/auth/token/login/          POST  log in (username, password) -> returns auth_token
/api/menu/                  GET list, POST create
/api/menu/<id>/             GET, PUT, PATCH, DELETE
/api/bookings/              GET list, POST create (first_name, reservation_date, reservation_slot 10-20)
/api/bookings/<id>/         GET, PUT, PATCH, DELETE
/                           HTML home page (served by Django)
/about/                     HTML about page

SETUP
1. pipenv install
2. pipenv shell
3. Create the MySQL database:  CREATE DATABASE littlelemon;
4. Set USER and PASSWORD in littlelemon/settings.py (DATABASES)
5. python manage.py migrate
6. python manage.py createsuperuser   (optional, for /admin/)
7. python manage.py runserver

Note: mysqlclient needs the MySQL client libraries (macOS: brew install mysql pkg-config;
Ubuntu: sudo apt install libmysqlclient-dev pkg-config).

TESTS
python manage.py test
(the MySQL user needs permission to create the test_littlelemon database)

INSOMNIA EXAMPLES
POST /auth/users/            {"username": "carol", "email": "carol@example.com", "password": "<password>"}
POST /auth/token/login/      {"username": "carol", "password": "<password>"}
POST /api/bookings/          {"first_name": "Carol", "reservation_date": "2026-11-20", "reservation_slot": 12}
POST /api/menu/              {"name": "Greek Salad", "price": "12.00", "menu_item_description": "Fresh salad"}
