from .cart import Cart

def cart(request):
    """
    این تابع سبد خرید را به عنوان یک متغیر سراسری به تمام صفحات HTML می‌فرستد
    """
    return {'cart': Cart(request)}