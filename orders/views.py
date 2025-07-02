from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
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
            order = form.save(commit=False)
            order.coupons = cart.coupon
            order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderProduct.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                )
            cart.clear()

            if order.paid == "delivery":
                return redirect('orders:order_done')
            else:
                request.session['order_id'] = order.id
                return redirect(reverse('payment:process'))

    else:
        form = OrderAdd()

    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'components/orders.html', context)


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id = order_id)
    return render(request, 'components/include/orders_detail.html',{'order':order})
    