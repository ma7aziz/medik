from django.urls import path
from . import views

urlpatterns = [
    path('cart', views.cart, name='cart'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('place_order', views.place_order, name='place_order')
]
