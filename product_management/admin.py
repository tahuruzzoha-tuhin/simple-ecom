from django.contrib import admin

from product_management.models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    list_filter = ['name']
    search_fields = ['name']
    
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    list_filter = ['name']
    search_fields = ['name']
    
    
admin.site.register(Product, ProductAdmin)