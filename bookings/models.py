from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.IntegerField()
    bedrooms = models.IntegerField()
    
    # Owner
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    
    # Image
    image = models.ImageField(upload_to='properties/', blank=True, null=True)
    
    # Availability
    available = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Properties"

class Booking(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    
    check_in = models.DateField()
    check_out = models.DateField()
    num_guests = models.IntegerField()
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Confirmed')
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.guest.username} - {self.property.title}"
    
    def calculate_total(self):
        nights = (self.check_out - self.check_in).days
        return self.property.price_per_night * nights