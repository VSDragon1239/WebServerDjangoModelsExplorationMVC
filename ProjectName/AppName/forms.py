from django import forms

from AppName.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)


class CategoryEditForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
