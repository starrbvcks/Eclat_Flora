from django.urls import path
from . import views

app_name = 'basket' # این دقیقاً همان namespace است که جنگو دنبالش می‌گشت!

urlpatterns = [
    path('', views.basket_detail, name='basket_detail'),
]