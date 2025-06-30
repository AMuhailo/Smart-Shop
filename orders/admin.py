from django.contrib import admin
from .models import Order , OrderProduct
# Register your models here.

class OrderProductInLine(admin.TabularInline):
    model = OrderProduct
    fields = ['product','quantity','price']
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email','number','postal_code','city', 'paid','created', 'updated'] 
    list_filter = ['paid']
    date_hierarchy = 'created'
    inlines = [OrderProductInLine]