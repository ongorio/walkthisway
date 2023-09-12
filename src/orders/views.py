from django.shortcuts import render, redirect
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.urls import reverse
import json
import stripe

from products.models import Product
from orders.models import Order, OrderItem, ShippingAddress
from orders.forms import ShippingForm
from orders.utils import get_cart_data

from datetime import date

stripe.api_key = settings.STRIPE_SECRET_KEY

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


class UpdateOrderItemView(generic.View):
    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)

        action = data['action']
        customer = request.user.customer
        product = Product.objects.get(pk=data['productId'])

        order, created = Order.objects.get_or_create(customer=customer,closed=False)
        orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)


        if action == 'add':
            if product.quantity >= 1 and product.quantity >= orderitem.quantity + 1:
                print('adding')
                orderitem.quantity += 1

        elif action == 'remove':
            if orderitem.quantity > 0:
                orderitem.quantity -= 1

        orderitem.save()

        if orderitem.quantity == 0:
            orderitem.delete()

        return JsonResponse('Item Updated!', safe=False)


class OrderDetailView(generic.DetailView):
    template_name = 'order_detail.html'
    model = Order
    context_object_name = 'order'


class CartView(generic.View):
    template_name = 'cart.html'
    def get(self, request, *args, **kwargs):
        context = {}
        # customer = request.user.customer
        # order, _ = Order.objects.get_or_create(customer=customer, closed=False)

        cart = get_cart_data(self.request)

        context['order'] = cart['order']
        context['items'] = cart['items']
        context['cart_items'] = cart['cart_items']


        return render(request, self.template_name, context)
    

class CheckoutView(generic.View):
    template_name = 'checkout.html'
    form_class = ShippingForm


    def get(self, request, *args, **kwargs):
        context = {}
        form = self.form_class()
        # customer = request.user.customer
        # order = Order.objects.filter(customer=customer, closed=False).first()

        cart = get_cart_data(request)

        context['order'] = cart['order']
        context['items'] = cart['items']

        # context['order'] = order
        context['address_form'] = form
        return render(request, self.template_name, context)
    
    
    def post(self, request, *args, **kwargs):
        context = {}

        form = self.form_class(request.POST)
        
        if form.is_valid():
            shipping_address: ShippingAddress = form.save(commit=False)
            customer = request.user.customer
            order = Order.objects.filter(customer=customer, closed=False).first()

            shipping_address.customer = customer
            shipping_address.order = order
            
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency':'mxn',
                            'unit_amount': str(int(order.get_total*100)),
                            'product_data': {
                                'name': 'Orden'
                            }
                        },
                        'quantity': str(order.get_total_items),
                    }
                ],
                customer_email=customer.user.email,
                mode='payment',
                success_url = settings.SITE_URL + reverse('orders:success'),
                cancel_url = settings.SITE_URL + reverse('orders:cart'),
                metadata={'order_pk': order.pk, 'customer_pk': customer.pk}
            )

            return redirect(checkout_session.url)
        
        context['form'] = form

        return render(request, self.template_name, context=context)


class SuccessView(generic.TemplateView):
    template_name = 'success.html'


# Stripe Fullfillment
@csrf_exempt
def my_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.ENDPOINT_SECRET
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print(e)
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items']
        )

        order = Order.objects.get(pk=session.metadata.order_pk)

        for item in order.items.all():
            item.product.quantity -= item.quantity
            item.product.save()

        order.closed = True
        order.date_ordered = date.today()
        order.save()


    return HttpResponse(status=200)
