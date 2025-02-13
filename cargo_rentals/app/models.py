from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category= models.TextField()

class Car(models.Model):
    
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    image = models.FileField()
    fuel = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    num_of_seats = models.IntegerField()
    price_per_day = models.IntegerField()
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    

class Rental(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.car.name} ({self.status})"
    