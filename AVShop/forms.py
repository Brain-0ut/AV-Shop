from django.forms import ModelForm

from AVShop import models


class ProductForm(ModelForm):
    class Meta:
        model = models.Product
        exclude = ('is_deleted', 'author', 'deleted_at')
