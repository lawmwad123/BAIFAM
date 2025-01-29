from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
# So i think i need only one app cos it not match to handele with your endpoint 1 with the endpoitn

class Car(models.Model):
    # Let me try to folow the kinda same structure
    # Now one thing is am going to add some data since Philip said free will since am done with the task
    name = models.CharField(max_length=256, default="Unnamed Car")
    make = models.CharField(max_length=256)
    model = models.CharField(max_length=256)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    external_id = models.CharField(max_length=100, unique=True, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.year} {self.make} {self.model}"

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"{self.year} {self.make} {self.model}"
        super().save(*args, **kwargs)

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-order_date']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.car}"

    def save(self, *args, **kwargs):
        if not self.total_amount:
            # So here i need to set a default price of 0 if car price is None
            self.total_amount = self.car.price if self.car.price is not None else Decimal('0.00')
        super().save(*args, **kwargs)

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']

    def __str__(self):
        return f"Image for {self.car}"
