from django.shortcuts import render

from django.views.generic.base import TemplateView
from django.views import generic
from django.shortcuts import get_object_or_404,render
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from products.models import Product,Category,Comment

class AboutUsView(generic.TemplateView):
    template_name='pages/about_us.html'

class HomePageView(generic.ListView):
    model=Product
    template_name='home.html'
    context_object_name='products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
    
    
 

