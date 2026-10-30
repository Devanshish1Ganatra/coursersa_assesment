from django.db import IntegrityError, transaction
from django.test import TestCase

from restaurant.models import Booking, Menu


class MenuModelTest(TestCase):
    def test_str_returns_name(self):
        item = Menu.objects.create(name='Greek Salad', price='12.00', menu_item_description='Fresh')
        self.assertEqual(str(item), 'Greek Salad')

    def test_fields_saved(self):
        item = Menu.objects.create(name='Bruschetta', price='8.50')
        item.refresh_from_db()
        self.assertEqual(str(item.price), '8.50')
        self.assertEqual(item.menu_item_description, '')


class BookingModelTest(TestCase):
    def test_str_contains_name_and_slot(self):
        b = Booking.objects.create(first_name='Ann', reservation_date='2030-11-01', reservation_slot=12)
        self.assertIn('Ann', str(b))
        self.assertIn('12:00', str(b))

    def test_default_slot(self):
        b = Booking.objects.create(first_name='Ann', reservation_date='2030-11-01')
        self.assertEqual(b.reservation_slot, 10)

    def test_same_date_and_slot_not_allowed(self):
        Booking.objects.create(first_name='Ann', reservation_date='2030-11-01', reservation_slot=12)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Booking.objects.create(first_name='Bob', reservation_date='2030-11-01', reservation_slot=12)
