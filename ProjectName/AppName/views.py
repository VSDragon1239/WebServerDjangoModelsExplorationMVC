# /views.py - Через класс - = ПРИМЕР =
from django.http import HttpRequest
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from AppName.viewmodels.categories_viewmodel import CategoriesViewModel
from AppName.viewmodels.products_viewmodel import ProductsViewModel

from AppName.forms import CategoryForm, CategoryEditForm, ProductsForm, ProductsEditForm

from AppName.models import Category, Product


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
        try:
            context["product"] = self.products[0]
        except IndexError as e:
            print(e)
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
        self.filters_array1 = kwargs.get('pk')
        print(self.filters_array1)
        self.filters_array2 = kwargs.get('pk2')
        # print(self.filters_array)
        self.products = self.ProductsVM.get_products(self.filters_array1)
        self.product = self.ProductsVM.get_product(self.filters_array2)
        print(self.products, self.product)
        # return super().get(request, *args, **kwargs)
        return self.render_to_response({
            'pk': self.filters_array1,
            'pk2': self.filters_array2,
            'products': self.products,
            'product': self.product,
        })

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')  # Получаем значение pk
        pk2 = kwargs.get('pk2')  # Получаем значение pk2
        context = super().get_context_data(**kwargs)
        context["product"] = self.product
        context["pk"] = pk
        context["pk2"] = pk2
        return context


class ChangeCategoryView(TemplateView):
    template_name = 'change_category.html'

    form = CategoryEditForm()

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        category = get_object_or_404(Category, pk=pk)
        form = CategoryEditForm(instance=category)
        return self.render_to_response({'form': form, 'pk': pk})

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        category = Category.objects.get(pk=pk)
        context['name'] = category.name
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        pk = kwargs.get('pk')
        print(pk, '[PK], АХАХАХ')

        if request.method == 'POST':
            category = Category.objects.get(pk=pk)
            form = CategoryEditForm(request.POST, instance=category)
            if form.is_valid():
                for attr, value in form.cleaned_data.items():
                    setattr(category, attr, value)
                category.slug = slugify(form.cleaned_data['name'], allow_unicode=True)
                category.save()
                return redirect(f'/categories/{pk}')
            return self.render_to_response({'form': form})


@method_decorator(csrf_protect, name='dispatch')
class AddCategoryView(TemplateView):
    template_name = 'add_category.html'
    form = CategoryForm()

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        # pk = kwargs.get('pk')
        # print(pk)
        if request.method == 'POST':
            # raise Exception()
            form = CategoryForm(request.POST)
            if form.is_valid():
                slug = slugify(form.cleaned_data['name'], allow_unicode=True)
                category = Category(**form.cleaned_data, slug=slug)
                category.save()
                print(slug, category)
                return redirect('/categories')
            return self.render_to_response({'form': form})


class AddProductView(TemplateView):
    template_name = 'add_product.html'

    form = ProductsForm()

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        category = get_object_or_404(Category, pk=pk)
        form = ProductsForm()
        return self.render_to_response({'form': form, 'category': category, 'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs.get('pk')
        context['form'] = self.form
        context['pk'] = pk
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        pk = kwargs.get('pk')
        category = get_object_or_404(Category, pk=pk)
        if request.method == 'POST':
            form = ProductsForm(request.POST)
            if form.is_valid():
                product = Product(**form.cleaned_data)
                product.category = category
                product.save()
                print(product)
                return redirect(f'/categories/{ pk }')
            return self.render_to_response({'form': form, 'category': category})


class ChangeProductView(TemplateView):
    template_name = 'change_product.html'

    form = ProductsForm()

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        pk2 = kwargs.get('pk2')
        product = get_object_or_404(Product, pk=pk2)
        form = ProductsEditForm(instance=product)
        return self.render_to_response({
            'form': form,
            'product': product,
            'pk': pk,
            'pk2': pk2,
        })

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        pk2 = kwargs.get('pk2')
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['pk'] = pk
        context['pk2'] = pk2
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        pk = kwargs.get('pk')
        pk2 = kwargs.get('pk2')
        product = Product.objects.get(pk=pk2)
        if request.method == 'POST':
            form = ProductsEditForm(request.POST, instance=product)
            if form.is_valid():
                for attr, value in form.cleaned_data.items():
                    setattr(product, attr, value)
                product.save()
                print(product)
                return redirect(f'/categories/{pk}/products/{pk2}')
            return self.render_to_response({'form': form})


class DeleteCategoryView(TemplateView):
    template_name = 'delete_category.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        category = get_object_or_404(Category, pk=pk)
        return self.render_to_response({'category': category, 'pk': pk})

    def post(self, request: HttpRequest, *args, **kwargs):
        pk = kwargs.get('pk')
        category = get_object_or_404(Category, pk=pk)

        # Удаляем категорию
        category.delete()
        return redirect('/categories')  # Перенаправляем на страницу со списком категорий


class DeleteProductView(TemplateView):
    template_name = 'delete_product.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')  # pk категории
        pk2 = kwargs.get('pk2')  # pk продукта
        product = get_object_or_404(Product, pk=pk2)
        return self.render_to_response({
            'product': product,
            'pk': pk,
            'pk2': pk2,
        })

    def post(self, request: HttpRequest, *args, **kwargs):
        pk = kwargs.get('pk')
        pk2 = kwargs.get('pk2')
        product = get_object_or_404(Product, pk=pk2)

        # Удаляем продукт
        product.delete()
        return redirect(f'/categories/{pk}')  # Перенаправляем на страницу со списком продуктов в категории
