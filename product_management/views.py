

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.text import slugify
import os

from product_management.models import Category, Product
from product_management.forms import ProductForm, CategoryForm




##################################################
############### Admin Views ###################
##################################################



@login_required(login_url='login')
def product_list(request, category_slug=None):
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Add pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'products': page_obj,  # For backward compatibility
        'category_slug': category_slug
    }
    
    return render(request, 'product_management/product/product_list.html', context)


@login_required(login_url='login')
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            # Auto-generate slug if not provided
            if not product.slug:
                product.slug = slugify(product.name)
            product.save()
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('product_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'action': 'Add'
    }
    return render(request, 'product_management/product/product_form.html', context)


@login_required(login_url='login')
def product_update(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            # Auto-generate slug if not provided
            if not product.slug:
                product.slug = slugify(product.name)
            product.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('product_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'action': 'Update'
    }
    return render(request, 'product_management/product/product_form.html', context)


@login_required(login_url='login')
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product
    }
    return render(request, 'product_management/product/product_detail.html', context)


@login_required(login_url='login')
def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        # Delete the image file if it exists
        if product.image:
            if os.path.isfile(product.image.path):
                os.remove(product.image.path)
        
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('product_list')
    
    context = {
        'product': product
    }
    return render(request, 'product_management/product/product_confirm_delete.html', context)


# Category Views
@login_required(login_url='login')
def category_list(request):
    categories = Category.objects.all()
    
    # Add pagination
    paginator = Paginator(categories, 10)  # Show 10 categories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': page_obj  # For backward compatibility
    }
    return render(request, 'product_management/category/category_list.html', context)


@login_required(login_url='login')
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            # Auto-generate slug if not provided
            if not category.slug:
                category.slug = slugify(category.name)
            category.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'action': 'Add'
    }
    return render(request, 'product_management/category/category_form.html', context)


@login_required(login_url='login')
def category_update(request, slug):
    category = get_object_or_404(Category, slug=slug)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            # Auto-generate slug if not provided
            if not category.slug:
                category.slug = slugify(category.name)
            category.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'action': 'Update'
    }
    return render(request, 'product_management/category/category_form.html', context)


@login_required(login_url='login')
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True)
    
    # Add pagination for products in category
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'products': page_obj
    }
    return render(request, 'product_management/category/category_detail.html', context)


@login_required(login_url='login')
def category_delete(request, slug):
    category = get_object_or_404(Category, slug=slug)
    
    if request.method == 'POST':
        category_name = category.name
        # Check if category has products
        product_count = category.products_category.count()
        
        if product_count > 0:
            messages.error(request, f'Cannot delete category "{category_name}" because it has {product_count} product(s). Please move or delete the products first.')
            return redirect('category_list')
        
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('category_list')
    
    context = {
        'category': category,
        'product_count': category.products_category.count()
    }
    return render(request, 'product_management/category/category_confirm_delete.html', context)


# Additional utility views
@login_required(login_url='login')
def products_by_category(request, category_slug):
    """View products filtered by category"""
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, available=True)
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'products': page_obj
    }
    return render(request, 'product_management/product/products_by_category.html', context)





##################################################
############### Frontend Views ###################
##################################################



def home(request):
    products = Product.objects.filter(available=True)[:8]  # Show latest 8 products
    context = {
        'products': products
    }
    return render(request, 'frontend/home.html', context)


def home_product_list(request, category_slug=None):
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Add pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'products': page_obj,  # For backward compatibility
        'category_slug': category_slug
    }
    
    return render(request, 'frontend/product/home_product_list.html', context)




def front_product_list(request, category_slug=None):
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Add pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'products': page_obj,  # For backward compatibility
        'category_slug': category_slug
    }
    
    return render(request, 'frontend/product/front_product_list.html', context)




def front_product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product
    }
    return render(request, 'frontend/product/front_product_details.html', context)