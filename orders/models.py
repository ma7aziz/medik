import string
import random
from core.models import Product
from django.db import models

# Create your models here.


class Cart(models.Model):
    session = models.CharField(max_length=200)
    item = models.ForeignKey('Cart_item', on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def cart_price(self):
        prices = []
        for c in self.cart_item_set.all():
            prices.append(c.total_price())
        return sum(prices)

    def cart_count(self):
        return self.cart_item_set.all().count()


class Cart_item(models.Model):
    shopping_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    time = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        if self.item.sale_price:
            total_price = self.qty * self.item.sale_price

        else:
            total_price = self.qty * self.item.price
        return total_price

    def __str__(self):
        return self.item.name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


STATUS_CHOICE = (
    (1, 'recieved'),
    (2, 'confirmed'),
    (3, 'shipped'),
    (4, 'delivered'),
)


class Order(models.Model):
    session = models.CharField(max_length=200)
    tracking_id = models.CharField(
        unique=True, max_length=40, blank=True, null=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICE, default=1, max_length=20)
    notes = models.TextField(blank=True)

    # objects = OrderManager()

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.tracking_id:
            new_id = random.randint(100000, 999999)
            unique = False
            while not unique:
                if Order.objects.all().filter(tracking_id=new_id):
                    unique = False
                else:
                    unique = True
                    self.tracking_id = new_id

        super(Order, self).save(*args, **kwargs)
