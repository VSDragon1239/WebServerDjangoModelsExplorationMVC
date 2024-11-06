from django import forms

from AppName.models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)


class CategoryEditForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'descriptions', )


class ProductsEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'price', 'descriptions', )
