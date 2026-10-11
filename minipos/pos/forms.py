from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "price", "stock_quantity"]


from django.forms import inlineformset_factory
from .models import Sale, SaleItem


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["customer"]


class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ["product", "quantity"]


SaleItemFormSet = inlineformset_factory(Sale, SaleItem, form=SaleItemForm, extra=3)
