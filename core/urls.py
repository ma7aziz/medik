from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,  name='index'),
    path('shop', views.shop, name='shop'),
    path('product/<str:slug>', views.product, name='product'),
    path('contact-us', views.contact, name='contact'),
    path('search', views.search, name='search')
]
