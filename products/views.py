from django.views import generic
from django.shortcuts import get_object_or_404,render
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Product,Category,Comment
from .forms import CommentForm


class ProductListView(generic.ListView):
    model=Product
    template_name='product/product_list.html'
    context_object_name='products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
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

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Product.objects.filter(category_id=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(id=self.kwargs['category_id'])
        return context