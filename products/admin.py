from django.contrib import admin, messages
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext as _
from mptt.admin import DraggableMPTTAdmin

from . import models

@admin.register(models.Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('id','tree_actions', 'indented_title', 'slug','parent')
    # list_display=['id','tree_actions', 'indented_title','title','slug','parent']
    list_per_page = 40
    search_fields = ['title', ]
    prepopulated_fields = {
        'slug': ['title', ]
    }
    # list_editable = ['title','slug']
    # list_display_links = None
    def __str__(self):
        return self.title

#فیلتر بر اساس موجودی محصولات
class InventoryFilter(admin.SimpleListFilter):
    LESS_THAN_3 = '<3'
    BETWEEN_3_and_10 = '3<=10'
    MORE_THAN_10 = '>10'
    title = _('Critical Inventory Status')
    parameter_name = _('inventory')

    def lookups(self, request, model_admin):
        return [
            (InventoryFilter.LESS_THAN_3, _('High')),
            (InventoryFilter.BETWEEN_3_and_10, _('Medium')),
            (InventoryFilter.MORE_THAN_10, _('OK')),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == InventoryFilter.LESS_THAN_3:
            return queryset.filter(inventory__lt=3)
        if self.value() == InventoryFilter.BETWEEN_3_and_10:
            return queryset.filter(inventory__range=(3, 10))
        if self.value() == InventoryFilter.MORE_THAN_10:
            return queryset.filter(inventory__gt=10)

class TechnicalSpecificationInline(admin.TabularInline):  # یا admin.StackedInline
    model = models.TechnicalSpecification
    extra = 3  # تعداد ردیف‌های خالی پیش‌فرض 
class ProductImageInLine(admin.TabularInline):
    model = models.ProductImage
    extra = 2

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','unit_code', 'name', 'inventory', 'unit_price', 'inventory_status', 'product_category', 'num_of_comments']
    list_per_page = 10
    list_editable = ['unit_price']
    list_select_related = ['category']
    list_filter = ['datetime_created', InventoryFilter]
    actions = ['clear_inventory']
    search_fields = ['name', ]
    filter_horizontal = ['related_products'] 
    prepopulated_fields = {
        'slug': ['name', ]
    }
    inlines = [TechnicalSpecificationInline, ProductImageInLine] 

    def get_queryset(self, request):
        return super().get_queryset(request) \
                .prefetch_related('comments') \
                .annotate(
                    comments_count=Count('comments'),
                )
    #وضعیت موحودی محصولات
    @admin.display(description=_('inventory_status'), )
    def inventory_status(self, product):
        if product.inventory < 10:
            return _('Low')
        if product.inventory > 50:
            return _('High')
        return _('Medium')
    
    @admin.display(description=_('# comments'), ordering=_('comments_count'))
    def num_of_comments(self, product):
        url = (
            reverse('admin:products_comment_changelist') 
            + '?'
            + urlencode({
                'product__id': product.id,
            })
        )
        return format_html('<a href="{}">{}</a>', url, product.comments_count)
        
    #سورت کردن بر اساس عنوان category
    @admin.display(description=_('product_category'),ordering='category__title')
    def product_category(self, product):
        return product.category.title
    
    @admin.action(description=_('Clear inventory'))
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{update_count} of products inventories cleared to zero.',
            messages.ERROR,
        )

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','body', 'product', 'status', ]
    list_editable = ['status']
    list_per_page = 10
    autocomplete_fields = ['product', ]


# class OrderItemInline(admin.TabularInline):
#     model = models.OrderItem
#     fields = ['product', 'quantity', 'unit_price']
#     extra = 0
#     min_num = 1


# @admin.register(models.Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'customer', 'status', 'datetime_created', 'num_of_items']
#     list_editable = ['status']
#     list_per_page = 10
#     ordering = ['-datetime_created']
#     inlines = [OrderItemInline]

#     #گرفتن آیتم های یک سفارش
#     def get_queryset(self, request):
#         return super() \
#                 .get_queryset(request) \
#                 .prefetch_related('items') \
#                 .annotate(
#                     items_count=Count('items')
#                 )

#     @admin.display(ordering='items_count', description='# items')
#     def num_of_items(self, order):
#         return order.items_count




#@admin.register(models.TechnicalSpecification)
#class TechnicalSpecificationAdmin(admin.ModelAdmin):
#    list_display=['key','value',]
 #   list_per_page = 10
    # list_editable = ['key','value']


# @admin.register(models.ProductImage)
# class ProductImageAdmin(admin.ModelAdmin):
#     list_display=['product','alt_text']
#     list_per_page = 10
    # list_editable = ['product','alt_text']


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', ]
    list_per_page = 10
    ordering = ['user__last_name', 'user__first_name', ]
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith', ]

    def first_name(self, customer):
        return customer.user.first_name
    
    def last_name(self, customer):
        return customer.user.last_name

    def email(self, customer):
        return customer.user.email


# @admin.register(models.OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ['order', 'product', 'quantity', 'unit_price']
#     autocomplete_fields = ['product', ]


# class CartItemInline(admin.TabularInline):
#     model = models.CartItem
#     fields = ['id', 'product', 'quantity']
#     extra = 0
#     min_num = 1


# @admin.register(models.Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ['id', 'created_at']
#     inlines = [CartItemInline]
