import uuid
from django.db import models

from shop.models import Product

# Create your models here.
class Order(models.Model):
    POST_USE = [
        ('UK','UrkPost'),
        ('NW','NewPost'),
    ]
    PAID_USE = [
        ('card','Card'),
        ('delivery','   '),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    
    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields = ['-created'])]
        
    def __str__(self):
        return f"Order №{str(self.id)[-4]}"
    
    def get_total_cost(self):
        return sum(item.get_cost for item in self.products.all())
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = 'products')
    
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'order_products')
    quantity = models.PositiveIntegerField(default = 1)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    
    
    def __str__(self):
        return self.order
    
    def get_cost(self):
        return self.price * self.quantity