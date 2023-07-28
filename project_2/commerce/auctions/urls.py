from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("create_item", views.create_item, name="create_item"),
    path("listings/<str:listing_title>", views.show_listings, name="show_listings"),
    path("add_item_to_watchlist", views.add_item_watchlist, name="add_item_to_watchlist"),
    path("remove_from_watchlist", views.remove_item_watchlist, name="remove_item_watchlist"),
    path("place_bid", views.place_bid, name="place_bid"),
    path("close_auction", views.close_auction, name="close_auction"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("watchlists_page", views.watchlists_page, name="watchlists_page"),
    path("all_categories", views.all_categories, name="all_categories"),
    path("category_search", views.category_search, name="category_search")
]
