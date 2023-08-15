from django import forms
from .models import Category, Product, CustomUser, Order, OrderItem, ShippingAddress
from django.forms import DateInput, DateTimeInput, ModelForm, NumberInput, Select, widgets, TextInput, CheckboxInput

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.models import User



# class ImageUploadForm(forms.ModelForm):
#     images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

#     class Meta:
#         model = Product
#         fields = ('images',)



# class LoginForm2(ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'password']
#         widgets = {
#             'username': TextInput(attrs={
#                 'class': 'form-control left',
#                 'placeholder': 'login',
#             }),
#             'password': TextInput(attrs={
#                 'class': 'form-control left',
#                 'placeholder': 'password',
#                 'type': "password",
#             }),

#         }

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    

# class RegisterForm(UserCreationForm):
class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

