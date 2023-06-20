from django.db import models
from django.utils import timezone

from customers.models import Customer
from products.models import Product

# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(Customer, models.CASCADE, related_name='orders')
    closed = models.BooleanField('Closed', default=False)
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