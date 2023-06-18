from django import forms

from products.models import Product

class ProductRegisterForm(forms.ModelForm):
    price = forms.DecimalField(min_value=0)
    quantity = forms.IntegerField(min_value=0)

    class Meta:
        model = Product
        fields = (
            'name', 'description', 'price', 'image', 'quantity'
        )
        

    field_order = [
        'name', 'price', 'quantity',
        'description','image'
    ]
