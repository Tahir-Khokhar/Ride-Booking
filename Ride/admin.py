from django.contrib import admin
from .models import Passenger, Driver, RideRequest

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'created_at']
    search_fields = ['name', 'email']

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['driver_name', 'driver_email', 'is_available', 'phone_number', 'created_at']
    list_filter = ['is_available']
    search_fields = ['driver_name', 'driver_email']

@admin.register(RideRequest)
class RideRequestAdmin(admin.ModelAdmin):
    list_display = ['passenger', 'pickup_location', 'dropoff_location', 'status', 'assigned_driver', 'created_at']
    list_filter = ['status']
    search_fields = ['passenger__name', 'pickup_location']
