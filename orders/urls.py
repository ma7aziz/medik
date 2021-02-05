from django.urls import path
from . import views

urlpatterns = [
    path('cart', views.cart, name='cart'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('plus_cart', views.plus_cart, name='plus_cart'),
    path('minus_cart', views.minus_cart, name='minus_cart'),
    path('delete_cart/<int:cart_id>', views.delete_cart, name='delete_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('place_order', views.place_order, name='place_order')
]
