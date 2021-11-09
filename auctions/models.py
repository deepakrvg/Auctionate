from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=64, blank=True, default="")
    price = models.PositiveIntegerField()
    user_id = models.PositiveIntegerField(blank=True)
    image = models.CharField(max_length=5000, blank=True, default="")
    description = models.CharField(max_length=500, blank=True, default="")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}:-- name: {self.name} category: {self.category} price: {self.price} image: {self.price} description: {self.description} time: {self.time}"

class Bids(models.Model):
    bid_price = models.PositiveIntegerField()
    user_id = models.IntegerField(blank=True, default=0)
    item_number = models.IntegerField(blank=True, default=0)
    time = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    comment = models.CharField(max_length=500)
    user_id = models.IntegerField(blank=True, default=0)
    item_number = models.IntegerField(blank=True, default=0)
    username = models.CharField(max_length=64, blank=True, default="")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}:-- {self.comment} {self.user_id} {self.username} {self.item_number}"

class WatchList(models.Model):
    name = models.CharField(max_length=64)
    user_name = models.CharField(max_length=64)
    price = models.IntegerField()
    image = models.CharField(max_length=500, blank=True)
    item_number = models.IntegerField(default=0)

class WinBid(models.Model):
    item_number = models.IntegerField()
    user_id = models.IntegerField()
    name = models.CharField(max_length=64)
    user_name = models.CharField(max_length=64)
    price = models.IntegerField()
    image = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.user_name} bought {self.name} for {self.price}"
