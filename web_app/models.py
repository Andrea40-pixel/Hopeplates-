from accounts.models import FoodDonation
from django.contrib.auth.models import User
from django.db import models
from django.db import models

class PickupRequest(models.Model):
    donation = models.ForeignKey(FoodDonation, on_delete=models.CASCADE)
    ngo = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ngo_requests")
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donor_requests")


    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ngo.username} → {self.donation.food_name}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class ContactDb(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    email=models.EmailField(max_length=100,null=True,blank=True)
    subject=models.CharField(max_length=100,null=True,blank=True)
    message=models.TextField()
