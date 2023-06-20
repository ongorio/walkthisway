from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('add-product/', views.AddProductView.as_view(), name='add_product'),
    path('cart/', views.CartView.as_view(), name='cart')
]
