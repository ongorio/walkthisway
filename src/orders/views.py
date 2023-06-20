from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
import json

from products.models import Product
from orders.models import Order, OrderItem

# Create your views here.
class AddProductView(generic.View):
    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)

        customer = request.user.customer
        product = Product.objects.get(pk=data['productId'])

        if product.quantity >= 1:
            order, created = Order.objects.get_or_create(customer=customer,closed=False)
            orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
            orderitem.quantity = orderitem.quantity + 1
            orderitem.save()

            return JsonResponse('Item Added', safe=False)

        return JsonResponse('Item Failed to add!', safe=False)
        

class CartView(generic.View):
    template_name = 'cart.html'
    def get(self, request, *args, **kwargs):
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, closed=False).first()
        # print()

        return render(request, self.template_name, {'cart': order})