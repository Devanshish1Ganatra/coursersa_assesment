from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from restaurant.models import Booking, Menu

FUTURE = (date.today() + timedelta(days=30)).isoformat()
PAST = (date.today() - timedelta(days=30)).isoformat()


class PageViewTests(TestCase):
    def test_index_html_served(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Little Lemon')

    def test_about_page(self):
        self.assertEqual(self.client.get('/about/').status_code, 200)

    def test_menu_page_lists_items(self):
        Menu.objects.create(name='Lemon Dessert', price='7.00')
        response = self.client.get('/menu-page/')
        self.assertContains(response, 'Lemon Dessert')


class AuthenticatedAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', 't@example.com', 'S3cure-pass!')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')


class MenuViewTests(AuthenticatedAPITestCase):
    def test_create_and_list(self):
        r = self.client.post('/api/menu/', {'name': 'Bruschetta', 'price': '8.00', 'menu_item_description': 'x'})
        self.assertEqual(r.status_code, 201)
        r = self.client.get('/api/menu/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    def test_single_get_update_delete(self):
        item = Menu.objects.create(name='Fish', price='20.00')
        self.assertEqual(self.client.get(f'/api/menu/{item.pk}/').status_code, 200)
        self.assertEqual(self.client.patch(f'/api/menu/{item.pk}/', {'price': '22.00'}).status_code, 200)
        self.assertEqual(self.client.delete(f'/api/menu/{item.pk}/').status_code, 204)

    def test_missing_item_404(self):
        self.assertEqual(self.client.get('/api/menu/999/').status_code, 404)

    def test_invalid_price_rejected(self):
        r = self.client.post('/api/menu/', {'name': 'Free lunch', 'price': '0'})
        self.assertEqual(r.status_code, 400)

    def test_blank_name_rejected(self):
        r = self.client.post('/api/menu/', {'name': '   ', 'price': '5.00'})
        self.assertEqual(r.status_code, 400)


class BookingViewTests(AuthenticatedAPITestCase):
    data = {'first_name': 'Ann', 'reservation_date': FUTURE, 'reservation_slot': 12}

    def test_create_and_list(self):
        self.assertEqual(self.client.post('/api/bookings/', self.data).status_code, 201)
        r = self.client.get('/api/bookings/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    def test_duplicate_slot_rejected(self):
        self.client.post('/api/bookings/', self.data)
        r = self.client.post('/api/bookings/', {**self.data, 'first_name': 'Bob'})
        self.assertEqual(r.status_code, 400)

    def test_invalid_slot_rejected(self):
        r = self.client.post('/api/bookings/', {**self.data, 'reservation_slot': 3})
        self.assertEqual(r.status_code, 400)

    def test_past_date_rejected(self):
        r = self.client.post('/api/bookings/', {**self.data, 'reservation_date': PAST})
        self.assertEqual(r.status_code, 400)

    def test_update_and_delete(self):
        b = Booking.objects.create(first_name='Ann', reservation_date=FUTURE, reservation_slot=12)
        r = self.client.put(f'/api/bookings/{b.pk}/', {**self.data, 'reservation_slot': 13})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.client.delete(f'/api/bookings/{b.pk}/').status_code, 204)


class AuthViewTests(APITestCase):
    def test_bookings_need_token(self):
        self.assertEqual(self.client.get('/api/bookings/').status_code, 401)

    def test_menu_readable_without_token_but_not_writable(self):
        self.assertEqual(self.client.get('/api/menu/').status_code, 200)
        self.assertEqual(self.client.post('/api/menu/', {'name': 'x', 'price': '1.00'}).status_code, 401)

    def test_djoser_registration_and_token_login(self):
        r = self.client.post('/auth/users/', {'username': 'newuser', 'password': 'S3cure-pass!'})
        self.assertEqual(r.status_code, 201)
        r = self.client.post('/auth/token/login/', {'username': 'newuser', 'password': 'S3cure-pass!'})
        self.assertEqual(r.status_code, 200)
        self.assertIn('auth_token', r.json())

    def test_api_token_auth_route(self):
        User.objects.create_user('u', password='S3cure-pass!')
        r = self.client.post('/api-token-auth/', {'username': 'u', 'password': 'S3cure-pass!'})
        self.assertEqual(r.status_code, 200)
        self.assertIn('token', r.json())

    def test_wrong_password(self):
        User.objects.create_user('u', password='S3cure-pass!')
        r = self.client.post('/auth/token/login/', {'username': 'u', 'password': 'wrong'})
        self.assertEqual(r.status_code, 400)

    def test_browsable_api_login_page(self):
        self.assertEqual(self.client.get('/api-auth/login/').status_code, 200)
