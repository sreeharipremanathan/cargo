from django.db import models


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
    