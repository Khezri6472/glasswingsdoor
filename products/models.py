from django.db import models
from django.shortcuts import reverse
from django.core.validators import MinValueValidator
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey


from uuid import uuid4


class Category(MPTTModel):
    title = models.CharField(max_length=255 , verbose_name=_('Title'))
    parent = TreeForeignKey('self', blank=True,null=True, on_delete=models.CASCADE, related_name='children',verbose_name=_('Parent'))
    slug=models.SlugField(allow_unicode=True,verbose_name=_('Slug'))
    top_product = models.ForeignKey('Product', on_delete=models.SET_NULL, blank=True, null=True, related_name='+',verbose_name=_('Top Product'))
    class MPTTMeta:
        order_insertion_by = ['id']
        verbose_name = _('Category')
        verbose_name_plural = _('categories')
    def __str__(self):
        return self.title
   
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('categories')

class Discount(models.Model):
    discount = models.FloatField(verbose_name=_('Discount'))
    description = models.CharField(max_length=255,verbose_name=_('Description'))

    def __str__(self):
        return f'{str(self.discount)} | {self.description}'
    class Meta:
        verbose_name = _('Discount')
        verbose_name_plural = _('Discounts')

class Product(models.Model):
    name = models.CharField(max_length=255,verbose_name=_('Name'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products',verbose_name=_('Category'))
    slug = models.SlugField(allow_unicode=True,verbose_name=_('Slug'))
    description = RichTextField(verbose_name=_('Description'))
    short_description = models.TextField(verbose_name=_('Short Description'))
    unit_price = models.PositiveIntegerField(verbose_name=_('Unit Price'))
    inventory = models.IntegerField(validators=[MinValueValidator(0)],verbose_name=_('Inventory'))
    datetime_created = models.DateTimeField(auto_now_add=True,verbose_name=_('Datetime Created'))
    datetime_modified = models.DateTimeField(auto_now=True,verbose_name=_('Datetime Modified'))
    discounts = models.ManyToManyField(Discount, blank=True,verbose_name=_('Discounts'))

    unit_code=models.CharField(max_length=4,unique=True,verbose_name=_('Unit Code'))
    main_image = models.ImageField(upload_to='product/product_image/main_image/', blank=True, verbose_name=_('Main Product Image'))

    related_products = models.ManyToManyField("self", blank=True, verbose_name=_('Related Products'))

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return reverse('product_detail', kwargs={ 'slug': self.slug , 'unit_code': self.unit_code,})



class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE,verbose_name=_('Product'))
    image = models.ImageField(upload_to='product/product_image/other_image/',verbose_name=_('Image'))  # محل ذخیره تصاویر
    alt_text = models.CharField(max_length=255, blank=True,verbose_name=_('Image Description'))  # توضیح عکس

    def __str__(self):
        return f"Image for {self.product.name}"

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')

class TechnicalSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications',verbose_name=_('Product'))
    key = models.CharField(max_length=100, verbose_name=_('Key'))  # عنوان مشخصه فنی، مثلاً "پردازنده"
    value = models.CharField(max_length=255,verbose_name=_('Value'))  # مقدار مشخصه، مثلاً "Intel Core i7"
    class Meta:
        verbose_name = _('Technical Specification')
        verbose_name_plural = _('Technical Specifications')
    def __str__(self):
        return f"{self.key}: {self.value}"

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,verbose_name=_('User') )
    phone_number = models.CharField(max_length=255,verbose_name=_('Phone Number'))
    birth_date = models.DateField(null=True, blank=True,verbose_name=_('Birth Date'))

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    class Meta:
        permissions = [
            ('send_private_email', 'Can send private email to user by the button')
        ]
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')


class Address(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE,
                                     primary_key=True,verbose_name=_('Customer'))
    province = models.CharField(max_length=255,verbose_name=_('Province'))
    city = models.CharField(max_length=255,verbose_name=_('City'))
    street = models.CharField(max_length=255,verbose_name=_('Street'))
    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

class UnpaidOrderManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Order.ORDER_STATUS_UNPAID)


class Order(models.Model):
    ORDER_STATUS_PAID = 'p'
    ORDER_STATUS_UNPAID = 'u'
    ORDER_STATUS_CANCELED = 'c'
    ORDER_STATUS = [
        (ORDER_STATUS_PAID,_('Paid')),
        (ORDER_STATUS_UNPAID,_('Unpaid')),
        (ORDER_STATUS_CANCELED,_('Canceled')),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders',verbose_name='Customer')
    datetime_created = models.DateTimeField(auto_now_add=True,verbose_name='Datetime Created')
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default=ORDER_STATUS_UNPAID,
                              verbose_name='Status')

    objects = models.Manager()
    unpaid_orders = UnpaidOrderManger()
    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
    
    def __str__(self):
        return f'Order {self.id}'

    def get_total_price(self):
        return sum(item.quantity * item.price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = [['order', 'product']]
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    def __str__(self):
        return f'OrderItem {self.id}: {self.product} x {self.quantity} (price:{self.unit_price})'

class CommentManger(models.Manager):
    def get_approved(self):
        return self.get_queryset().filter(status=Comment.COMMENT_STATUS_APPROVED)


class ApprovedCommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Comment.COMMENT_STATUS_APPROVED)


class Comment(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, _('Waiting')),
        (COMMENT_STATUS_APPROVED, _('Approved')),
        (COMMENT_STATUS_NOT_APPROVED, _('Not Approved')),
    ]

    PRODUCT_STARS = [
        ('1', _('Very Bad')),
        ('2', _('Bad')),
        ('3', _('Normal')),
        ('4', _('Good')),
        ('5', _('Perfect')),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments',
                                verbose_name='Product')
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Comment author'
    )
    body = models.TextField(verbose_name='Content')
    datetime_created = models.DateTimeField(auto_now_add=True,verbose_name='Datetime Created')
    status = models.CharField(max_length=2, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING,
                              verbose_name='Status')
    stars = models.CharField(max_length=10, choices=PRODUCT_STARS, verbose_name=_('What is your score?'))

    objects = CommentManger()
    approved = ApprovedCommentManager()

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.product.id])
    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')