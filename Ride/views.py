from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Passenger, Driver, RideRequest
from .forms import RideBookingForm

def home(request):  
    return render(request, "home.html")

def book(request):
    return redirect('book_ride')

@login_required
def book_ride(request):
    if request.method == "POST":
        form = RideBookingForm(request.POST)
        if form.is_valid():
            passenger, created = Passenger.objects.get_or_create(
                name=request.user.username,
                defaults={'email': request.user.email}
            )
            ride = form.save(commit=False)
            ride.passenger = passenger
            ride.save()
            messages.success(request, "Ride request booked successfully!")
            return redirect('book_ride')
    else:
        form = RideBookingForm()
    return render(request, "ride_booking.html", {'form': form})

def user_register(request):
    if request.method == "POST":
        user_name = request.POST.get("User_Name")
        email = request.POST.get("Email")
        password = request.POST.get("Password")
        if User.objects.filter(username=user_name).exists():
            messages.error(request, "Username already exists")
            return render(request, "user_register.html")
        User.objects.create_user(
            username=user_name,
            email=email,
            password=password
        )
        messages.success(request, "User registered!")
        return redirect("user_login")
    return render(request, "user_register.html")

def user_login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST.get("User_Name"), password=request.POST.get("Password"))
        if user:
            login(request, user)
            return redirect("home")
        messages.error(request, "Invalid credentials")
    return render(request, "user_login.html")

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    if 'driver_id' in request.session:
        del request.session['driver_id']
    return redirect('home')

def driver_register(request): 
    if request.method == "POST":
        driver_name = request.POST.get("Driver_Name")
        driver_email = request.POST.get("email")
        driver_password = request.POST.get("password")
        phone_number = request.POST.get("phone_number", "")
        if Driver.objects.filter(driver_email=driver_email).exists():
            messages.error(request, "Email exists")
            return render(request, "driver_register.html")
        Driver.objects.create(
            driver_name=driver_name,
            driver_email=driver_email,
            driver_password=make_password(driver_password),
            phone_number=phone_number
        )
        messages.success(request, "Driver registered!")
        return redirect("driver_login")
    return render(request, "driver_register.html")

def driver_login(request):
    if request.method == "POST":
        try:
            driver = Driver.objects.get(driver_email=request.POST.get("email"))
            if check_password(request.POST.get("password"), driver.driver_password):
                request.session['driver_id'] = driver.driver_id
                request.session['driver_name'] = driver.driver_name
                messages.success(request, "Logged in!")
                return redirect("driver_dashboard")
            messages.error(request, "Invalid")
        except Driver.DoesNotExist:
            messages.error(request, "Invalid")
    return render(request, "driver_login.html")

def driver_dashboard(request):
    driver_id = request.session.get('driver_id')
    driver = get_object_or_404(Driver, driver_id=driver_id)
    if request.method == 'POST':
        ride_id = request.POST.get('ride_id')
        ride = get_object_or_404(RideRequest, id=ride_id, status='pending')
        with transaction.atomic():
            ride = RideRequest.objects.select_for_update().get(id=ride_id, status='pending', assigned_driver__isnull=True)
            if driver.is_available:
                ride.assigned_driver = driver
                ride.status = 'confirmed'
                ride.save()
                driver.is_available = False
                driver.save()
                messages.success(request, 'Ride accepted (locked)!')
            else:
                messages.error(request, "Not available")
    pending_rides = RideRequest.objects.filter(status='pending').select_related('passenger')[:20]
    context = {'pending_rides': pending_rides, 'driver': driver}
    return render(request, 'driver_dashboard.html', context)

def driver_list(request):
    drivers = Driver.objects.all()
    paginator = Paginator(drivers, 10)
    page = request.GET.get('page')
    drivers = paginator.get_page(page)
    return render(request, "driver_list.html", {'drivers': drivers})

def passenger_list(request):
    passengers = Passenger.objects.all()
    paginator = Paginator(passengers, 10)
    page = request.GET.get('page')
    passengers = paginator.get_page(page)
    return render(request, "passenger_list.html", {'passengers': passengers, 'title': 'Passengers'})

def ride_list(request):
    rides = RideRequest.objects.select_related('passenger', 'assigned_driver').all().order_by('-created_at')
    paginator = Paginator(rides, 10)
    page = request.GET.get('page')
    rides = paginator.get_page(page)
    return render(request, "ride_list.html", {'rides': rides, 'title': 'Booked Rides'})

def user_list(request):
    users = User.objects.all()
    paginator = Paginator(users, 10)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    return render(request, "user_list.html", {'users': users})

def admin_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_drivers': Driver.objects.count(),
        'total_passengers': Passenger.objects.count(),
        'total_rides': RideRequest.objects.count(),
        'pending_rides': RideRequest.objects.filter(status='pending').count(),
        'confirmed_rides': RideRequest.objects.filter(status='confirmed').count(),
    }
    return render(request, 'admin_dashboard.html', context)
