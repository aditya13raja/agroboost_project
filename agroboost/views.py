from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm, ProductForm
from .models import Profile, Product, Resource
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages


def home(request):
    latest_products = Product.objects.order_by('-added_on')[:6]
    return render(request, 'home.html', {'latest_products': latest_products})


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
    if request.user.is_authenticated:
        # Fetch products uploaded by the logged-in user
        products = Product.objects.filter(uploader=request.user).order_by('-added_on')
    else:
        products = []

    return render(request, 'dashboard.html', {'products': products})



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


from django.core.paginator import Paginator

def view_products(request):
    role = request.GET.get('role')
    query = request.GET.get('q', '')
    products = Product.objects.all()

    if role in ['SHG', 'FPG']:
        products = products.filter(uploader__profile__role=role)
    if query:
        products = products.filter(name__icontains=query)

    paginator = Paginator(products, 6)  # 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'view_products.html', {
        'products': page_obj,
        'query': query
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Only uploader can edit
    if product.uploader != request.user:
        return redirect('view_products')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('view_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'add_product.html', {'form': form, 'edit': True})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.uploader != request.user:
        return redirect('view_products')

    if request.method == 'POST':
        product.delete()
        return redirect('view_products')

    return render(request, 'confirm_delete.html', {'product': product})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was updated successfully.")
            return redirect('dashboard')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})
