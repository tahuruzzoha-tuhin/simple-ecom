from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from product_management.models import Category, Product

#Category Helper function
def category_to_dict(category):
    return {
        "id": category.id,
        "name": category.name,
        "slug": category.slug,
        "description": category.description,
        "created_at": category.created_at,
        "updated_at": category.updated_at,
    }
    
    
# Product Helper function
def product_to_dict(product):
    return {
        "id": product.id,
        "category": product.category.id,
        "category_name": product.category.name,
        "name": product.name,
        "slug": product.slug,
        "description": product.description,
        "price": product.price,
        "available": product.available,
        "stock": product.stock,
        "rating": product.rating,
        "image": product.image.url if product.image else None,
        "created_at": product.created_at,
        "updated_at": product.updated_at,
    }


# Categories Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def category_list_create(request):
    if request.method == "GET":
        categories = Category.objects.all() #queryset
        data = [category_to_dict(cat) for cat in categories] # [{}, {}, ...]
        return JsonResponse(data, safe=False)
    
    elif request.method == "POST":
        pass
    
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def category_details(request, pk):
    category = Category.objects.get(pk=pk)
    
    if request.method == "GET":
        return JsonResponse(category_to_dict(category))
    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
        
        
# Products Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def product_list_create(request):
    if request.method == "GET":
        products = Product.objects.all()
        data = [product_to_dict(prod) for prod in products]
        return JsonResponse(data, safe=False)
    
    elif request.method == "POST":
        pass
    
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def product_details(request, pk):
    product = Product.objects.get(pk=pk)
    
    if request.method == "GET":
        return JsonResponse(product_to_dict(product))
    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    



# Products by Category
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def products_by_category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    products = Product.objects.filter(category=category)
    data = [product_to_dict(prod) for prod in products] # [{}, {}, ...]
    return JsonResponse(data, safe=False)


# @require_http_methods(["GET"])