from django.shortcuts import render
from rest_framework import generics, viewsets

from .models import Booking, Menu
from .serializers import BookingSerializer, MenuSerializer


# ---- Static HTML pages served by Django ----
def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


# ---- API views (token authentication required) ----
class MenuItemsView(generics.ListCreateAPIView):
    """GET /api/menu/ lists items; POST /api/menu/ creates one."""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    """GET / PUT / PATCH / DELETE /api/menu/<id>/"""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """Full CRUD for table bookings at /api/bookings/ and /api/bookings/<id>/"""
    queryset = Booking.objects.all().order_by("reservation_date", "reservation_slot")
    serializer_class = BookingSerializer
