from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionItem, Bids


def index(request):
    bid_dict = {}
    all_bids = Bids.objects.all()
    for bid_item in all_bids:
        bid_dict[str(bid_item.bidding_item.name)] = bid_item.amount
    return render(request, "auctions/index.html", {
        "items": AuctionItem.objects.all(),
        "bids": bid_dict # AQUI ME QUEDE !!!!!!!!!!!!!!!!!!!!!!!
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    return render(request, "auctions/create_listing.html")

def create_item(request):
    if request.method == 'POST':
        listing_item = request.POST
    item = AuctionItem(name=listing_item["name"], description=listing_item["description"],
                creation_year=listing_item["creation_year"], starting_bid=listing_item["starting_bid"],
                image=listing_item["image"], category=listing_item["category"])
    item.save()
    return HttpResponseRedirect(reverse("index"))