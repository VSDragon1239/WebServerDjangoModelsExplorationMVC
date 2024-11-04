# AppName/urls.py
from django.urls import path
from AppName.views import IndexView, CategoriesView, ProductsView, ProductCardView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),               # Главная страница
    path('categories/', CategoriesView.as_view(), name='categories'),  # Страница продуктов
    path('categories/<int:pk>', ProductsView.as_view(), name='products'),  # Страница продуктов
    path('categories/<int:pk>/<int:pk2>', ProductCardView.as_view(), name='card_product'),  # Страница продуктов
]
