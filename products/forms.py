from django import forms
from .models import Comment

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'id': 'id_content'}),
        }

    class Media:
        js = (
            'https://cdn.ckeditor.com/ckeditor5/39.0.1/classic/ckeditor.js',
            'assets/js/ckeditor_init.js',
        )
        css = {
            'all': ('assets/css/admin_ckeditor.css',)
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'stars', ]


SORT_CHOICES = (
    ("relevance", "مرتبط‌ترین"),
    ("new", "جدیدترین"),
    ("price_asc", "ارزان‌ترین"),
    ("price_desc", "گران‌ترین"),
    ("rating", "بالاترین امتیاز"),
    ("bestseller", "پرفروش‌ترین"),
)

BOOL3 = (("", "همه"), ("true", "بله"), ("false", "خیر"))

class ProductSearchForm(forms.Form):
    q = forms.CharField(required=False, label="جستجو")
    category = forms.SlugField(required=False)                 # slug دسته‌بندی
    min_price = forms.IntegerField(required=False, min_value=0)
    max_price = forms.IntegerField(required=False, min_value=0)
    in_stock = forms.ChoiceField(required=False, choices=BOOL3)
    discounted = forms.ChoiceField(required=False, choices=(("", "مهم نیست"), ("true", "فقط تخفیف‌دار")))
    min_rating = forms.IntegerField(required=False, min_value=1, max_value=5)
    sort = forms.ChoiceField(required=False, choices=SORT_CHOICES)
    page = forms.IntegerField(required=False, min_value=1)

