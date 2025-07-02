from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order , OrderProduct
# Register your models here.

def order_detail(obj):
    url = reverse('orders:order_detail', args = [obj.id])
    return mark_safe(f"<a href='{url}'>View</a>")
class OrderProductInLine(admin.TabularInline):
    model = OrderProduct
    fields = ['product','quantity','price']
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email','number','postal_code','city','post', 'paid','created', 'updated', 'payable',order_detail] 
    list_filter = ['post','paid','payable']
    date_hierarchy = 'created'
    inlines = [OrderProductInLine]
    
