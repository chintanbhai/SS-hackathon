from django.urls import path, include
from .views import *

urlpatterns = [
    path('', farmer_home, name='farmer_home'),  # Farmer home page
]
