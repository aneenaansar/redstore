from django.conf import settings
from .models import Cart, CartItem
from mainapp.models import Item
from  decimal import Decimal

CART_SESSION_KEY = getattr(settings, 'CART_SESSION_KEY', 'cart_id')

class CartManager:
    def get_cart(self, request):
        cart_id = request.session.get(CART_SESSION_KEY)
        if cart_id:
            cart = Cart.objects.get(pk=cart_id)
        else:
            cart = Cart.objects.create(user=request.user)
            request.session[CART_SESSION_KEY] = cart.id
        return cart
    
    def add_to_cart(self, request, item_id):
        cart = self.get_cart(request)
        item = Item.objects.get(pk=item_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
        cart_item.quantity += 1
        cart_item.save()
    
    def get_cart_items(self, request):
        cart = self.get_cart(request)
        return cart.cartitem_set.all()

    def update_quantity(self, request, cart_item_id, new_quantity):
        cart=self.get_cart(request)
        for cart_item in cart:
            if cart_item.item.id == cart_item_id:
                cart_item.quantity = new_quantity
                self.save_cart(request,cart)
                break

    def remove_item(self, request, cart_item_id):
        cart_item = CartItem.objects.get(pk=cart_item_id)
        cart_item.delete()

    def get_cart_tax(self,request):
        cart_items=self.get_cart_items(request)
        tax_rate=Decimal('0.10')
        cart_tax = sum(Decimal(item.item.price) * item.quantity * tax_rate for item in cart_items)

        return cart_tax    
    

    