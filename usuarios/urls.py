#/
#/entrar
#/cadastrar
#/lista_clientes
#/cliente_details/<int:cliente_id>
#/edit_user/<int:cliente_id>
#/profile_page
#/deletar_conta

from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name = 'home'),
    path('entrar/', views.entrar, name = 'entrar'),
    path('cadastrar/', views.cadastrar, name = 'cadastrar'),
    path('profile_page/', views.profile_page , name = 'profile_page'),
    path('delete_user/', views.deletar_conta , name = 'delete_user'),
    path('edit_user/<int:cliente_id>', views.edit_user , name = 'edit_user'),
    path('cliente_list/', views.lista_clientes , name = 'cliente_list'),
    path('cliente_details/<int:cliente_id>', views.cliente_details, name = 'cliente_details')
]