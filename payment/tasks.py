from celery import shared_task
from orders.models import Order, OrderProduct
from django.core.mail import send_mail


@shared_task
def task_paid_success(order_id):
    order = Order.objects.get(id = order_id)
    subject = f"Order №{order.id}"
    message = 'Paid was success. Wait for a call to confirm the data.'
    return send_mail(subject, message, 'admin@gmail.com',['amuhailo25@gmail.com'])

@shared_task
def task_paid_canceled(order_id):
    order = Order.objects.get(id = order_id)
    subject = f"Order №{order.id}"
    message = 'An error occurred during payment. Please try payment again.'
    return send_mail(subject, message, 'admin@gmail.com',['amuhailo25@gmail.com'])