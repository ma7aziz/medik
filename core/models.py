from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='categories/', blank=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductManager(models.Manager):
    def all(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(active=True, featured=True)

    # def top_selling(self):
    #     self.all().order_by('times_sold')
    def on_sale(self):
        return self.filter(sale_price__isnull=False)

    def covid(self):
        return self.filter(covid=True, active=True).order_by('-price')


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(allow_unicode=True, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = RichTextField()
    # color = models.CharField(max_length=50)
    price = models.IntegerField()
    sale_price = models.IntegerField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    times_sold = models.IntegerField(default=1)
    main_image = models.ImageField(upload_to='products/')
    image1 = models.ImageField(upload_to='products/', blank=True, null=True)
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/', blank=True, null=True)
    image4 = models.ImageField(upload_to='products/', blank=True, null=True)
    product_type = models.CharField(max_length=100, blank=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True)
    covid = models.BooleanField(default=False)
    objects = ProductManager()

    def __str__(self):
        return self.name
