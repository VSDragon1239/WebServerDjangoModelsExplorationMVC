# AppName/urls.py
from django.urls import path
from AppName.views import IndexView, ProductsView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),               # Главная страница
    path('products/', ProductsView.as_view(), name='products'),  # Страница продуктов
]
