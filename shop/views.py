from decimal import Decimal
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST, require_GET
from django.utils import timezone
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.utils.decorators import method_decorator
from shop.forms import CouponField, SearchField
from .models import Category, Coupon , Product
from cart.form import CartField
# Create your views here.

class CategoryListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'components/main-page.html'
    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        self.category = None
        self.products = Product.objects.filter(available = True)
        if category_slug:
            try:
                self.category = Category.objects.get(slug = category_slug)
                self.products = self.products.filter(category = self.category)
            except Category.DoesNotExist:
                pass
        return self.products
    
    def get_context_data(self, **kwargs):
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if max_price or max_price:
            self.products = Product.objects.filter(price__gte = Decimal(min_price), price__lte = Decimal(max_price))
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context['category'] = self.category 
        context['form_search'] = SearchField()
        context['products'] = self.products
        return context
    

class ProductListView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'components/product-page.html'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_form'] = CartField()
        context["categories"] = Category.objects.all()
        return context
    
    
class SearchForm(FormView):
    form_class = SearchField
    template_name = 'components/main-page-search.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['query'] = self.request.GET.get('query', None)
        context['results'] = []
        if self.request.GET.get('query'):
            form = SearchField(self.request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                search_vector = SearchVector('name', 'description')
                search_query_obj = SearchQuery(query)
                context['results'] = Product.objects.annotate(
                    search=search_vector,
                    rank=SearchRank(search_vector, search_query_obj)
                ).filter(search=search_query_obj).order_by('-rank')
        return context
    

@method_decorator(require_POST, name = 'dispatch')
class CouponApplyField(FormView):
    form_class = CouponField
    success_url = reverse_lazy('cart:cart_detail')
    def form_valid(self, form):
        now = timezone.now()
        form = CouponField(self.request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__iexact = code, valid_from__lte = now,valid_to__gte = now, active = True)
                self.request.session['coupon_id'] = coupon.id
            except Coupon.DoesNotExist:
                self.request.session['coupon_id'] = None
        return super().form_valid(form)
    
    def form_invalid(self, form):
        self.request.session['coupon_id'] = None
        return super().form_invalid(form)   
    