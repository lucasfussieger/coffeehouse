from django.db import models
from usuarios.models import User

class Product(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    preco = models.CharField(max_length=100)
    descricao = models.CharField(max_length=200, blank=True, null=True)
    product_type = models.CharField(max_length=100)
    image = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=100)

    def __str__(self):
        return f'Order #{self.id}'

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_price = models.FloatField()
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f'{self.product_name} (x{self.quantity})'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.product.nome} (x{self.quantity})'
