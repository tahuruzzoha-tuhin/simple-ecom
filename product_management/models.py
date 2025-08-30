from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Product Category'
        ordering = ('created_at',)
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_management:products_by_category', args=[self.slug])
    
    
    

class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products_category", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('created_at',)
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_management:product_detail', args=[self.slug])