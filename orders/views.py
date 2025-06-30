from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Order, OrderProduct 
from cart.cart import Cart
from .forms import OrderAdd
# Create your views here.

def order_done(request):
    return render(request, 'components/include/order_done.html')

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderAdd(request.POST)
        if form.is_valid():
            order = form.save(commit = False)
            order.save()
            for item in cart:
                OrderProduct.objects.create(order = order, product = item['product'], quantity = item['quantity'], price = item['price'])
            cart.clear()
        if order.paid == "delivery":
            return redirect('orders:order_done')
        else:
            return HttpResponse('Card')
            
    else:
        form = OrderAdd()
    context = {
        'cart':cart,
        'form':form,
    }
    return render(request, 'components/orders.html', context)