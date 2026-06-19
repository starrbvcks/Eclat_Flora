from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    # این فیلد کلیدِ ماجراست
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='subcategories'
    )

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    """مدل اصلی محصولات (گل‌ها) Éclat Floral"""
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="دسته‌بندی")
    name = models.CharField(max_length=200, verbose_name="نام گل")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name="توضیحات")
    
    # فیلد قیمت: دقیقاً برای قیمت‌هایی که گفتی داری
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت")
    
    # فیلد عکس: نیازمند کتابخانه Pillow که در بالا نصب کردیم
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="عکس محصول")
    
    # مدیریت موجودی گل‌ها
    stock = models.PositiveIntegerField(verbose_name="موجودی در انبار")
    available = models.BooleanField(default=True, verbose_name="موجود است؟")
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name