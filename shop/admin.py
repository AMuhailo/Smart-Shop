from django.contrib import admin
from .models import Category, Product

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
    