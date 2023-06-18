from django import forms

from products.models import Product

class ProductRegisterForm(forms.ModelForm):
    price = forms.DecimalField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    class Meta:
        
        model = Product
        fields = (
            'name', 'description', 'price', 'image', 'quantity'
        )
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'})
        }

    field_order = [
        'name', 'price', 'quantity',
        'description','image'
    ]
