from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Product, Order, CartItem, OrderItem
from django.core.files.storage import default_storage
import uuid

@login_required
def store(request):
    produtos = Product.objects.all()
    return render(request, 'store.html', {'produtos': produtos, 'usuario': request.user})

@login_required
def store_filter(request, product_type):
    produtos = Product.objects.filter(product_type=product_type)
    return render(request, 'store.html', {'produtos': produtos, 'usuario': request.user})

@login_required
def register_product(request):
    if request.user.user_type != 'vendedor':
        messages.error(request, 'Você não tem permissão para acessar essa rota!')
        return redirect('store')

    if request.method == 'POST':
        nome = request.POST.get('name')
        preco = request.POST.get('price')
        descricao = request.POST.get('description')
        product_type = request.POST.get('product_type')
        imagem = request.FILES.get('image')

        if not all([nome, preco, descricao, product_type, imagem]):
            messages.warning(request, 'Nenhum campo pode ficar vazio')
            return redirect('register_product')

        if Product.objects.filter(nome=nome).exists():
            messages.warning(request, 'Este produto já está cadastrado!')
            return render(request, 'register_product.html', {'usuario': request.user})

        ext = imagem.name.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        file_path = default_storage.save(f'products/{filename}', imagem)

        produto = Product(
            nome=nome,
            preco=preco,
            descricao=descricao,
            product_type=product_type,
            image=file_path
        )
        produto.save()

        messages.success(request, 'Produto cadastrado com sucesso!')
        return redirect('store')

    return render(request, 'register_product.html', {'usuario': request.user})

@login_required
def product_details(request, product_id):
    produto = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        if request.user.user_type == 'cliente':
            quantidade = request.POST.get('quantidade')

            if not quantidade:
                messages.warning(request, 'É necessário uma quantidade para adicionar ao carrinho')
                return redirect('product_details', product_id=product_id)

            quantidade = int(quantidade)
            existing_item = CartItem.objects.filter(user=request.user, product=produto).first()

            if existing_item:
                existing_item.quantity += quantidade
                existing_item.save()
            else:
                new_item = CartItem(
                    product=produto,
                    product_name=produto.nome,
                    product_price=produto.preco,
                    quantity=quantidade,
                    user=request.user
                )
                new_item.save()

            messages.success(request, 'Produto adicionado ao carrinho, continue comprando!')
            return redirect('store')

    return render(request, 'product_details.html', {'produto': produto, 'usuario': request.user})

@login_required
def edit_product(request, product_id):
    produto = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        preco = request.POST.get('preco')
        descricao = request.POST.get('descricao')
        product_type = request.POST.get('product_type')
        imagem = request.FILES.get('image')

        if not all([nome, preco, descricao, product_type]):
            messages.warning(request, 'Nenhum campo pode ficar vazio')
            return redirect('edit_product', product_id=product_id)

        produto.nome = nome
        produto.preco = preco
        produto.descricao = descricao
        produto.product_type = product_type

        if imagem:
            ext = imagem.name.split('.')[-1]
            filename = f"{uuid.uuid4()}.{ext}"
            file_path = default_storage.save(f'products/{filename}', imagem)
            produto.image = file_path

        produto.save()
        messages.success(request, 'Produto atualizado com sucesso!')
        return redirect('store')

    return render(request, 'edit_product.html', {'produto': produto, 'usuario': request.user})

@login_required
def delete_product(request, product_id):
    if request.user.user_type != 'vendedor':
        raise PermissionDenied

    produto = get_object_or_404(Product, pk=product_id)
    produto.delete()
    messages.success(request, 'Produto deletado com sucesso!')
    return redirect('store')

@login_required
def carrinho(request):
    itens = CartItem.objects.filter(user=request.user)
    return render(request, 'carrinho.html', {'itens': itens, 'usuario': request.user})

@login_required
def item_details(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)

    if item.user_id != request.user.id:
        raise PermissionDenied

    if request.method == 'POST':
        if 'delete' in request.POST:
            item.delete()
            messages.success(request, 'Item removido do carrinho.')
            return redirect('carrinho')

        new_quantity = int(request.POST.get('quantity', item.quantity))
        if new_quantity <= 0:
            item.delete()
            messages.success(request, 'Item removido do carrinho.')
        else:
            item.quantity = new_quantity
            item.save()
            messages.success(request, 'Quantidade atualizada.')

        return redirect('carrinho')

    return render(request, 'pedido_details.html', {'item': item, 'usuario': request.user})

@login_required
def finalizar_carrinho(request):
    itens = CartItem.objects.filter(user=request.user)
    if not itens.exists():
        messages.warning(request, 'Seu carrinho está vazio.')
        return redirect('carrinho')

    order = Order.objects.create(user=request.user, created_at=timezone.now())

    for item in itens:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product_name,
            product_price=item.product_price,
            quantity=item.quantity
        )
    itens.delete()

    messages.success(request, 'Pedido realizado com sucesso!')
    return redirect('store')

@login_required
def order_list(request):
    if request.user.user_type == 'vendedor':
        lista = Order.objects.all()
        return render(request, 'lista_pedidos.html', {'order': lista})