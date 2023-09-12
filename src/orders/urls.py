from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('add-product/', views.AddProductView.as_view(), name='add_product'),
    path('upate-orderitem/', views.UpdateOrderItemView.as_view(), name='update_orderitem'),
    path('order-detail/<int:pk>/',  views.OrderDetailView.as_view(), name='order_detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('success/', views.SuccessView.as_view(), name='success'),

]
