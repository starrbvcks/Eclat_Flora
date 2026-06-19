
from django.shortcuts import render

def basket_detail(request):
    # فعلاً یک صفحه خالی برمی‌گردانیم تا ارور برطرف شود
    return render(request, 'basket/detail.html')