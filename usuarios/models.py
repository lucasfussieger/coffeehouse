from django.db import models
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    nome = models.CharField(max_length=100)
    user_type = models.CharField(max_length=50)

    def verificar_senha(self, senha):
        return check_password(senha, self.senha)

    def __str__(self):
        return self.nome
