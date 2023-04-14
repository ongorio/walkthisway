from django import forms

from products.models import Product

class ProductRegisterForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name', 'description', 'price', 'image', 'quantity'
        )
        

    field_order = [
        'name', 'price', 'quantity',
        'description','image'
    ]
