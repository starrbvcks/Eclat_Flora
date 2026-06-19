from django.shortcuts import render, get_object_or_404
from .models import Product

# این تابع از قبل وجود داشت
def product_list(request):
    products = Product.objects.filter(available=True)
    return render(request, 'shop/product_list.html', {'products': products})

# این تابع جدید را اضافه کن
def product_detail(request, slug):
    # محصول را پیدا کن یا ارور 404 بده
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'shop/product_detail.html', {'product': product})