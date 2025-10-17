from django.contrib import admin
from django.urls import include, path
from accounts.views import (
    register_view, login_view, logout_view,
    register_api, login_api, profile_api, logout_api
)

urlpatterns = [
    # Traditional web views
    path("login_view", login_view, name="login_view"),
    path("register_view", register_view, name="register_view"),
    path("logout_view", logout_view, name="logout_view"),
    
    # API endpoints
    path("api/register/", register_api, name="api_register"),
    path("api/login/", login_api, name="api_login"),
    path("api/profile/", profile_api, name="api_profile"),
    path("api/logout/", logout_api, name="api_logout"),
]
