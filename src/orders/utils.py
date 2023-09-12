import json
from products.models import Product
from orders.models import Order

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_total': 0, 'get_total_items': 0}
    cartitems = order['get_total_items']

    for key in cart:
        try:
            product = Product.objects.get(pk=key)

            cartitems += cart[key]['quantity']
            total = product.price * cart[key]['quantity']

            order['get_total'] += total
            order['get_total_items'] += cart[key]['quantity']

            item  = {
                'product':{
                    'pk': product.pk,
                    'slug': product.slug,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[key]['quantity'],
                'get_total': total
            }
            items.append(item)

        except:
            pass
            
    return {'cart_items': cartitems, 'order': order, 'items': items}


def get_cart_data(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, closed=False)
        items = order.items.all()
        cart_items = order.get_total_items

    else:
        cart_data = cookieCart(request)

        items = cart_data['items']
        order = cart_data['order']
        cart_items = cart_data['cart_items']

    return {
        'cart_items': cart_items,
        'items': items,
        'order': order
    }
