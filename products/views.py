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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .models import Product,Category,Comment
from .forms import CommentForm

class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_products = list(Product.objects.all())  # همه محصولات

        if all_products:
            def random_products_block(count=None):
                if count is None:
                    count = random.randint(10, 15)
                return random.sample(all_products, min(count, len(all_products)))

            context['random_products'] = random_products_block(5)
            context['best_sellers'] = random_products_block()
            context['new_products'] = random_products_block()
            context['feature_products'] = random_products_block()
        else:
            context['random_products'] = []
            context['best_sellers'] = []
            context['new_products'] = []
            context['feature_products'] = []

        context['categories'] = Category.objects.all()
        return context

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
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product_detail'

    def get_object(self, queryset=None):
        unit_code = self.kwargs.get("unit_code")
        slug = self.kwargs.get("slug")
        return Product.objects.get( slug=slug ,unit_code=unit_code,)

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
    


class SearchSuggestionsView(generic.View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q", "").strip()
        if not q:
            return JsonResponse({"results": []})

        # فیلتر ۱۰ محصول حداکثر و انتخاب ۳ تا رندوم
        products_qs = Product.objects.filter(name__icontains=q)[:10]
        products_list = list(products_qs)
        products = random.sample(products_list, min(5, len(products_list)))

        results = [
            {"id": p.id, "name": p.name, "url": p.get_absolute_url()}
            for p in products
        ]

        return JsonResponse({"results": results})


class UpdatePriceAPI(APIView):
    def post(self, request):
        unit_code = request.data.get('unit_code')
        new_price = request.data.get('price')
        user_price = request.data.get('user_price')  

        if not unit_code:
            return Response({'status': 'error', 'message': 'unit_code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(unit_code=unit_code)

            # اگر price فرستاده شده بود، آپدیت کن
            if new_price is not None:
                product.unit_price = new_price

            # اگر user_price فرستاده شده بود، آپدیت کن
            if user_price is not None:
                product.user_price = user_price

            product.save()

            return Response({
                'status': 'success',
                'message': 'Price updated successfully.',
                'data': {
                    'unit_code': unit_code,
                    'unit_price': product.unit_price,
                    'user_price': product.user_price
                }
            }, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({'status': 'error', 'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

class UpdateStockAPI(APIView):
    def post(self, request):
        unit_code = request.data.get('unit_code')
        new_stock = request.data.get('stock')

        try:
            product = Product.objects.get(unit_code=unit_code)
            product.inventory = new_stock
            product.save()
            return Response({'status': 'success', 'message': 'Stock updated successfully.'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'status': 'error', 'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)



