from django.shortcuts import render

from django.views.generic.base import TemplateView
from django.views import generic
from django.shortcuts import get_object_or_404,render
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random

from products.models import Product,Category,Comment

class AboutUsView(generic.TemplateView):
    template_name='pages/about_us.html'

class HomePageView(generic.ListView):
    model=Product
    template_name='home.html'
    context_object_name='products'

    def get_queryset(self):
        # این لیست اصلی محصولات (نماینده تمام محصولات سایت)
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # محصولات تصادفی (پیشنهاد لحظه‌ای)
        product_ids = list(Product.objects.values_list('id', flat=True))
        selected_ids = random.sample(product_ids, min(4, len(product_ids)))
        context['random_products'] = Product.objects.filter(id__in=selected_ids)

        # دسته‌بندی‌ها
        context['categories'] = Category.objects.all()

        return context
    
    
 

