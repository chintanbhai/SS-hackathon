from django.shortcuts import render
from .templates import *

# Create your views here.
def farmer_home(request):
    """Render the farmer home page"""
    return render(request, 'farmer/home.html')