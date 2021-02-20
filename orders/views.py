from core.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator

from .models import Cart, Cart_item, Customer, Order

# Create your views here.


def cart(request):
    return render(request, 'orders/cart.html')


def add_to_cart(request):
    if not request.session or not request.session.session_key:
        request.session.save()
    product = Product.objects.get(id=request.POST.get('product_id'))
    if request.POST.get('qty'):
        qty = request.POST.get('qty')
    else:
        qty = 1
    cart = Cart.objects.all().filter(
        session=request.session.session_key, is_ordered=False).first()
    if cart:
        cart_item = Cart_item.objects.all().filter(
            shopping_cart=cart, item=product).first()
        if cart_item:
            if qty:
                cart_item.qty += int(qty)
                cart_item.save()
                messages.success(request, 'تم أضافة المنتج الي السلة')
            else:
                cart_item.qty += 1
                cart_item.save()
                messages.success(request, 'تم أضافة المنتج الي السلة')

        else:
            cart_item = Cart_item(
                shopping_cart=cart, item=product, qty=qty)
            cart_item.save()
            messages.success(request, 'تم أضافة المنتج الي السلة')

    else:
        cart = Cart(session=request.session.session_key)
        cart.save()
        cart_item = Cart_item(
            item=product, shopping_cart=cart)
        cart_item.save()
        messages.success(request, 'تم أضافة المنتج الي السلة')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def plus_cart(request):
    """
    change product quantitiy in cart (plus)
    """

    cart_item = Cart_item.objects.get(pk=request.GET.get('product_id'))
    cart_item.qty += 1
    cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def minus_cart(request):
    """
    change product quantitiy in cart (minus)
    """
    cart_item = Cart_item.objects.get(pk=request.GET.get('product_id'))
    if cart_item.qty > 1:
        cart_item.qty -= 1
        cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_cart(request, cart_id):
    """
    Remove product from cart 
    """
    cart = Cart_item.objects.get(id=cart_id)
    cart.delete()
    messages.success(request, 'تم حذف المنتج')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def checkout(request):
    return render(request, 'orders/checkout.html')


def place_order(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    address = request.POST['address']
    city = request.POST['city']
    notes = request.POST['notes']
    session = request.session.session_key
    cart = Cart.objects.get(pk=request.POST['cart_id'])
    customer = Customer(name=name, address=address, city=city,
                        email=email, phone=phone)
    customer.save()
    price = cart.cart_price()
    order = Order(customer=customer, cart=cart,
                  notes=notes, price=price, session=session)
    order.save()
    cart.is_ordered = True
    cart.save()
    for pro in cart.cart_item_set.all():
        pro.item.times_sold += 1
        pro.item.save()
    return render(request, 'orders/order_success.html')


@user_passes_test(lambda u: u.is_superuser)
def orders(request):
    orders = Order.objects.all().order_by('-timestamp')
    paginator = Paginator(orders, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = orders.count()
    return render(request, 'admin/orders.html',
                  {'page_obj': page_obj,
                   # 'count': count,
                   # 'prices': orders_prices
                   }
                  )


@user_passes_test(lambda u: u.is_superuser)
def order_details(request, id):
    order = Order.objects.get(pk=id)
    return render(request, 'admin/order_details.html', {'order': order})


@user_passes_test(lambda u: u.is_superuser)
def update_status(request):
    order = Order.objects.get(pk=request.POST['order_id'])
    status = request.POST['status']
    order.status = int(status)
    order.save()
    messages.success(request, 'order status hs been updated !')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
