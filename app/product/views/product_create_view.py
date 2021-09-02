from app.product.forms.product_create_forms import ProductCreateForm
from app.product.models.image import Image
from app.product.models.product import Product
from django.urls import reverse_lazy
from django.views.generic import CreateView


class CreateProductView(CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'product/product_create.html'
    success_url = reverse_lazy('product:product_create')
