from django.urls import path
from . import views

urlpatterns = [
    path('host/',views.index),
]