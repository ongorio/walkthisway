from django.shortcuts import render, redirect
from django.views import generic

from products.models import Product
from products.forms import ProductRegisterForm

template_prefix = 'products/'

class ProductListView(generic.ListView):
    template_name = template_prefix + 'product_list.html'
    model = Product
    context_object_name = 'products'


class ProductDetailView(generic.DetailView):
    template_name = template_prefix + 'product_detail.html'
    model = Product
    context_object_name = 'product'


class ProductCreateView(generic.CreateView):
    template_name = template_prefix + 'product_create.html'
    model = Product
    form_class = ProductRegisterForm


class ProductUpdateView(generic.UpdateView):
    template_name = template_prefix + 'product_update.html'
    model = Product
    form_class = ProductRegisterForm
    context_object_name = 'product'


class ProductDeleteView(generic.DeleteView):
    template_name = template_prefix + 'product_delete.html'
    model = Product
