from decimal import Decimal
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from shop.models import Coupon, Product

# Create your models here.
class Order(models.Model):
    POST_USE = [
        ('UK','UrkPost'),
        ('NW','NewPost'),
    ]
    PAID_USE = [
        ('card','Card'),
        ('delivery','Delivery'),
    ]
    coupons = models.ForeignKey(Coupon, on_delete = models.SET_NULL, blank = True, null = True, related_name = 'orders_coupons')
    discount = models.IntegerField(default = 0, validators = [MinValueValidator(0),MaxValueValidator(100)])
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField()
    number = models.CharField(max_length = 20)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length = 100)
    post = models.CharField(choices = POST_USE,blank = False, default = 'NW')
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    paid = models.CharField(choices = PAID_USE, blank = False, default = 'card') 
    
    payable = models.BooleanField(default = False)
    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields = ['-created'])]
        
    def __str__(self):
        return f"Order №{str(self.id)}"
    
    def get_total_cost(self):
        return self.get_total_cost_discount() - self.get_discount()
    
    def get_total_cost_discount(self):
        return sum(item.get_cost() for item in self.products.all())
    
    def get_discount(self):
        total_cost = self.get_total_cost_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = 'products')
    
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'order_products')
    quantity = models.PositiveIntegerField(default = 1)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    
    
    def __str__(self):
        return f"{self.pk}"
    
    def get_cost(self):
        return self.price * self.quantity