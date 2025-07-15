from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.store, name='store'),
    path('register_product/', views.register_product, name='register_product'),
    path('product_details/<int:product_id>/', views.product_details, name='product_details'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('carrinho/item/<int:item_id>/', views.item_details, name='item_details'),
    path('finalizar_carrinho/', views.finalizar_carrinho, name='finalizar_carrinho'),
    path('orders/', views.order_list, name = 'order_list')
]


#/pedidos
#/pedido/<int:pedido_id>/aprovar
#/store/produtos/<string:product_type>
