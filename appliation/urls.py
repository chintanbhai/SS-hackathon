from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.consumer_logout, name='consumer_logout'),
    path('index/', views.index, name='index'),
    path('', views.consumer_dashboard, name='home'),
    path('signup/', views.consumer_signup, name='consumer_signup'),
    path('signin/', views.consumer_signin, name='consumer_signin'),
    path('dashboard/', views.consumer_dashboard, name='consumer_dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/order/', views.place_order, name='place_order'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:pk>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('api/', views.api_home, name='api_home'),
    path('api/chat/', views.chat_api, name='chat_api'),  # Chat API endpoint
    # path('about/', views.about, name='about'),
    # path('contact/', views.contact, name='contact'),
]