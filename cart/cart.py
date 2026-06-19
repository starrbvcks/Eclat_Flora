from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request):
        """
        مقداردهی اولیه سبد خرید
        """
        self.session = request.session
        # تلاش برای گرفتن سبد خرید فعلی از سشنِ کاربر
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if not cart:
            # اگر کاربر سبد خریدی نداشت، یک دیکشنری خالی برایش در سشن می‌سازیم
            cart = self.session[settings.CART_SESSION_ID] = {}
            
        self.cart = cart
        
        
        def add(self, product, quantity=1, override_quantity=False):
            """
            اضافه کردن محصول به سبد خرید یا به‌روزرسانی تعداد آن
            """
            # در سشن، کلیدها باید حتماً رشته (String) باشند
            product_id = str(product.id) 
            
            # اگر این گل هنوز در سبد نیست، ساختار اولیه‌اش را می‌سازیم
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
                
            if override_quantity:
                # اگر کاربر در صفحه سبد خرید مستقیماً عدد جدیدی وارد کرد (مثلا گفت دقیقا ۵ تا میخوام)
                self.cart[product_id]['quantity'] = quantity
            else:
                # اگر کاربر در صفحه محصول دوباره دکمه "افزودن" را زد
                self.cart[product_id]['quantity'] += quantity
                
            self.save()

        def save(self):
            """
            علامت‌گذاری سشن به عنوان تغییریافته تا جنگو آن را در دیتابیس/مرورگر ذخیره کند
            """
            self.session.modified = True
            
        def remove(self, product):
            """
            حذف یک گل از سبد خرید
            """
            product_id = str(product.id)
            if product_id in self.cart:
                del self.cart[product_id]
                self.save()

        def __iter__(self):
            """
            پیمایش روی آیتم‌های سبد خرید و لود کردن آبجکت‌های واقعی از دیتابیس
            """
            product_ids = self.cart.keys()
            # فقط با یک کوئری (Query) تمام گل‌های موجود در سبد را از دیتابیس می‌گیریم
            products = Product.objects.filter(id__in=product_ids)
            
            # یک کپی موقت از سبد می‌سازیم تا آبجکت دیتابیس را به آن تزریق کنیم
            cart = self.cart.copy()
            for product in products:
                cart[str(product.id)]['product'] = product
                
            for item in cart.values():
                # قیمت را دوباره به Decimal تبدیل می‌کنیم تا در محاسبه ریاضی دقیق باشد
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

        def get_total_price(self):
            """
            محاسبه قیمت کلِ تمام آیتم‌های داخل سبد
            """
            return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

        def clear(self):
            """
            تخلیه کامل سبد خرید (پس از ثبت نهایی سفارش)
            """
            del self.session[settings.CART_SESSION_ID]
            self.save()