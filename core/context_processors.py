from .models import Product, Category
from orders.models import Cart


def add_variable_to_context(request):
    featured = Product.objects.featured()[:9]
    top_selling = Product.objects.all().order_by('-times_sold')[:3]
    cart = Cart.objects.all().filter(
        session=request.session.session_key, is_ordered=False).first()
    new_products = Product.objects.all().order_by('-timestamp')[:8]
    # delivery_charges = 40
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'featured': featured,
        'top_selling': top_selling,
        'cart': cart,
        'new_products': new_products
        # 'delivery_charges': delivery_charges
    }

    return context
