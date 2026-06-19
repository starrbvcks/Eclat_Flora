from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm

from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/product_list.html', {
        'category': category,
        'products': products,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
    })


def home(request):
    featured_products = Product.objects.filter(available=True)[:4]

    return render(request, 'shop/home.html', {
        'featured_products': featured_products,
    })


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    return render(request, 'shop/contact.html')


@staff_member_required
def dashboard(request):
    User = get_user_model()
    products = Product.objects.select_related('category')
    low_stock_products = products.filter(stock__gt=0, stock__lt=5)

    return render(request, 'dashboard/overview.html', {
        'stats': {
            'products': products.count(),
            'available': products.filter(available=True).count(),
            'orders': 0,
            'low_stock': low_stock_products.count(),
            'categories': Category.objects.count(),
            'users': User.objects.count(),
        },
        'recent_products': products.order_by('-updated')[:6],
        'low_stock_products': low_stock_products.order_by('stock')[:5],
        'active_panel': 'overview',
    })


@staff_member_required
def dashboard_products(request):
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    products = Product.objects.select_related('category').order_by('-updated')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(description__icontains=query)
        )

    if status == 'available':
        products = products.filter(available=True)
    elif status == 'hidden':
        products = products.filter(available=False)
    elif status == 'low':
        products = products.filter(stock__gt=0, stock__lt=5)
    elif status == 'out':
        products = products.filter(stock=0)

    return render(request, 'dashboard/products.html', {
        'products': products,
        'query': query,
        'status': status,
        'active_panel': 'products',
    })


@staff_member_required
def dashboard_orders(request):
    return render(request, 'dashboard/orders.html', {
        'active_panel': 'orders',
    })
