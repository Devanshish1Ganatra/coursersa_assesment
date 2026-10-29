from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Booking, Menu


class PageTests(TestCase):
    def test_home_page_served(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Little Lemon")

    def test_about_page_served(self):
        self.assertEqual(self.client.get("/about/").status_code, 200)


class ModelTests(TestCase):
    def test_menu_str(self):
        self.assertEqual(str(Menu.objects.create(name="Greek Salad", price="12.00")), "Greek Salad")

    def test_booking_str(self):
        b = Booking.objects.create(first_name="Ann", reservation_date="2026-11-01", reservation_slot=12)
        self.assertIn("Ann", str(b))


class AuthenticatedAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("tester", "t@example.com", "S3cure-pass!")
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")


class MenuAPITests(AuthenticatedAPITestCase):
    def test_create_and_list(self):
        r = self.client.post("/api/menu/", {"name": "Bruschetta", "price": "8.00", "menu_item_description": "x"})
        self.assertEqual(r.status_code, 201)
        r = self.client.get("/api/menu/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    def test_single_update_delete(self):
        item = Menu.objects.create(name="Fish", price="20.00")
        self.assertEqual(self.client.get(f"/api/menu/{item.pk}/").status_code, 200)
        r = self.client.patch(f"/api/menu/{item.pk}/", {"price": "22.00"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.client.delete(f"/api/menu/{item.pk}/").status_code, 204)

    def test_missing_item(self):
        self.assertEqual(self.client.get("/api/menu/999/").status_code, 404)


class BookingAPITests(AuthenticatedAPITestCase):
    data = {"first_name": "Ann", "reservation_date": "2026-11-01", "reservation_slot": 12}

    def test_create_and_list(self):
        self.assertEqual(self.client.post("/api/bookings/", self.data).status_code, 201)
        r = self.client.get("/api/bookings/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    def test_duplicate_slot_rejected(self):
        self.client.post("/api/bookings/", self.data)
        r = self.client.post("/api/bookings/", {**self.data, "first_name": "Bob"})
        self.assertEqual(r.status_code, 400)

    def test_invalid_slot_rejected(self):
        r = self.client.post("/api/bookings/", {**self.data, "reservation_slot": 3})
        self.assertEqual(r.status_code, 400)

    def test_update_and_delete(self):
        b = Booking.objects.create(first_name="Ann", reservation_date="2026-11-01", reservation_slot=12)
        r = self.client.put(f"/api/bookings/{b.pk}/", {**self.data, "reservation_slot": 13})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.client.delete(f"/api/bookings/{b.pk}/").status_code, 204)


class AuthTests(APITestCase):
    def test_unauthenticated_rejected(self):
        self.assertEqual(self.client.get("/api/menu/").status_code, 401)
        self.assertEqual(self.client.get("/api/bookings/").status_code, 401)

    def test_registration_and_token_login(self):
        r = self.client.post("/auth/users/", {"username": "newuser", "password": "S3cure-pass!"})
        self.assertEqual(r.status_code, 201)
        r = self.client.post("/auth/token/login/", {"username": "newuser", "password": "S3cure-pass!"})
        self.assertEqual(r.status_code, 200)
        self.assertIn("auth_token", r.json())

    def test_wrong_password(self):
        User.objects.create_user("u", password="S3cure-pass!")
        r = self.client.post("/auth/token/login/", {"username": "u", "password": "wrong"})
        self.assertEqual(r.status_code, 400)
