from datetime import date

from rest_framework import serializers

from .models import Booking, Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'price', 'menu_item_description']

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Name cannot be blank.')
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than zero.')
        return value


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'first_name', 'reservation_date', 'reservation_slot']

    def validate_first_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Name cannot be blank.')
        return value

    def validate_reservation_date(self, value):
        if value < date.today():
            raise serializers.ValidationError('Reservation date cannot be in the past.')
        return value

    def validate_reservation_slot(self, value):
        if not 10 <= value <= 20:
            raise serializers.ValidationError('Reservation slot must be between 10 and 20.')
        return value
