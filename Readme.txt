Little Lemon - Back-end Developer Capstone (Django REST Framework + MySQL)

Project: littlelemon      App: restaurant

API PATHS TO TEST (base URL: http://127.0.0.1:8000)

12
/                           GET   index.html page (served by Django)
/about/                     GET   about page
/menu-page/                 GET   HTML menu page (items from the database)
/auth/users/                POST  register (username, email, password)          [Djoser]
/auth/token/login/          POST  log in -> returns auth_token                  [Djoser]
/api-token-auth/            POST  log in -> returns token                       [DRF obtain_auth_token]
/api/menu/                  GET list (public), POST create (token needed)
/api/menu/<id>/             GET (public), PUT, PATCH, DELETE (token needed)
/api/bookings/              GET list, POST create (token needed)
/api/bookings/<id>/         GET, PUT, PATCH, DELETE (token needed)
/api-auth/login/            browsable API login page (session login for the browser)

AUTHENTICATION
Send the token on protected requests as the header:  Authorization: Token <token>

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

TESTING WITH THE BROWSABLE API
1. Open http://127.0.0.1:8000/api/menu/ (readable without logging in).
2. Open http://127.0.0.1:8000/api-auth/login/?next=/api/bookings/ and log in with the superuser
   or a registered user, then use the forms at the bottom of /api/bookings/ and /api/menu/.

TESTING WITH INSOMNIA
1. Import Insomnia_LittleLemon.json (Application > Import > From File).
2. Run "Register user", then "Login (Djoser)" and copy auth_token.
3. In Manage Environments, paste it as "token" (used as: Authorization: Token {{ _.token }}).
4. Run the menu and booking requests.

UNIT TESTS
python manage.py test
  restaurant/tests/test_models.py   model tests
  restaurant/tests/test_views.py    page, API and authentication tests
(the MySQL user needs permission to create the test_littlelemon database)
