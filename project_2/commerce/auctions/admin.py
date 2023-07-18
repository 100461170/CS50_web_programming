from django.contrib import admin
from .models import User, AuctionItem, Bids, Comments

# Register your models here.
admin.site.register(User)
admin.site.register(AuctionItem)
admin.site.register(Bids)
admin.site.register(Comments)