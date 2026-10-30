from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # App URLs: index.html page, menu/booking APIs and api-token-auth
    path('', include('restaurant.urls')),
    # Djoser endpoints: user registration (POST /auth/users/) and token login (POST /auth/token/login/)
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # Login / logout links for the DRF browsable API
    path('api-auth/', include('rest_framework.urls')),
]
