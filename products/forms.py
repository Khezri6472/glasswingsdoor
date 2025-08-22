from django import forms
from .models import Comment


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

