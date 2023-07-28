from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionItem, Bids, Watchlist, Comments


def index(request):
    all_bids = Bids.objects.all()
    return render(request, "auctions/index.html", {
        "items": AuctionItem.objects.all(),
        "bids": all_bids 
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
    item = AuctionItem(name=listing_item["name"], owner=request.user, description=listing_item["description"],
                creation_year=listing_item["creation_year"], starting_bid=listing_item["starting_bid"],
                image=listing_item["image"], category=listing_item["category"])
    item.save()
    return HttpResponseRedirect(reverse("index"))

def show_listings(request, listing_title):
    all_listings = AuctionItem.objects.all()
    for item in all_listings:
        if item.name == listing_title:
            searched_item = item
    all_bids = Bids.objects.all()
    searched_bid = None
    for item in all_bids:
        if item.bidding_item.name == searched_item.name:
            searched_bid = item
    watchlist_item = None
    all_watchlists = Watchlist.objects.all()
    for item in all_watchlists:
        if item.watchlist_item == searched_item:
            watchlist_item = item
    return render(request, "auctions/listings.html", {
        "auction_item": searched_item,
        "current_bid": searched_bid,
        "watchlist_item": watchlist_item,
        "owner": request.user,
        "comments": Comments.objects.all()
    })
            
def add_item_watchlist(request):
    if request.method == "POST":
        user_item = request.POST
    item_search_name = user_item["auction_item"]
    all_auctions = AuctionItem.objects.all()
    for item in all_auctions:
        if item.name == item_search_name:
            watchlist_auction_item = item
    watchlist_item = Watchlist(watchlist_item=watchlist_auction_item, 
                               watchlist_user=request.user)
    watchlist_item.save()
    return HttpResponseRedirect(reverse("index"))
    
def remove_item_watchlist(request):
    if request.method == "POST":
        auction_post = request.POST
    auction_item = auction_post["auction_item"]
    for item in Watchlist.objects.all():
        if item.watchlist_item.name == auction_item and item.watchlist_user == request.user:
            Watchlist.objects.filter(id=item.id).delete()
    return HttpResponseRedirect(reverse("index"))

def place_bid(request):
    if request.method == "POST":
        post_item = request.POST
    auction_item_name = post_item["auction_item"]
    bid_value = int(post_item["bid_value"])
    for item in AuctionItem.objects.all():
        if item.name == auction_item_name:
            auction_item = item
    if auction_item.starting_bid >= bid_value:
        return render(request, "auctions/error_page.html")
    bids_on_item = Bids.objects.filter(bidding_item=auction_item)
    for item in bids_on_item:
        if item.amount >= bid_value:
            return render(request, "auctions/error_page.html")
    Bids(bidding_item=auction_item, bidding_user=request.user, amount=bid_value).save()
    return HttpResponseRedirect(reverse("index"))

def close_auction(request):
    if request.method == "POST":
        post_item = request.POST
    auction_item_name = post_item["auction_item"]
    for item in AuctionItem.objects.all():
        if item.name == auction_item_name:
            auction_item = item
    auction_item.active = False
    auction_item.save()
    return HttpResponseRedirect(reverse("index"))

def add_comment(request):
    if request.method == "POST":
        post_item = request.POST
    comment_text = post_item["comment"]
    auction_item_name = post_item["auction_item"]
    for item in AuctionItem.objects.all():
        if item.name == auction_item_name:
            auction_item = item
    Comments(commented_item=auction_item, commenting_user=request.user, comment=comment_text).save()
    return HttpResponseRedirect(reverse("index"))

def watchlists_page(request):
    watchlist_items = []
    user = request.user
    for item in Watchlist.objects.all():
        if item.watchlist_user == user:
            watchlist_items.append(item)
    return render(request, "auctions/watchlist_page.html", {
        "watchlist_items": watchlist_items
    })

def all_categories(request):
    categories = []
    for item in AuctionItem.objects.all():
        if item.category != "":
            categories.append(item.category)
    return render(request, "auctions/all_categories.html", {
        "categories": categories
    })
def category_search(request):
    if request.method == "POST":
        post_item = request.POST
    auction_items = []
    category = post_item["category"]
    for item in AuctionItem.objects.all():
        if item.category == category:    
            auction_items.append(item)
    return render(request, "auctions/index.html", {
        "items": auction_items,
        "bids": Bids.objects.all()
    })