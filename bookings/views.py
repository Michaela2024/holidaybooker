from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import datetime
import requests
from .models import Property, Booking

# -------------------------
# Homepage & Property List
# -------------------------
def index(request):
    """Browse available properties with pagination"""
    properties_list = Property.objects.filter(available=True).order_by('-created_at')
    paginator = Paginator(properties_list, 6)  # 6 per page
    page_number = request.GET.get('page')
    properties = paginator.get_page(page_number)
    return render(request, 'bookings/index.html', {'properties': properties})

# -------------------------
# Property Detail Page
# -------------------------
def property_detail(request, property_id):
    """Show property details and map"""
    property = get_object_or_404(Property, pk=property_id)

    latitude = None
    longitude = None
    bbox = None

    if property.location:
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {"q": property.location, "format": "json"}
            headers = {"User-Agent": "my-django-app"}
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            if data:
                latitude = float(data[0]["lat"])
                longitude = float(data[0]["lon"])
                delta_lat = 0.015
                delta_lon = 0.025
                bbox = {
                    "min_lat": latitude - delta_lat,
                    "max_lat": latitude + delta_lat,
                    "min_lon": longitude - delta_lon,
                    "max_lon": longitude + delta_lon,
                }
        except Exception as e:
            print("Geocoding failed:", e)

    return render(request, "bookings/property_detail.html", {
        "property": property,
        "latitude": latitude,
        "longitude": longitude,
        "bbox": bbox,
    })


@login_required
def create_booking(request, property_id):
    """Create a new booking"""
    property = get_object_or_404(Property, id=property_id)
    user = request.user

    # Prevent owners from booking their own property
    if property.owner == user:
        messages.error(request, "Owners cannot book their own property.")
        return redirect('property_detail', property_id=property.id)

    if request.method == "POST":
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        num_guests = request.POST.get('num_guests')

        # Validation
        errors = False
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, "Invalid date format.")
            errors = True
        else:
            if check_in_date.weekday() != 5 or check_out_date.weekday() != 5:
                messages.error(request, "Bookings must start and end on a Saturday.")
                errors = True
            if (check_out_date - check_in_date).days != 7:
                messages.error(request, "Bookings must be exactly 7 nights (Saturday to Saturday).")
                errors = True

        try:
            num_guests_int = int(num_guests)
            if num_guests_int < 1 or num_guests_int > property.max_guests:
                messages.error(request, f"Number of guests must be between 1 and {property.max_guests}.")
                errors = True
        except (ValueError, TypeError):
            messages.error(request, "Invalid number of guests.")
            errors = True

        if not errors:
            total_price = property.price_per_night * 7
            Booking.objects.create(
                guest=user,
                property=property,
                check_in=check_in_date,
                check_out=check_out_date,
                num_guests=num_guests_int,
                total_price=total_price,
                status='confirmed'
            )
            messages.success(request, "Booking confirmed!")
            return redirect('my_bookings')

    return redirect('property_detail', property_id=property.id)

@login_required
def my_bookings(request):
    """View all your bookings"""
    bookings = Booking.objects.filter(guest=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def edit_booking(request, booking_id):
    """Edit an existing booking via Ajax"""
    booking = get_object_or_404(Booking, pk=booking_id, guest=request.user)

    if request.method == 'POST':
        try:
            check_in = request.POST.get('check_in')
            check_out = request.POST.get('check_out')
            num_guests = request.POST.get('num_guests')

            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            num_guests_int = int(num_guests)

            # Prevent owner from booking their own property
            # Prevent owner from booking their own property
            if booking.property.owner == request.user:
                return JsonResponse({'success': False, 'error': "Owners cannot book their own property."})


            # Validate dates
            if check_in_date.weekday() != 5 or check_out_date.weekday() != 5:
                return JsonResponse({'success': False, 'error': "Check-in and check-out must be Saturdays."})
            if (check_out_date - check_in_date).days != 7:
                return JsonResponse({'success': False, 'error': "Bookings must be exactly 7 nights."})

            # Validate max guests
            if num_guests_int < 1 or num_guests_int > booking.property.max_guests:
                return JsonResponse({'success': False, 'error': f"Maximum guests allowed: {booking.property.max_guests}"})

            # Update booking
            booking.check_in = check_in_date
            booking.check_out = check_out_date
            booking.num_guests = num_guests_int
            booking.total_price = booking.property.price_per_night * 7
            booking.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def delete_booking(request, booking_id):
    """Delete/cancel a booking via Ajax"""
    booking = get_object_or_404(Booking, pk=booking_id, guest=request.user)

    if request.method == 'POST':
        try:
            booking.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'bookings/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')

        if password != confirmation:
            messages.error(request, 'Passwords must match')
            return render(request, 'bookings/register.html')

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            login(request, user)
            return redirect('index')
        except:
            messages.error(request, 'Username already taken')

    return render(request, 'bookings/register.html')
