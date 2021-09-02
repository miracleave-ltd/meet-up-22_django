from django.urls import path
from app.product.views.product_create_view import CreateProductView
from app.product.views.product_search_view import ProductSearchListView
from django.views.generic import TemplateView

app_name = 'product'

urlpatterns = [
    path('', TemplateView.as_view(template_name='product/product_top.html'), name='top'),
    path('search/', ProductSearchListView.as_view(), name='product_search'),
    path('create/', CreateProductView.as_view(), name='product_create'),
]
