from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('home/', views.home, name='home_alt'),
    path('index/', views.home, name='index'),
    path('chatbot/', views.chatbot, name='chatbot'),  # Chatbot page
    
    # Consumer product browsing and ordering
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/order/', views.place_order, name='place_order'),
    
    # API endpoints
    path('api/', views.api_home, name='api_home'),
    path('api/chat/', views.chat_api, name='chat_api'),  # Chat API endpoint
    
    # Static pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

]