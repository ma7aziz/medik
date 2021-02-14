from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,  name='index'),
    path('shop', views.shop, name='shop'),
    path('product/<str:slug>', views.product, name='product'),
    path('category/<str:category>',  views.category, name='category'),
    path('shop/<str:brand>', views.brand,  name='brand'),
    path('contact-us', views.contact, name='contact'),
    path('search', views.search, name='search'),
    path('filter', views.filter, name='filter')
]
