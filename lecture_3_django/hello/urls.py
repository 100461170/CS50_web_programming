from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tomas", views.tomas, name="tomas"),
    path("david", views.david, name="david"),
    path("<str:name>", views.greet, name="greet")
]