from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls', namespace='shop')), # اتصال صفحه اصلی
    path('cart/', include('cart.urls', namespace='cart')),
]

# این خط برای لود شدن عکس‌ها در محیط توسعه (Development) حیاتی است
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)