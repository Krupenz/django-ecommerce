from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.TextField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class AuctionListing(models.Model):
    name = models.CharField(max_length=64)
    image = models.URLField(default="https://icon-library.com/images/no-image-icon/no-image-icon-0.jpg")
    description = models.TextField(max_length=512)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auctions")


class Comment(models.Model):
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    date = models.DateField()
    content = models.TextField(max_length=128)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username} {self.date}"


class Bid(models.Model):
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    amount = models.FloatField()
    date = models.DateField()

    class Meta:
        get_latest_by = "date"


class Watchlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchlists")