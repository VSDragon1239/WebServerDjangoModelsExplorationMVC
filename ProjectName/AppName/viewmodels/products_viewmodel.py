from AppName.models import Product


class ProductsViewModel:
    def __init__(self):
        self.products = []
        self.filter_products_bool = False
        self.filter_type = 'id'

    def load_products(self, filter=False, filter_array=None):
        """Загружает все продукты из базы данных."""
        if not filter:
            self.products = Product.objects.all()
        else:
            # Фильтрация по полю `category_id`
            if self.filter_type == 'category_id' and filter_array:
                self.products = Product.objects.filter(category_id=int(filter_array))
            else:
                self.products = Product.objects.all()

    def get_products(self, filter_array=''):
        """Используем, чтобы получить данные продуктов в интерфейс"""
        # print(filter_array)
        if not self.products and not self.filter_products_bool:
            self.load_products()
        elif self.filter_products_bool:
            self.load_products(filter=True, filter_array=filter_array)
        return self.products

    def filter_products(self):
        if self.filter_products_bool:
            self.filter_products_bool = False
        else:
            self.filter_products_bool = True

    def set_type_filter(self, type_filter: str):
        self.filter_type = type_filter

    def get_product(self, id):
        try:
            return Product.objects.get(pk=int(id))
        except Product.DoesNotExist:
            return None
