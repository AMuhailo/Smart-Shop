from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 100, blank = True)
    
    
    class Meta:
        ordering = ['-title', '-id']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    def save(self, *args, **kwargs):
        if  not self.slug:
            self.slug = slugify(self.title) + slugify(self.pk)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title}"
    
class Product(models.Model):
    image = models.ImageField(upload_to='product/', blank = True, null = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = 'product_category')
    name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 100, blank = True)
    description = models.TextField(blank = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    available = models.BooleanField(default = True)
    
    created = models.DateTimeField(auto_now_add  = True)
    updated = models.DateTimeField(auto_now = True)
    
    class Meta:
        ordering = ['-id']
        indexes = [models.Index(fields = ['-id']),
                   models.Index(fields = ['slug']),
                   models.Index(fields = ['-price']),
                   models.Index(fields = ['-created'])]
        
    def save(self, *args, **kwargs):
        if  not self.slug:
            self.slug = slugify(self.name) + f"{slugify(self.pk)}"
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}"
    
class Coupon(models.Model):
    code = models.CharField(max_length=100, unique = True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators = [MinValueValidator(0),MaxValueValidator(100)], help_text = 'Percantage value (0 to 100)')
    active = models.BooleanField()
    
    def __str__(self):
        return f"{self.code}"