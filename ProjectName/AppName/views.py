# /views.py - Через класс - = ПРИМЕР =
from django.views.generic import TemplateView

from AppName.viewmodels.product_viewmodel import ProductViewModel as ProductViewModel


class IndexView(TemplateView):
    template_name = 'index.html'


class ProductsView(TemplateView):
    template_name = 'products.html'

    ProductViewModel = ProductViewModel()
    categories = ProductViewModel.get_categories()
    products = ProductViewModel.get_products()
    filter_categories = ProductViewModel.filter_categories()
    filter_products = ProductViewModel.filter_products()
    filters_array = []

    def get(self, request, *args, **kwargs):
        self.filters_array = request.GET.get('filters', None)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = self.categories
        context["products"] = self.products
        return context
