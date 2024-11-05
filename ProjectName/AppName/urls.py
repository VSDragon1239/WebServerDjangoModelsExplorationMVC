# AppName/urls.py
from django.urls import path
from AppName.views import IndexView, CategoriesView, ProductsView, ProductCardView, ChangeCategoryView, AddCategoryView, AddProductView, ChangeProductView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),                                                 # Главная страница
    path('categories/', CategoriesView.as_view(), name='categories'),                           # Страница категорий
    path('categories/<int:pk>', ProductsView.as_view(), name='products'),                       # Страница продуктов
    path('categories/<int:pk>/products/<int:pk2>', ProductCardView.as_view(), name='card_product'),      # Страница продукта

    path('categories/<int:pk>/change', ChangeCategoryView.as_view(), name='change_category'),      # Страница изменения выбранной категории
    path('categories/add', AddCategoryView.as_view(), name='add_category'),      # Страница изменения категорий (добавить)
    path('categories/<int:pk>/products/add', AddProductView.as_view(), name='add_product'),      # Страница изменения продуктов
    path('categories/<int:pk>/products/<int:pk2>/change', ChangeProductView.as_view(), name='change_product'),      # Страница изменения продукта
]
