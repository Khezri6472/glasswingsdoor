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


class HomeView(generic.ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    def get_queryset(self):
       
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_products = list(Product.objects.all())  # همه محصولات
        if all_products:
            def random_products_block(count=None):
                if count is None:
                    count = random.randint(10, 15)
                return random.sample(all_products, min(count, len(all_products)))

            # 🔹 بلوک‌های مختلف محصولات
            context['random_products'] = random_products_block(5)
            context['best_sellers'] = random_products_block()
            context['new_products'] = random_products_block()
            context['feature_products'] = random_products_block()
        else:
            context['random_products'] = []
            context['best_sellers'] = []
            context['new_products'] = []
            context['feature_products'] = []

        # 🔹 دسته‌بندی‌ها
        context['categories'] = Category.objects.all()

        return context