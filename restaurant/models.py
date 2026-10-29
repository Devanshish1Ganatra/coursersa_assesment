from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    menu_item_description = models.TextField(max_length=1000, default="", blank=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    reservation_date = models.DateField()
    reservation_slot = models.SmallIntegerField(default=10)

    class Meta:
        # A date/time slot can only be booked once
        unique_together = ("reservation_date", "reservation_slot")

    def __str__(self):
        return f"{self.first_name} - {self.reservation_date} at {self.reservation_slot}:00"
