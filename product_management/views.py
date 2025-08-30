from django.shortcuts import render
from product_management.models import Category, Product



def home(request):
    return render(request, 'pages/home.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from product_management.forms import RegisterForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, "accounts/register.html", {'form': form})




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, "accounts/login.html", {'error': 'invalid credentials'})
    return render(request, "accounts/login.html")


@login_required(login_url='login')
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def product_list(request, category_slug=None):
    products = Product.objects.filter(available=True)
    
    context = {
        'products': products,
    }
    
    return render(request, 'product_management/product/product_list.html', context)


def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'product_management/category/category_list.html', context)