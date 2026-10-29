from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("restaurant.urls")),
    # Djoser: registration (POST /auth/users/) and token login (POST /auth/token/login/)
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    # Static HTML pages served by Django
    path("", include("restaurant.page_urls")),
]
