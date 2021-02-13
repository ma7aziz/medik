from django.shortcuts import render
from .models import Product, Category
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect

# Create your views here.


def index(request):

    if not request.session or not request.session.session_key:
        request.session.save()
    print(request.session.session_key)
    return render(request, 'core/index.html')


def product(request, slug):
    product = Product.objects.get(slug=slug)
    category = product.category
    brand = product.brand
    related = Product.objects.all().exclude(name=product.name).filter(Q(category=category) |
                                                                      Q(brand=brand)).order_by('-price')[:3]
    # reviews = Review.objects.all().filter(product = product).order_by('-timestamp')
    # reviews_count = reviews.count()
    context = {
        'product': product,
        'related': related
    }

    return render(request, 'core/product.html', context)


def category(request, category):
    category = Category.objects.all().filter(name=category)[0]
    products = Product.objects.all().filter(category=category)
    paginator = Paginator(products, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    recent = Product.objects.all().order_by('-timestamp')[:4]
    context = {'page_obj': page_obj,
               'category': category,
               'recent': recent}
    return render(request, 'core/category.html', context)


def shop(request):
    products = Product.objects.all()
    paginator = Paginator(products, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    recent = Product.objects.all().order_by('-timestamp')[:3]
    return render(request, 'core/shop.html', {'page_obj': page_obj, 'recent': recent})


def contact(request):
    return render(request, 'core/contact.html')


def search(request):
    keyword = request.GET.get('s').strip()
    result = Product.objects.filter(Q(name__icontains=keyword) | Q(
        description__icontains=keyword))

    return render(request, 'core/search_results.html', {'result': result, 'keyword': keyword})


# filter shop
def filter(request):
    q = request.GET.get('q')
    print(q)
    return HttpResponseRedirect('shop')


# filter category
