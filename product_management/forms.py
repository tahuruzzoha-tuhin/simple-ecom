from django import forms
from product_management.models import Category, Product
import os

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter URL slug (auto-generated if left blank)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter category description (optional)'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'slug', 'description', 'price', 'available', 'stock', 'rating', 'image']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter URL slug (auto-generated if left blank)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter product description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Enter stock quantity'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Enter rating'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'category': 'Product Category',
            'name': 'Product Name',
            'slug': 'URL Slug',
            'description': 'Product Description',
            'price': 'Price ($)',
            'available': 'Available for sale',
            'stock': 'Stock Quantity',
            'rating': 'Rating (0-5)',
            'image': 'Product Image'
        }
        help_texts = {
            'slug': 'Leave blank to auto-generate from product name',
            'price': 'Enter price in USD',
            'stock': 'Number of items in stock',
            'image': 'Upload product image (JPG, PNG, GIF, WebP - Max 5MB)'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        # Set available to True by default for new products
        if not self.instance.pk:
            self.fields['available'].initial = True
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (5MB limit)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large (maximum 5MB)")
            
            # Check file extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError("Invalid file format. Please use JPG, PNG, GIF, or WebP")
        
        return image
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be negative")
        return price
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError("Stock cannot be negative")
        return stock
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Check if product name already exists (exclude current instance if updating)
            existing_product = Product.objects.filter(name__iexact=name)
            if self.instance.pk:
                existing_product = existing_product.exclude(pk=self.instance.pk)
            
            if existing_product.exists():
                raise forms.ValidationError("A product with this name already exists")
        
        return name

