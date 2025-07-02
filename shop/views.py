from unicodedata import category
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView

from shop.forms import CouponField
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
        context['cart_form'] = CartField()
        context["categories"] = Category.objects.all()
        return context
    


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponField(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact = code, valid_from__lte = now,valid_to__gte = now, active = True)
            request.session['coupon_id'] = coupon.id
        except:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')    