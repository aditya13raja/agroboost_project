from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm, ProductForm
from .models import Profile, Product, Resource


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user, role=form.cleaned_data['role'])
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def dashboard(request):
    return render(request, 'dashboard.html')


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.uploader = request.user
            product.save()
            return redirect('dashboard')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


def view_products(request):
    role = request.GET.get('role')
    if role in ['SHG', 'FPG']:
        products = Product.objects.filter(uploader__profile__role=role)
    else:
        products = Product.objects.all()
    return render(request, 'view_products.html', {'products': products})
