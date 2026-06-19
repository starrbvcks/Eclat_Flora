from .models import Category

def category_list(request):
    # نام تابع باید دقیقاً category_list باشد
    return {'categories': Category.objects.filter(parent__isnull=True)}