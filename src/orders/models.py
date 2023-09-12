from django.db import models
from django.utils import timezone

from customers.models import Customer
from products.models import Product

# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(Customer, models.CASCADE, related_name='orders')
    closed = models.BooleanField('Closed', default=False)
    shipped = models.BooleanField('Shipped', default=False)
    date_ordered = models.DateField('Date Ordered', default=timezone.now)

    @property
    def get_total_items(self) -> int:
        total = sum([item.quantity for item in self.items.all()])
        return total
    
    @property
    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.quantity * item.product.price
        
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField('Quantity', default=0)

    @property
    def get_total(self):
        return self.product.price * self.quantity


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, related_name='addresses', null=True, blank=True)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='address', null=True, blank=True)
    zip_code = models.CharField('Zip Code', max_length=20)
    city = models.CharField('City', max_length=255)
    state = models.CharField('State', max_length=255)
    address_line1 = models.CharField('Address Line 1', max_length=500)
    address_line2 = models.CharField('Address Line 2', max_length=500)