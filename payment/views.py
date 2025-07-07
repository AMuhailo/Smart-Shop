from decimal import Decimal
from math import e
from django.http import HttpResponse
import stripe
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from orders.models import Order
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from payment.tasks import task_paid_canceled, task_paid_success

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id = order_id)
    if request.method == "POST":
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))
        session_data = {
            'mode':'payment',
            'client_reference_id':order.id,
            'success_url':success_url,
            'cancel_url':cancel_url,
            'line_items':[]
        }
        for item in order.products.all():
            session_data['line_items'].append({
                'price_data':{
                    'unit_amount':int(item.price * Decimal('100')),
                    'currency':'usd',
                    'product_data':{
                        'name':item.product.name,
                    },
                },
                'quantity':item.quantity,
            })
        if order.coupons:
            stripe_coupon = stripe.Coupon.create(name = order.coupons.code, percent_off = order.discount, duration='once')
            session_data['discounts'] = [{
                'coupon':stripe_coupon.id
            }]
        session = stripe.checkout.Session.create(**session_data)
        
        return redirect(session.url, code = 303)
    else:
        return render(request, 'components/payment/process.html',locals())
    
def payment_completed(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id = order_id)
    task_paid_success.delay(order.id)
    return render(request, 'components/payment/completed.html')

def payment_canceled(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id = order_id)
    task_paid_canceled.delay(order.id)
    return render(request, 'components/payment/canceled.html')

@require_POST
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    signature_header = request.META("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, signature_header, endpoint_secret) 
    except:
        return HttpResponse(status = 400)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(f"{session.mode} {session.payment_status}")
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id = session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status = 400)
            order.payable = True
            order.save()
    return HttpResponse(status = 200)
        