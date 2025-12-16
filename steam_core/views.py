from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, CartItem, Order


def _get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def product_list(request):
    products = Product.objects.filter(is_available=True)
    return render(request, 'steam_core/game_list.html', {'products': products})


def add_to_cart(request, product_id):
    session_key = _get_session_key(request)
    product = get_object_or_404(Product, id=product_id, is_available=True)

    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        session_key=session_key,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('steam_core:cart_view')


def cart_view(request):
    session_key = _get_session_key(request)
    cart_items = CartItem.objects.filter(session_key=session_key)

    total = sum(item.total_price for item in cart_items)

    return render(request, 'steam_core/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


def create_order(request):
    session_key = _get_session_key(request)
    cart_items = CartItem.objects.filter(session_key=session_key)

    if not cart_items.exists():
        return redirect('steam_core:cart_view')

    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()

        if not phone and not email:
            messages.error(request, "Введи телефон або email")
            return redirect('steam_core:cart_view')

        order = Order.objects.create(
            session_key=session_key,
            phone=phone,
            email=email
        )

        cart_items.delete()

        messages.success(request, f"Замовлення #{order.id} створено")
        return redirect('steam_core:product_list')


def remove_from_cart(request, item_id):
    session_key = _get_session_key(request)
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        session_key=session_key
    )
    cart_item.delete()
    return redirect('steam_core:cart_view')
