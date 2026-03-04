from django.db import models
from django.contrib.auth.models import User

class ProfileDb(models.Model):
    USER_TYPE = (
        ('donor', 'Donor'),
        ('ngo', 'NGO'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE,
    )
    phone= models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username

class FoodDonation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    food_name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    location = models.CharField(max_length=200)
    expiry_date = models.DateField()
    image = models.ImageField(upload_to='food_images/',null=True, blank=True)


    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Accepted', 'Accepted'),
        ('Expired', 'Expired'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return self.food_name


