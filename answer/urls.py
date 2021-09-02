from django.urls import path
from app.product.views.product_create_view import CreateProductView
from app.product.views.product_search_view import ProductSearchListView
from app.product.views.product_update_view import ProductUpdateView
from app.product.views.product_detail_view import ProductDetailView
from django.views.generic import TemplateView

app_name = 'product'

urlpatterns = [
    path('', TemplateView.as_view(template_name='product/product_top.html'), name='top'),
    path('search/', ProductSearchListView.as_view(), name='product_search'),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('create/', CreateProductView.as_view(), name='product_create'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
]
