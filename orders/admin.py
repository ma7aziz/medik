from django.contrib import admin
from .models import Cart_item, Cart, Order
# Register your models here.
admin.site.register(Cart)
admin.site.register(Cart_item)
admin.site.register(Order)
