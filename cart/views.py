from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    """
    این تابع دیتای فرم را می‌گیرد و گل را به سبد خریدِ Session اضافه می‌کند
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
        
    # بعد از اضافه شدن، کاربر را به صفحه سبد خرید پاس می‌دهیم
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    """
    حذف کامل یک نوع گل از سبد خرید
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    
    return redirect('cart:cart_detail')
def cart_detail(request):
    """
    نمایش صفحه اصلی سبد خرید
    """
    cart = Cart(request)
    
    # یک ترفند مهندسی: فرم را برای تک‌تک گل‌های داخل سبد لود می‌کنیم 
    # تا کاربر بتواند همان‌جا تعداد را تغییر دهد (مثلاً ۲ دسته گل را بکند ۳ تا)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
            
    return render(request, 'cart/detail.html', {'cart': cart})