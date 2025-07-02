from django.contrib import admin
from .models import Category, Product, Coupon

# Register your models here.
class ProductInLine(admin.TabularInline):
    model = Product
    fields = ['image','name','description','price','available']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    search_fields = ['title']
    inlines = [ProductInLine]
    
@admin.register(Product)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','category','image','description','price','available']
    search_fields = ['name']
    list_filter = ['category','available']
    
    
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code','valid_from','valid_to','discount','active']
    list_filter = ['active','valid_from','valid_to']
    search_fields = ['code']