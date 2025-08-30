"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from product_management.views import  home, login_view, register_view, logout_view
urlpatterns = [
    # path('pages', include('apps.pages.urls')),
    # path('dyn_dt', include('apps.dyn_dt.urls')),
    # path('dyn_api', include('apps.dyn_api.urls')),
    # path('charts/', include('apps.charts.urls')),
    # path("admin/", admin.site.urls),
    path('', home, name="home_page"),
    path("dashboard/", include('admin_adminlte.urls'), name="dashboard"),
    
    path('accounts/login/', login_view, name='login'),
    path('accounts/register/', register_view, name='register'),
    path('accounts/logout/', logout_view, name='logout'),
    
    path("product_management/", include("product_management.urls"))
]
