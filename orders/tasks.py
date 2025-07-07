from celery import shared_task
from .models import Order, OrderProduct
from django.core.mail import send_mail


@shared_task
def task_order_create(order_id):
    order = Order.objects.get(id = order_id)
    return f"{order.paid}"