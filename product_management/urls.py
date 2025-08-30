from django.contrib import admin
from django.urls import include, path

from product_management.views import product_list, category_list, home

urlpatterns = [

    path('products/',product_list, name="product_list"),
    path('categories/',category_list, name="category_list"),
]
