
from django.shortcuts import render, get_object_or_404
from .models import Product
from cart.forms import CartAddProductForm
from django.http import HttpResponse

# این تابع از قبل وجود داشت
def product_list(request):
    products = Product.objects.filter(available=True)
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        # به جای ارور ۴۰۴، متن واقعی ارور را چاپ کن
        return HttpResponse(f"Product with slug '{slug}' not found in database!")
    
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product_detail.html', {
                'product': product,
                'cart_product_form': cart_product_form
    })  
    
def home(request):
    # انتخاب ۴ محصولِ منتخب برای نمایش در صفحه اصلی
    featured_products = Product.objects.filter(available=True)[:4]
    return render(request, 'shop/home.html', {'featured_products': featured_products})