from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"bookings", views.BookingViewSet, basename="booking")

urlpatterns = [
    path("menu/", views.MenuItemsView.as_view(), name="menu-items"),
    path("menu/<int:pk>/", views.SingleMenuItemView.as_view(), name="menu-item"),
    path("", include(router.urls)),
]
