from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название", blank=True)
    slug = models.SlugField(verbose_name="Slug", max_length=150)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Category({self.name})"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название", blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(verbose_name="Цена", max_digits=10, decimal_places=2)
    descriptions = models.TextField(verbose_name="Описание", blank=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name
