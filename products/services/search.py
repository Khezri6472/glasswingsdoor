from django.db.models import Q, Avg, Sum, Case, When, IntegerField, F
from django.db.models.functions import Cast
from products.models import Product, Comment, Category

def _parse_bool_choice(val):
    if val == "true": return True
    if val == "false": return False
    return None

def product_search(params):
    q = (params.get("q") or "").strip()

    qs = (Product.objects
          .select_related("category")
          .prefetch_related("discounts", "images")
          .annotate(
              # stars رشته‌ای است: 1..5 → برای Avg باید Cast کنیم
              avg_rating=Avg(
                  Cast(F("comments__stars"), IntegerField()),
                  filter=Q(comments__status=Comment.COMMENT_STATUS_APPROVED)
              ),
              sales_qty=Sum("order_items__quantity"),
          ))

    # فیلتر متن
    if q:
        qs = qs.annotate(
            relevance=Case(
                When(name__icontains=q, then=3),
                When(short_description__icontains=q, then=2),
                When(description__icontains=q, then=1),
                default=0, output_field=IntegerField()
            )
        ).filter(
            Q(name__icontains=q) |
            Q(short_description__icontains=q) |
            Q(description__icontains=q) |
            Q(category__title__icontains=q)
        )
    else:
        qs = qs.annotate(relevance=Case(default=1, output_field=IntegerField()))

    # فیلتر دسته‌بندی (همراه با زیرشاخه‌ها - MPTT)
    cat_slug = params.get("category")
    if cat_slug:
        cat = Category.objects.filter(slug=cat_slug).first()
        if cat:
            cats = cat.get_descendants(include_self=True)
            qs = qs.filter(category__in=cats)

    # فیلتر قیمت
    if params.get("min_price"):
        qs = qs.filter(unit_price__gte=params["min_price"])
    if params.get("max_price"):
        qs = qs.filter(unit_price__lte=params["max_price"])

    # موجودی
    in_stock = _parse_bool_choice(params.get("in_stock"))
    if in_stock is True:
        qs = qs.filter(inventory__gt=0)
    elif in_stock is False:
        qs = qs.filter(inventory__lte=0)

    # تخفیف‌دار
    discounted = _parse_bool_choice(params.get("discounted"))
    if discounted is True:
        qs = qs.filter(discounts__isnull=False)

    # حداقل امتیاز
    if params.get("min_rating"):
        minr = int(params["min_rating"])
        qs = qs.filter(
            comments__status=Comment.COMMENT_STATUS_APPROVED,
            comments__stars__in=[str(i) for i in range(minr, 6)]
        )

    # مرتب‌سازی
    sort = params.get("sort") or "relevance"
    ordering = {
        "relevance": ("-relevance", "-avg_rating", "-datetime_created"),
        "new": ("-datetime_created",),
        "price_asc": ("unit_price",),
        "price_desc": ("-unit_price",),
        "rating": ("-avg_rating", "-datetime_created"),
        "bestseller": ("-sales_qty", "-datetime_created"),
    }[sort]

    return qs.order_by(*ordering).distinct()
