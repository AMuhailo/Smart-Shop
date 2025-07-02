from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from shop.forms import CouponField
from shop.models import Product
from .cart import Cart
from .form import CartField

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id = product_id)
    form = CartField(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,quantity = int(cd['quantity']), override=cd['override'])
    return redirect('cart:cart_detail')
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id = product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['item_override'] = CartField(initial={'quantity':item['quantity'], 'override':True})
    coupon_form = CouponField()
    context = {"cart":cart,
               'coupon_form':coupon_form}
    return render(request, 'components/cart.html',context)
# Create your views here.