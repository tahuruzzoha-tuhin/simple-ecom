from django.contrib import admin
from django.urls import include, path

from product_management.views import *
from product_management.without_drf_apiviews import *
from product_management.drf_apiviews import *

urlpatterns = [
    
    ################################
    ####### Frontend url ###########
    ################################
    
    path('home/', home, name="home"),
    path('home-product-list/', home_product_list, name='home_product_list'),
    path('product-list/', front_product_list, name='front_product_list'),
    path('product/<slug:slug>/', front_product_detail, name='front_product_detail'),
    
    
    
    ################################
    ####### Admin Panel url ########
    ################################

    
    # Product URLs
    path('products/', product_list, name='product_list'),
    path('products/add/', product_create, name='product_create'),
    path('products/<slug:slug>/', product_detail, name='product_detail'),
    path('products/<slug:slug>/edit/', product_update, name='product_update'),
    path('products/<slug:slug>/delete/', product_delete, name='product_delete'),
    
    # Category URLs
    path('categories/', category_list, name='category_list'),
    path('categories/add/', category_create, name='category_create'),
    path('categories/<slug:slug>/', category_detail, name='category_detail'),
    path('categories/<slug:slug>/edit/', category_update, name='category_update'),
    path('categories/<slug:slug>/delete/', category_delete, name='category_delete'),
    
    # Products by category
    path('category/<slug:category_slug>/products/', products_by_category, name='products_by_category'),
]






urlpatterns += [
    #Categories
    path("api/categories/", category_list_create, name="api_category_list_create"),
    path("api/categories/<int:pk>/", category_details, name="api_category_details"),
    
    #Products
    path("api/products/", product_list_create, name="api_product_list_create"),
    path("api/products/<int:pk>/", product_details, name="api_product_details"),
    
    path("api/products/category/<slug:category_slug>/", products_by_category, name="api_products_by_category"),
    
        
]


urlpatterns += [
    #Categories
    path("api/drf/categories/", CategoryListCreateAPIView.as_view(), name="drf_category_list_create"),
    path("api/drf/categories/<int:pk>/", CategoryDetailsAPIView.as_view(), name="drf_category_details"),
    
    #Products
    path("api/drf/products/", ProductListCreateAPIView.as_view(), name="drf_product_list_create"),
    path("api/drf/products/<int:pk>/", ProductDetailsAPIView.as_view(), name="drf_product_details"),
]