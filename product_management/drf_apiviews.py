
# 1. Query from db 
# 2. Dictionary
# 3. JsonResponse

#DRF (Serialization)
# 1. Query from db
# 2. Serializer --> 
# 3. Response


#DRF (Deserialization)
# 1. Request (JSON)
# 2. Serializer (Validation, Deserialization)
# 3. Save to db



from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from product_management.models import Category, Product
from product_management.serializers import CategorySerializer, ProductSerializer


#Category Views
class CategoryListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        categories = Category.objects.all() #queryset SELECT * FROM category
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data) #deserialization
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class CategoryDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
# Product Views
class ProductListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        products = Product.objects.order_by('-created_at') # 1. database(sql), 2. queryset 3. serializer(-> python data type) 4. Response(-> JSON)
        # print(products)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ProductDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
    
# Products by Category
class ProductsByCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, category_slug):
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    

 # a > b ? "a is greater" : "b is greater"