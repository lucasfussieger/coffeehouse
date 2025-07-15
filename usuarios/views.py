from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User 
from django.contrib.auth.hashers import make_password

#/product_details/<int:product_id>
#/delete_product/<int:product_id>
#/edit_product/<int:product_id>
#/carrinho
#/carrinho/item/<int:item_id>
#/finalizar_carrinho
#/pedidos
#/pedido/<int:pedido_id>/aprovar
#/store/produtos/<string:product_type>

def home(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        if request.POST.get('modo') == 'cadastrar':
            return redirect('cadastrar')
        return redirect('entrar')
    return render(request, 'home.html')

def entrar(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.warning(request, 'nome de usuário ou senha inválidos')
    return render(request, 'entrar.html')

def cadastrar(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']
        senha_confirmacao = request.POST['senha_confirmacao']
        user_type = request.POST['user_type']

        if User.objects.filter(email=email).exists():
            messages.warning(request, 'este email já está cadastrado! tente outro!')
            return redirect('cadastrar')

        if not nome or not email or not senha or not senha_confirmacao:
            messages.warning(request, 'nenhum campo pode ficar vazio')
            return redirect('cadastrar')

        if senha != senha_confirmacao:
            messages.warning(request, 'as senhas não batem')
            return render(request, 'cadastro.html')

        user = User(
            username=email,       
            email=email,
            nome=nome,
            user_type=user_type
        )
        user.set_password(senha)
        user.save()
        login(request, user)

        messages.success(request, f'bem vindo à CoffeHouse, {user.user_type} {user.nome}')
        return render(request, 'store.html')

    return render(request, 'cadastro.html')

@login_required
def profile_page(request):
    usuario = request.user
    return render(request, 'profile_page.html', {'usuario': usuario})

@login_required
def deletar_conta(request):
    request.user.delete()
    logout(request)
    messages.success(request, 'Conta deletada com sucesso.')
    return redirect('home')

@login_required
def edit_user(request):
    if request.user.user_type != 'cliente':
        
        messages.warning(request, 'pagina não disponível')
        return redirect('store')

    if request.method == 'POST':

        nome = request.POST['nome']

        if not nome:
            messages.warning(request, 'o nome não pode estar vazio')
            return redirect('edit_user')

        request.user.nome = nome
        request.user.save()

        messages.success(request, 'nome de usuário editado com sucesso!')
        return redirect('store')

    return render(request, 'edit_user.html', {'usuario': request.user})

@login_required
def lista_clientes(request):
    if request.user.user_type == 'vendedor':
        lista = User.objects.filter(user_type='cliente')
        return render(request, 'list.html', {'clientes': lista, 'usuario': request.user})
    else:
        return HttpResponse('URL indisponível')

@login_required
def cliente_details(request, cliente_id):
    usuario = get_object_or_404(User, id = cliente_id)
    return render(request, 'cliente_details.html', {'user': usuario, 'usuario': request.user})