from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Driver, RideRequest, Passenger

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DriverRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Driver
        fields = ['driver_name', 'driver_email', 'phone_number', 'password']

class RideBookingForm(forms.ModelForm):
    class Meta:
        model = RideRequest
        fields = ['pickup_location', 'dropoff_location']
        widgets = {
            'pickup_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pickup'}),
            'dropoff_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dropoff'}),
        }
