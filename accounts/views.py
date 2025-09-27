from django.shortcuts import render, redirect
from accounts.forms import RegisterForm
from django.contrib.auth import authenticate, login, logout

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = RegisterForm()
    
    return render(request, "frontend/accounts/register.html", {'form':form})



def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            return render(request, 'frontend/accounts/login.html', {'error':'invalid credentials'})
    return render(request, 'frontend/accounts/login.html')



def logout_view(request):
    logout(request)
    return redirect("/")