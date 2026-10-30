from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'bookings', views.BookingViewSet, basename='booking')

urlpatterns = [
    # HTML pages served by Django (index.html is rendered by views.index)
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('menu-page/', views.menu_page, name='menu-page'),

    # Token authentication: POST username + password -> {"token": "..."}
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),

    # API endpoints
    path('api/menu/', views.MenuItemsView.as_view(), name='menu-items'),
    path('api/menu/<int:pk>/', views.SingleMenuItemView.as_view(), name='menu-item'),
    path('api/', include(router.urls)),
]
