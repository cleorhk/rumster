from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):

    BUSINESS = 'business'
    RESIDENTIAL = 'residential'
    LISTING_CHOICES = [
        (BUSINESS, 'Business'),
        (RESIDENTIAL, 'Residential'),
    ]
    # Choices for county field
    COUNTY_CHOICES = [
        ('Nairobi', 'Nairobi'),
        ('Mombasa', 'Mombasa'),
    ]

    title = models.CharField(max_length=255)
    county = models.CharField(max_length=50, choices=COUNTY_CHOICES)  # Up
    type = models.CharField(max_length=20, choices=LISTING_CHOICES,default=RESIDENTIAL)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)  # New field

    def __str__(self):
        return self.title


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} to {self.recipient.username}: {self.content}"
