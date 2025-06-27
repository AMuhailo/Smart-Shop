from unicodedata import category
from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from .models import Category , Product
# Create your views here.

class CategoryListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'components/main-page.html'
    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        self.category = None
        products = Product.objects.filter(available = True)
        if category_slug:
            try:
                self.category = Category.objects.get(slug = category_slug)
                products = products.filter(category = self.category)
            except Category.DoesNotExist:
                pass
        return products
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context['category'] = self.category 
        return context
    

class ProductListView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'components/product-page.html'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
    

