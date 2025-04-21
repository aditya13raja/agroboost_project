from django import forms
from django.contrib.auth.models import User
from .models import Profile, Product

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile.USER_ROLES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price']
