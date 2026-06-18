from django.shortcuts import render
from .models import Product

def product_list(request):
    # فقط گل‌هایی که موجود هستند را فیلتر می‌کنیم
    products = Product.objects.filter(available=True)
    
    return render(request, 'shop/product_list.html', {'products': products})