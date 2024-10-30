from AppName.models import Product, Category


class ProductViewModel:
    def __init__(self):
        self.products = []
        self.category = []
        self.filter_categories_bool = False
        self.filter_products_bool = False

    def load_products(self, filter=False, filter_array='filter_array'):
        """Загружает все продукты из базы данных."""
        if not filter:
            self.products = Product.objects.all()
        else:
            filters = filter_array
            self.products = Product.objects.filter(filters)

    def load_category(self, filter=False, filter_array='filter_array'):
        """Загружает все категории из базы данных"""
        if not filter:
            self.category = Category.objects.all()
        else:
            filters = filter_array
            self.category = Category.objects.filter(filters)

    def get_categories(self, filter_array='filter_array'):
        """Используем, чтобы получить данные категорий в интерфейс"""
        if not self.category and not self.filter_categories_bool:
            self.load_category()
        elif self.filter_categories_bool:
            self.load_products(filter=True, filter_array=filter_array)
        return self.category

    def get_products(self, filter_array='filter_array'):
        """Используем, чтобы получить данные продуктов в интерфейс"""
        if not self.products and not self.filter_products_bool:
            self.load_products()
        elif self.filter_products_bool:
            self.load_products(filter=True, filter_array=filter_array)
        return self.products

    def filter_categories(self):
        if self.filter_categories_bool:
            self.filter_categories_bool = False
        else:
            self.filter_categories_bool = True

    def filter_products(self):
        if self.filter_products_bool:
            self.filter_products_bool = False
        else:
            self.filter_products_bool = True
