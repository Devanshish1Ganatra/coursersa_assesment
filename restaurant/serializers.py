from rest_framework import serializers

from .models import Booking, Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "name", "price", "menu_item_description"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "first_name", "reservation_date", "reservation_slot"]

    def validate_reservation_slot(self, value):
        if not 10 <= value <= 20:
            raise serializers.ValidationError("Reservation slot must be between 10 and 20.")
        return value
