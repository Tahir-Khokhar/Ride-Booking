from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("book/", views.book, name="book"),
    path("book_ride/", views.book_ride, name="book_ride"),
    path("user_register/", views.user_register, name="user_register"),
    path("user_login/", views.user_login, name="user_login"),
    path("logout/", views.logout_view, name="logout"),
# path("passenger_register/", views.passenger_register, name="passenger_register"),  # passenger_list instead
    path("driver_register/", views.driver_register, name="driver_register"),
    path("driver_login/", views.driver_login, name="driver_login"),
    path("driver_dashboard/", views.driver_dashboard, name="driver_dashboard"),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('users_list/', views.user_list, name='user_list'),
    path('drivers_list/', views.driver_list, name='driver_list'),
    path('passengers_list/', views.passenger_list, name='passenger_list'),
    path('rides/', views.ride_list, name='ride_list'),
]
