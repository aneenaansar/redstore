from django.shortcuts import render, redirect, get_object_or_404
from mainapp.models import Item
from .cart import CartManager

cart_manager = CartManager()

def add_to_cart(request, item_id):
    cart_manager.add_to_cart(request, item_id)
    return redirect('cart:view_cart')

def view_cart(request):
    cart_items = cart_manager.get_cart_items(request)
    cart_tax=cart_manager.get_cart_tax(request)
    
    for cart_item in cart_items:
        cart_item.total_price=cart_item.item.price*cart_item.quantity
    cart_total = sum(item.item.price * item.quantity for item in cart_items)
    cart_total_with_tax=cart_total+cart_tax
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'cart_total': cart_total,'cart_tax':cart_tax,'cart_total_with_tax':cart_total_with_tax})

def update_cart(request, cart_item_id):
    if request.method == 'POST':
        new_quantity = int(request.POST.get('new_quantity', 1))
        cart_manager.update_quantity(request, cart_item_id, new_quantity)
    return redirect('cart:view_cart')

def remove_from_cart(request, cart_item_id):
    cart_manager.remove_item(request, cart_item_id)
    return redirect('cart:view_cart')
