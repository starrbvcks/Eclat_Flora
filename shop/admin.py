from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import format_html

from .models import Category, Product
from .price_utils import format_price_value


admin.site.site_header = "مدیریت Éclat Floral"
admin.site.site_title = "پنل مدیریت Éclat Floral"
admin.site.index_title = "مدیریت فروشگاه"


def toman(value):
    return format_html('<span class="ef-price">{} تومان</span>', format_price_value(value))


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'product_count', 'slug']
    list_filter = ['parent']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['parent']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(products_total=Count('products'))

    @admin.display(description="تعداد محصولات", ordering='products_total')
    def product_count(self, obj):
        return obj.products_total


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'image_thumb',
        'name',
        'category',
        'formatted_price',
        'stock',
        'stock_status',
        'available',
        'updated',
    ]
    list_display_links = ['image_thumb', 'name']
    list_editable = ['stock', 'available']
    list_filter = ['available', 'category', 'created', 'updated']
    list_select_related = ['category']
    search_fields = ['name', 'description', 'category__name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_preview', 'created', 'updated']
    date_hierarchy = 'created'
    ordering = ['-created']
    actions = ['make_available', 'make_unavailable']
    fieldsets = (
        ("اطلاعات اصلی", {
            'fields': ('name', 'slug', 'category', 'description'),
        }),
        ("قیمت و موجودی", {
            'fields': ('price', 'stock', 'available'),
        }),
        ("تصویر محصول", {
            'fields': ('image', 'image_preview'),
        }),
        ("زمان‌بندی", {
            'classes': ('collapse',),
            'fields': ('created', 'updated'),
        }),
    )

    @admin.display(description="تصویر")
    def image_thumb(self, obj):
        if not obj.image:
            return format_html('<span class="ef-empty-thumb">{}</span>', "بدون عکس")

        return format_html(
            '<img class="ef-thumb" src="{}" alt="{}" />',
            obj.image.url,
            obj.name,
        )

    @admin.display(description="قیمت", ordering='price')
    def formatted_price(self, obj):
        return toman(obj.price)

    @admin.display(description="پیش‌نمایش تصویر")
    def image_preview(self, obj):
        if not obj.image:
            return "هنوز عکسی ثبت نشده است."

        return format_html(
            '<img class="ef-preview" src="{}" alt="{}" />',
            obj.image.url,
            obj.name,
        )

    @admin.display(description="وضعیت انبار", ordering='stock')
    def stock_status(self, obj):
        if obj.stock == 0:
            return format_html('<span class="ef-badge ef-badge-danger">{}</span>', "ناموجود")
        if obj.stock < 5:
            return format_html('<span class="ef-badge ef-badge-warning">{}</span>', "کم‌موجودی")
        return format_html('<span class="ef-badge ef-badge-success">{}</span>', "موجود")

    @admin.action(description="فعال کردن محصولات انتخاب‌شده")
    def make_available(self, request, queryset):
        updated = queryset.update(available=True)
        self.message_user(request, f"{updated} محصول فعال شد.")

    @admin.action(description="غیرفعال کردن محصولات انتخاب‌شده")
    def make_unavailable(self, request, queryset):
        updated = queryset.update(available=False)
        self.message_user(request, f"{updated} محصول غیرفعال شد.")


def eclat_dashboard(request):
    User = get_user_model()
    products = Product.objects.select_related('category')
    recent_products = products.order_by('-updated')[:6]

    context = {
        **admin.site.each_context(request),
        'title': 'داشبورد فروشگاه',
        'stats': {
            'products': products.count(),
            'available': products.filter(available=True).count(),
            'hidden': products.filter(available=False).count(),
            'low_stock': products.filter(stock__gt=0, stock__lt=5).count(),
            'out_stock': products.filter(stock=0).count(),
            'categories': Category.objects.count(),
            'users': User.objects.count(),
        },
        'recent_products': recent_products,
    }
    return TemplateResponse(request, 'admin/eclat_dashboard.html', context)


default_get_urls = admin.site.get_urls


def get_admin_urls():
    custom_urls = [
        path('eclat-dashboard/', admin.site.admin_view(eclat_dashboard), name='eclat_dashboard'),
    ]
    return custom_urls + default_get_urls()


admin.site.get_urls = get_admin_urls
