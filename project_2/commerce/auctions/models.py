from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True, primary_key=True)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=128)
    
    def __str__(self) -> str:
        return f"username: {self.username}, email: {self.email}"
    
    
class AuctionItem(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    description = models.TextField(max_length=1000)
    creation_year = models.IntegerField()
    starting_bid = models.PositiveIntegerField()
    image = models.TextField(max_length=1000, blank=True)
    category = models.CharField(blank=True, max_length=32)
    active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f"name of item: {self.name} dating to: {self.creation_year}."
    
class Bids(models.Model):
    bidding_item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, related_name="bidding_item")
    bidding_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidding_user")
    amount = models.PositiveIntegerField()
    # code = models.CharField(max_length=10, primary_key=True)

    def __str__(self) -> str:
        return f"Bid made on {self.bidding_item} by {self.bidding_user} for {self.amount}"

class Comments(models.Model):
    commented_item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, related_name="commented_item")
    commenting_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenting_user")
    comment = models.TextField(max_length=1000, primary_key=True)
    
    def __str__(self) -> str:
        return f"{self.commenting_user} commented on {self.commented_item} with the following message: {self.comment}"
    
class Watchlist(models.Model):
    watchlist_item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, related_name="watchlist_item")
    watchlist_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
    def __str__(self) -> str:
        return f"{self.watchlist_user} added {self.watchlist_item} to his watchlist"
    
    
    

    
    
    
    
    
