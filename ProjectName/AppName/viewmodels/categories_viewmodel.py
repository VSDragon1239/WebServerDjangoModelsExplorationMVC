from AppName.models import Category


class CategoriesViewModel:
    def __init__(self):
        self.category = []
        self.filter_categories_bool = False
        self.filter_products_bool = False

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
            self.load_category(filter=True, filter_array=filter_array)
        return self.category

    def filter_categories(self):
        if self.filter_categories_bool:
            self.filter_categories_bool = False
        else:
            self.filter_categories_bool = True
