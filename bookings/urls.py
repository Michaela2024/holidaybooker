from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/edit/', views.edit_booking, name='edit_booking'),
    path('booking/<int:booking_id>/delete/', views.delete_booking, name='delete_booking'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('property/<int:property_id>/book/', views.create_booking, name='create_booking'),

]
