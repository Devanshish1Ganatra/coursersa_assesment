from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Booking, Menu
from .serializers import BookingSerializer, MenuSerializer


# ---- HTML pages served by Django ----
def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def menu_page(request):
    items = Menu.objects.all().order_by('name')
    return render(request, 'menu.html', {'menu': items})


# ---- API views ----
class MenuItemsView(generics.ListCreateAPIView):
    """GET /api/menu/ lists items (public); POST /api/menu/ creates one (token required)."""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    """GET (public) / PUT / PATCH / DELETE (token required) /api/menu/<id>/"""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    """Full CRUD for table bookings at /api/bookings/ and /api/bookings/<id>/ (token required)."""
    queryset = Booking.objects.all().order_by('reservation_date', 'reservation_slot')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
