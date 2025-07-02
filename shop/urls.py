from django.urls import path
from . import views
urlpatterns = [
    path('', views.CategoryListView.as_view(), name = 'categories_url'),
    path('search/', views.search_field, name='search_field'),
    path('<slug>/',views.CategoryListView.as_view(), name = 'category_url'),
    path('product/<slug>/<pk>/', views.ProductListView.as_view(), name = 'product_url'),
    path('coupon/apply/', views.coupon_apply, name = 'coupon_apply')
]

