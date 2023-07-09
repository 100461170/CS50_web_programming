from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path('search', views.search, name="search"),
    path('create', views.create, name="create"),
    path('create_page', views.create_page, name="create_page"),
    path("edit", views.edit, name="edit"),
    path("edit_page", views.edit_page, name="edit_page"),
    path("random_page", views.random_page, name="random page")
]
