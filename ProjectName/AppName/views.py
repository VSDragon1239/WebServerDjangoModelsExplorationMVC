# /views.py - Через класс - = ПРИМЕР =
from django.views.generic import TemplateView

from AppName.viewmodels.categories_viewmodel import CategoriesViewModel
from AppName.viewmodels.products_viewmodel import ProductsViewModel


class IndexView(TemplateView):
    template_name = 'index.html'


class CategoriesView(TemplateView):
    template_name = 'categories.html'

    CategoriesView = []
    categories = []
    # filter_categories = CategoriesView.filter_categories()
    filters_array = []

    def get(self, request, *args, **kwargs):
        self.initViewModel()
        self.filters_array = request.GET.get('filters', None)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.initViewModel()
        context = super().get_context_data(**kwargs)
        context["categories"] = self.categories
        return context

    def initViewModel(self):
        self.CategoriesView = CategoriesViewModel()
        self.categories = self.CategoriesView.get_categories()


class ProductsView(TemplateView):
    template_name = 'products.html'

    def get(self, request, *args, **kwargs):
        # Получаем значение `pk` из URL для фильтрации
        self.filters_array = kwargs.get('pk')
        self.initViewModel()

        # Отладочный вывод для проверки значений
        print(self.products, ' - ', self.filters_array)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Инициализируем ViewModel перед передачей данных в контекст
        self.initViewModel()

        # Получаем значение `pk` из URL
        pk = kwargs.get('pk')
        context = super().get_context_data(**kwargs)

        # Добавляем продукты в контекст
        context["products"] = self.products
        context["pk"] = pk

        return context

    def initViewModel(self):
        # Создаем новый экземпляр ViewModel при каждом вызове
        self.ProductsVM = ProductsViewModel()

        # Устанавливаем фильтрацию по `category_id`
        self.ProductsVM.set_type_filter('category_id')

        # Получаем отфильтрованные продукты, если задано значение `pk`
        if self.filters_array:
            self.ProductsVM.filter_products()
            self.products = self.ProductsVM.get_products(filter_array=self.filters_array)
        else:
            self.products = self.ProductsVM.get_products()


class ProductCardView(TemplateView):
    template_name = 'product_card.html'

    # categories = ProductsView.get_categories()
    # products = ProductsVM.get_products()
    # filter_categories = ProductsView.filter_categories()

    filters_array = []

    def get(self, request, *args, **kwargs):
        self.ProductsVM = ProductsViewModel()
        self.filter_products = self.ProductsVM.filter_products()
        self.filter_type = self.ProductsVM.set_type_filter('category_id')

        # self.filters_array.append(kwargs.get('pk'))
        self.filters_array1 = kwargs.get('pk1')
        self.filters_array2 = kwargs.get('pk2')
        # print(self.filters_array)
        self.products = self.ProductsVM.get_products(self.filters_array1)
        self.product = self.ProductsVM.get_product(self.filters_array2)
        print(self.products, self.product)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')  # Получаем значение pk
        pk2 = kwargs.get('pk2')  # Получаем значение pk2
        context = super().get_context_data(**kwargs)
        context["product"] = self.product
        context["pk"] = pk
        context["pk2"] = pk2
        return context
