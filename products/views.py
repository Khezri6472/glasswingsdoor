from django.views import generic
from django.shortcuts import get_object_or_404,render
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Sum, Case, When, IntegerField, F
from django.db.models.functions import Cast
from products.models import Product, Comment, Category
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from .forms import ProductSearchForm
from .services.search import product_search
from .models import Product
import random

from .models import Product,Category,Comment
from .forms import CommentForm


class ProductListView(generic.ListView):
    model=Product
    template_name='product/product_list.html'
    context_object_name='products'
    paginate_by = 20  # در صورت نیاز


    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        return context
     


class ProductDetailView(generic.DetailView):
    model=Product
    template_name='product/product_detail.html'
    context_object_name='product_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['related_products'] = product.related_products.all()
        context['comment_form'] = CommentForm()
        return context

# @login_required 
class CommentCreateView(generic.CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        product_id = int(self.kwargs['product_id'])
        product = get_object_or_404(Product, id=product_id)
        obj.product = product

        messages.success(self.request, _('Comment successfully created'))
        return super().form_valid(form)

def product_quick_view(request,pk):
    product=get_object_or_404(Product,pk=pk) 
    return render(request,'product/product_quick_view.html',{'product':product})

class ProductByCategoryView(generic.ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'
    paginate_by = 28
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        descendants = self.category.get_descendants(include_self=True)
        return Product.objects.filter(category__in=descendants).select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context
    


class ProductSearchListView(generic.ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'
    paginate_by = 12  # هر صفحه 12 محصول

    def get_queryset(self):
        # استفاده از تابع جستجوی آماده
        return product_search(self.request.GET)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # افزودن page_obj و is_paginated به context
        context['page_obj'] = context['page_obj']  # همان object_list
        context['is_paginated'] = context['is_paginated']
        return context